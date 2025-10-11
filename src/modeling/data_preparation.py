# Data preparation for MedBERT POC training.

import pandas as pd
from utils.data_utils import convert_icd_codes


def prepare_cohort_local(admissions: pd.DataFrame, diagnoses: pd.DataFrame, patients: pd.DataFrame) -> pd.DataFrame:
    """
    Merges MIMIC dataframes and create diagnosis sequence text per admission.
    Applies ICD_9 tp ICD_10 mapping for rows with icd_version == 9.
    Returns a cohort DataFrame.
    """

    # ICD-9 to ICD-10 mapping
    mask_icd9 = diagnoses["icd_version"] == 9
    if mask_icd9.any():
        icd9_codes = diagnoses.loc[mask_icd9, "icd_code"].tolist()
        mapped_codes = convert_icd_codes(icd9_codes, source_code="icd9", target_code="icd10")
        diagnoses.loc[mask_icd9, "icd_code"] = mapped_codes
        diagnoses.loc[mask_icd9, "icd_version"] = 10

    # Build diagnosis code sequences per admission
    cohort = (
        diagnoses.groupby("hadm_id")["icd_code"]
        .apply(lambda x: " ".join(sorted(set(x.astype(str)))))
        .reset_index()
    )

    cohort = cohort.merge(admissions[["hadm_id", "subject_id"]], on="hadm_id", how="left")
    cohort = cohort.merge(patients[["subject_id", "gender", "anchor_age"]], on="subject_id", how="left")

    # Dummy label generation
    def assign_group(icd_text):
        if any(code.startswith("I") for code in icd_text.split()):
            return "Cardiac"
        elif any(code.startswith("J") for code in icd_text.split()):
            return "Respiratory"
        else:
            return "Other"

    cohort["diagnosis_group"] = cohort["icd_code"].apply(assign_group)
    return cohort
