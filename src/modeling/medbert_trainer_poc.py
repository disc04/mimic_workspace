# Fine-tunes Med-BERT (Bio_ClinicalBERT) on diagnosis group prediction using local mimic-iv demo subset

# Load local csv to DataFrames (admissions, diagnoses_icd, patients)
# Merge into a cohort table
# Group ICD codes by subject_id or hadm_id
# Create text-like token sequences (e.g. “I10 E11 J18”)
# Fine-tune a BERT model (from HuggingFace) for diagnosis group prediction
# Evaluates with accuracy and prints sample predictions

# pip install transformers[torch]` or `pip install 'accelerate>=0.26.0'`
from os.path import join
import yaml
from config.project_configuration import DATA_PATH, CONFIG_PATH
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from utils import data_utils
from data_preparation import prepare_cohort_local
from tokenizer_utils import prepare_datasets
from trainer_utils import create_trainer

mimic4_path = join(DATA_PATH, "mimic-iv-clinical-database-demo-2.2")
raw_data_path = join(DATA_PATH, "raw")
config_path = join(CONFIG_PATH, "medbert_poc.yaml")


def load_config(config_path: str):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# TODO in assign_group Replace with real target labels!


def main(config_path):
    hosp_tables, icu_tables = data_utils.load_mimic_data(mimic4_path, verbose=False)
    admissions = hosp_tables["admissions"][["hadm_id", "subject_id", "admittime", "dischtime"]]
    diagnoses = hosp_tables["diagnoses_icd"][["hadm_id", "icd_code", "icd_version"]]
    patients = hosp_tables["patients"][["subject_id", "gender", "anchor_age", "anchor_year_group"]]

    # Cohort from downloaded demo version
    cohort = prepare_cohort_local(admissions, diagnoses, patients)

    # Encode labels and split
    label_encoder = LabelEncoder()
    cohort["label"] = label_encoder.fit_transform(cohort["diagnosis_group"])

    train_df, test_df = train_test_split(
        cohort, test_size=0.2, random_state=1, stratify=cohort["label"])

    # Tokenize
    train_ds, test_ds, tokenizer = prepare_datasets(train_df, test_df)

    # Trainer and Model
    cfg = load_config(config_path)
    trainer = create_trainer(
        train_ds=train_ds,
        test_ds=test_ds,
        num_labels=len(label_encoder.classes_),
        output_dir=cfg["output"]["model_dir"],
        learning_rate=cfg["model"]["learning_rate"],
        batch_size=cfg["model"]["batch_size"],
        num_train_epochs=cfg["model"]["num_train_epochs"],
        weight_decay=cfg["model"]["weight_decay"],
    )
    trainer.train()

    # Evaluate
    preds = trainer.predict(test_ds)
    y_true = np.array(test_df["label"])
    y_pred = np.argmax(preds.predictions, axis=1)
    acc = (y_true == y_pred).mean()

    print(f"\n POC complete. Test Accuracy: {acc:.3f}\n")

    test_df["predicted_group"] = label_encoder.inverse_transform(y_pred)
    print(test_df[["icd_code", "diagnosis_group", "predicted_group"]].head())


if __name__ == "__main__":
    main(config_path)
