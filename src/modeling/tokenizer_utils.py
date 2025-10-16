# Tokenization and dataset preparation utilities for MedBERT training.

from transformers import BertTokenizerFast
from datasets import Dataset


def prepare_datasets(device, train_df, test_df, tokenizer_name="emilyalsentzer/Bio_ClinicalBERT", max_length=64):
    tokenizer = BertTokenizerFast.from_pretrained(tokenizer_name)

    def tokenize(batch):
        return tokenizer(
            batch["icd_code"],
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )

    train_ds = Dataset.from_pandas(train_df[["icd_code", "label"]])
    test_ds = Dataset.from_pandas(test_df[["icd_code", "label"]])

    train_ds = train_ds.map(tokenize, batched=True)
    test_ds = test_ds.map(tokenize, batched=True)

    train_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"], device=device)
    test_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"], device=device)
    return train_ds, test_ds, tokenizer
