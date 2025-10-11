# Trainer setup for MedBERT fine-tuning.

from transformers import BertForSequenceClassification, Trainer, TrainingArguments


def create_trainer(train_ds,
                   test_ds,
                   num_labels,
                   learning_rate,
                   batch_size,
                   num_train_epochs,
                   weight_decay,
                   output_dir="./models/medbert_poc"):

    model = BertForSequenceClassification.from_pretrained(
        "emilyalsentzer/Bio_ClinicalBERT", num_labels=num_labels
    )

    training_args = TrainingArguments(
        # evaluation_strategy="epoch",
        logging_strategy="epoch",
        save_strategy="no",
        learning_rate=float(learning_rate),
        per_device_train_batch_size=batch_size,
        num_train_epochs=num_train_epochs,
        weight_decay=weight_decay,
        report_to="none",
        output_dir=output_dir,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=test_ds,
    )

    return trainer
