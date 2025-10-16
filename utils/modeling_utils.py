import pathlib
from pathlib import Path
from os.path import join
import pandas as pd
import numpy as np
from typing import Any, Tuple, Dict, List
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import torch
from torch import nn
from torchmetrics import Accuracy
import torchvision
from torchvision import transforms
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from mlflow.models import infer_signature
import tempfile
import yaml


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def set_device():
    if torch.cuda.is_available():
        device = "cuda"  # NVIDIA GPU
    elif torch.backends.mps.is_available():
        device = "mps"  # Apple Silicon GPU
    else:
        device = "cpu"  # Default
    print(f"device: {device}")
    return device


def print_setup():
    try:
        assert int(torch.__version__.split(".")[1]) >= 12, "torch version should be 1.12+"
        assert int(torchvision.__version__.split(".")[1]) >= 13, "torchvision version should be 0.13+"
        print(f"torch version: {torch.__version__}")
        print(f"torchvision version: {torchvision.__version__}")
    except:
        print(f"[INFO] torch/torchvision versions not as required, installing nightly versions.")
        # !pip3 install - U torch torchvision torchaudio - -extra - index - url https: // download.pytorch.org / whl / cu113

        print(f"torch version: {torch.__version__}")
        print(f"torchvision version: {torchvision.__version__}")


def save_torch_model(model, target_dir: pathlib.Path, model_name: str):
    """Saves a PyTorch model to a target directory.

    Args:
      model: A target PyTorch model to save.
      target_dir: A directory for saving the model to.
      model_name: A filename for the saved model. Should include
        either ".pth" or ".pt" as the file extension.

    Example usage:
      save_model(model=model_0,
                 target_dir="models",
                 model_name="05_going_modular_tingvgg_model.pth")
    """
    # Create target directory
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # Create model save path
    assert model_name.endswith(".pth") or model_name.endswith(".pt"), "model_name should end with '.pt' or '.pth'"
    model_save_path = Path(join(target_dir, model_name))
    print(f"[INFO] Saving model to: {model_save_path}")
    torch.save(obj=model.state_dict(), f=model_save_path)


def load_torch_model(model, path):
    model.load_state_dict(torch.load(f=path))
    return model


class MedBertWrapper(torch.nn.Module):
    """ A wrapper that takes named numpy arrays (for MLflow)"""

    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask,
                             token_type_ids=token_type_ids)
        return outputs.logits


def get_model_signature(model, train_ds, tokenizer):
    """Creates model_signature (for MLflow)"""
    wrapped_model = MedBertWrapper(model).to("cpu")

    """
    # Option 1: prepare example input
    text = "Patient admitted with pneumonia and sepsis."
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    input_example = {
        "input_ids": inputs["input_ids"].cpu().numpy(),
        "attention_mask": inputs["attention_mask"].cpu().numpy(),
    }
     outputs = wrapped_model(input_example).detach().cpu().numpy()
    signature = infer_signature(input_example, outputs)
    """

    # Option 2: input example from train_ds sample
    sample = next(iter(train_ds))
    input_example = {
        "input_ids": sample["input_ids"].unsqueeze(0).cpu().numpy(),
        "attention_mask": sample["attention_mask"].unsqueeze(0).cpu().numpy()
    }
    with torch.no_grad():
        outputs = model(**{k: torch.tensor(v) for k, v in input_example.items()})
        output_array = outputs.logits.detach().cpu().numpy()

    signature = infer_signature(input_example, output_array)

    # Save tokenizer temporarily (so MLflow can log it too)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tokenizer.save_pretrained(tmp_dir)
    return wrapped_model, signature, tmp_dir


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="weighted"),
        "precision": precision_score(labels, preds, average="weighted"),
        "recall": recall_score(labels, preds, average="weighted"),
    }


def print_mlflow_metrics(experiment_name):
    from mlflow import MlflowClient

    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    for run in client.search_runs(experiment.experiment_id):
        print(run.info.run_name)
        print(run.data.metrics)

"""


def plot_predictions(train_data,
                     train_labels,
                     test_data,
                     test_labels,
                     predictions=None):

    #Plots training data, test data and compares predictions.

    plt.figure(figsize=(10, 7))
    plt.scatter(train_data, train_labels, c="b", s=4, label="Training data")
    plt.scatter(test_data, test_labels, c="g", s=4, label="Testing data")

    if predictions is not None:
        plt.scatter(test_data, predictions, c="r", s=4, label="Predictions")

    plt.legend(prop={"size": 14})
    plt.show()
    plt.close()


def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()  # torch.eq() calculates where two tensors are equal
    acc = (correct / len(y_pred)) * 100
    return acc


def get_tensors_from_df(df: pd.DataFrame, target_column: str = 'label'):
    features = [c for c in df.columns if c != target_column]
    X = torch.from_numpy(df[features].to_numpy()).type(torch.float)
    y = torch.from_numpy(df[[target_column]].to_numpy()).type(torch.float)
    return X, y


def torch_predict_samples(model: torch.nn.Module, data: list, device: torch.device):
    pred_probs = []
    model.eval()
    with torch.inference_mode():
        for sample in data:
            # Add an extra dimension and send sample to device
            sample = torch.unsqueeze(sample, dim=0).to(device)
            pred_logit = model(sample)
            # Get sample probability
            pred_prob = torch.softmax(pred_logit.squeeze(), dim=0)
            # in this case we have a batch size of 1, so can perform on dim=0

            pred_probs.append(pred_prob.cpu())

    return torch.stack(pred_probs)  # turn list into a tensor
    
"""