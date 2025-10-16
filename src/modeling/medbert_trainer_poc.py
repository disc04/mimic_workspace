"""
    Fine-tunes Med-BERT (Bio_ClinicalBERT) on diagnosis group prediction using local mimic-iv demo subset

    1. Load local csv to DataFrames (admissions, diagnoses_icd, patients)
    2. Merge into a cohort table
    3. Group ICD codes by subject_id or hadm_id
    4. Create text-like token sequences (e.g. “I10 E11 J18”)
    5. Fine-tune a BERT model (HuggingFace) for diagnosis group prediction
    6. Evaluates with accuracy and prints sample predictions
    7. Integrates with MLflow
"""

# pip install transformers[torch]` or `pip install 'accelerate>=0.26.0'`
# pip install --upgrade "transformers>=4.11.0"

import os
from os.path import join
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import Trainer, TrainingArguments
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import mlflow
import mlflow.pytorch
import torch
from utils import data_utils
from data_preparation import prepare_cohort_local
from tokenizer_utils import prepare_datasets
from utils.modeling_utils import load_config, set_device, get_model_signature, compute_metrics, print_mlflow_metrics
from config.project_config import DATA_PATH, CONFIG_PATH

#######################################################
# Somewhere in the middle of the HuggingFace code, the model changes from cpu to mps.
# So, I bring everything to "mps" in this script.
#######################################################

os.environ["TOKENIZERS_PARALLELISM"] = "false"

mimic4_path = join(DATA_PATH, "mimic-iv-clinical-database-demo-2.2")
raw_data_path = join(DATA_PATH, "raw")
config_path = join(CONFIG_PATH, "medbert_poc.yaml")


def train_model(device,
                config,
                train_ds,
                test_ds,
                num_labels,
                output_dir=None
                ):
    """
    Train Med-BERT model in two steps:
      1. Freeze encoder, train classifier head
      2. Unfreeze and fine-tune entire model
    """
    # Setup MLflow
    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    model = AutoModelForSequenceClassification.from_pretrained(
        config["model"]["pretrained_name"],
        num_labels=num_labels).to(device)

    # ---------------------------------------------------------------------
    # STEP 1 — Train classifier head
    # ---------------------------------------------------------------------
    for param in model.bert.parameters():
        param.requires_grad = False

    phase1_args = TrainingArguments(output_dir=f"{output_dir}/phase1_freeze",
                                    learning_rate=float(config["model"]["learning_rate_head"]),
                                    num_train_epochs=int(config["model"]["num_train_epochs_head"]),
                                    per_device_train_batch_size=int(config["model"]["per_device_train_batch_size"]),
                                    eval_strategy="epoch",
                                    save_strategy="epoch",
                                    logging_strategy="epoch",
                                    report_to=["mlflow"],
                                    load_best_model_at_end=True
                                    )

    print("Phase 1: Training classifier head only...\n")

    with ((mlflow.start_run(run_name="phase1_freeze"))):
        mlflow.log_params({"phase": "freeze_encoder",
                           "task": "diagnosis_group_prediction",
                           "batch_size": config["model"]["per_device_train_batch_size"],
                           "model": config["model"]["pretrained_name"]
                           })

        trainer = Trainer(model=model,
                          args=phase1_args,
                          train_dataset=train_ds,
                          eval_dataset=test_ds,
                          )

        trainer.train()
        trainer.save_model(f"{output_dir}/phase1_best")

        tokenizer = AutoTokenizer.from_pretrained(config["model"]["pretrained_name"])
        wrapped_model1, signature1, tmp_dir1 = get_model_signature(model, train_ds, tokenizer)
        mlflow.pytorch.log_model(pytorch_model=wrapped_model1,
                                 name="phase1_model",
                                 signature=signature1,
                                 )
        # Log tokenizer as an artifact
        mlflow.log_artifacts(tmp_dir1, artifact_path="tokenizer")
    mlflow.end_run()

    # ---------------------------------------------------------------------
    # STEP 2 — Fine-tune full model
    # ---------------------------------------------------------------------
    for param in model.bert.parameters():
        param.requires_grad = True

    phase2_args = TrainingArguments(
        output_dir=f"{output_dir}/phase2_finetune",
        learning_rate=float(config["model"]["learning_rate_tuner"]),
        num_train_epochs=int(config["model"]["num_train_epochs_tuner"]),
        per_device_train_batch_size=int(config["model"]["per_device_train_batch_size"]),
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        report_to=["mlflow"],
        load_best_model_at_end=True
    )

    print("Phase 2: Fine-tuning full model...\n")

    with mlflow.start_run(run_name="phase2_finetune"):
        mlflow.log_params({"phase": "fine_tune_all",
                           "task": "diagnosis_group_prediction",
                           "batch_size": config["model"]["per_device_train_batch_size"],
                           "model": config["model"]["pretrained_name"]
                           })

        fine_tuner = Trainer(model=model,
                             args=phase2_args,
                             train_dataset=train_ds,
                             eval_dataset=test_ds,
                             compute_metrics=compute_metrics
                             )

        fine_tuner.train()
        fine_tuner.save_model(f"{output_dir}/phase2_best")

        wrapped_model2, signature2, tmp_dir2 = get_model_signature(model, train_ds, tokenizer)
        mlflow.pytorch.log_model(pytorch_model=wrapped_model2,
                                 name="phase2_model",
                                 signature=signature2,
                                 )
        # Log tokenizer as an artifact
        mlflow.log_artifacts(tmp_dir2, artifact_path="tokenizer")
    mlflow.end_run()

    print("Training complete. Model saved to:", f"{output_dir}/phase2_best")

    fine_tuner.model.to(device)

    return fine_tuner


def main():
    print("transformers version:", transformers.__version__)

    # Load config
    cfg = load_config(config_path)
    model_output_dir = cfg["output"]["model_dir"]
    results_dir = cfg["output"]["results_dir"]
    os.makedirs(model_output_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    device = set_device()

    hosp_tables, icu_tables = data_utils.load_mimic_data(mimic4_path, verbose=False)
    admissions = hosp_tables["admissions"][["hadm_id", "subject_id", "admittime", "dischtime"]]
    diagnoses = hosp_tables["diagnoses_icd"][["hadm_id", "icd_code", "icd_version"]]
    patients = hosp_tables["patients"][["subject_id", "gender", "anchor_age", "anchor_year_group"]]

    # Cohort from downloaded demo version
    cohort = prepare_cohort_local(admissions, diagnoses, patients)

    label_encoder = LabelEncoder()
    cohort["label"] = label_encoder.fit_transform(cohort[cfg["data"]["label_column"]])
    num_labels = len(label_encoder.classes_)  # number of diagnosis groups

    train_df, test_df = train_test_split(
        cohort,
        test_size=cfg["data"]["test_size"],
        random_state=cfg["data"]["random_seed"],
        stratify=cohort["label"],
    )
    train_ds, test_ds, tokenizer = prepare_datasets(device,
                                                    train_df,
                                                    test_df,
                                                    tokenizer_name=cfg["model"]["pretrained_name"],
                                                    max_length=cfg["model"]["max_length"],
                                                    )
    trainer = train_model(device=device,
                          config=cfg,
                          train_ds=train_ds,
                          test_ds=test_ds,
                          num_labels=num_labels,
                          output_dir=model_output_dir
                          )

    # Evaluate
    preds = trainer.predict(test_ds)
    y_true = np.array(test_df["label"])
    y_pred = np.argmax(preds.predictions, axis=1)
    acc = (y_true == y_pred).mean()

    # Log metrics
    mlflow.log_metric("test_accuracy", float(acc))
    mlflow.set_tag("mlflow.runName", "Predictions_on_validation_set")

    # Save predictions
    test_df["predicted_group"] = label_encoder.inverse_transform(y_pred)
    test_df.to_csv(join(results_dir, "poc_predictions.csv"), index=False)
    print(f"\n POC complete. Test Accuracy: {acc:.3f}\n")
    print(test_df[["icd_code", "diagnosis_group", "predicted_group"]].head())

    # Reload model and predict
    # load_model_and_predict(run_id)
    # print_mlflow_metrics(experiment_name=cfg["mlflow"]["experiment_name"])


def load_model_and_predict(run_id: str):
    # Load model and tokenizer
    logged_model_uri = f"runs:/{run_id}/model"
    model = mlflow.pytorch.load_model(logged_model_uri)
    tokenizer = AutoTokenizer.from_pretrained(f"mlruns/{run_id}/artifacts/tokenizer")

    # Predict example
    text = "Patient presents with acute respiratory distress."
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
    with torch.no_grad():
        preds = model(**inputs)
    print(preds)


if __name__ == "__main__":
    main()
