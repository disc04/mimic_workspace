from pathlib import Path
from os.path import join
from zipfile import ZipFile
import pandas as pd
from icdmappings import Mapper
from configuration import mimic_iv_data_sources, vitals_keywords
from utils import med_utils
import re
# pip install icd-mappings


def extract_zip_file(datadir: Path, filename: str,  verbose: bool = False):
    if not Path(join(datadir, filename.replace(".zip",""))).exists():
        with ZipFile(Path(join(datadir, filename)), "r") as zip:
            zip.extractall(datadir)
            if verbose:
                zip.printdir()


def dataframe_from_csv(path: str, compression: any = "gzip", header=0, index_col=0):
    return pd.read_csv(path, compression=compression, header=header, index_col=index_col)


def load_mimic_data(mimic4_path, verbose=False):
    """
    Load MIMIC-IV data files
    """

    hosp_files = ["patients", "admissions", "diagnoses_icd", "d_icd_diagnoses",
                  "labevents", "d_labitems", "services", "transfers", "prescriptions",
                  "procedures_icd", "d_icd_procedures", "emar"]
    icu_files = ["icustays", "chartevents", "d_items", "procedureevents", "inputevents"]

    hosp, icu = {}, {}

    for source, content, result in zip(["hosp", "icu"], [hosp_files, icu_files], [hosp, icu]):
        for filename in content:
            try:
                result[filename] = pd.read_csv(join(mimic4_path, f"{source}/{filename}.csv.gz"),
                                               compression="gzip")
                if verbose:
                    print(f"Loaded {filename}: {len(content[filename])} rows")
            except FileNotFoundError:
                print(f"Warning: {filename}.csv.gz not found")
    return hosp, icu


def extract_admissions(hosp_tables: dict, hadm_ids: int | list | None) -> tuple:
    """
    Defines cohort or multiple admissions for single patient.
    :param hosp_tables: Dictionary of hospital data.
    :param hadm_ids: Admission id. Can be int for single admission, list for multiple admissions,
    or None for all admissions (returns unchanged admissions).
    :return: Filtered admission dataframe according to hadm_id, and list of subjects ids.
    """
    all_admissions = hosp_tables.get("admissions")
    if hadm_ids is None:
        hadm_ids = all_admissions["hadm_id"].unique().tolist()
        return all_admissions, hadm_ids
    else:
        if isinstance(hadm_ids, int):
            hadm_ids = [hadm_ids]
        admissions = all_admissions[all_admissions["hadm_id"].isin(hadm_ids)].copy()
        return admissions, hadm_ids


def extract_admissions_data(hosp_tables: dict, icu_tables: dict, hadm_ids: int | list | None,
                            return_as_cohort:bool)-> dict:
    """
    Extract admission
    :param hosp_tables: Dictionary of hospital data.
    :param icu_tables: Dictionary of icu data.
    :param hadm_ids: Admission id. Can be int for single admission, list for multiple admissions,
    :param return_as_cohort: Return as cohort data. If False, return dictionary by admission_id key.
    or None for all admissions (returns unchanged admissions).
    :return: Dictionary with hadm_ids keys and admission dictionaries as values.
    """

    admissions, hadm_ids = extract_admissions(hosp_tables, hadm_ids)

    # Enrich admissions with demographics
    admissions = admissions.merge(hosp_tables.get("patients"), how="left", on="subject_id")
    hadm_df = pd.DataFrame({"hadm_id": hadm_ids})

    # Extract admissions data
    labs, abnormal_labs = get_labs(hosp_tables, hadm_df)
    prescriptions_medications, emar_medications, infusions_medications = (
        get_medications(hosp_tables, icu_tables, hadm_df))
    admissions_data = {"admission": admissions,
                       "diagnoses": get_diagnoses(hosp_tables, hadm_df),
                       "vitals": get_vitals(icu_tables, hadm_df),
                       "labs": labs,
                       "prescription_medications": prescriptions_medications,
                       "emar_medications": emar_medications,
                       "infusion_medications": infusions_medications,
                       "procedures": get_procedures(hosp_tables, hadm_df),
                       "icu_procedures": get_icu_procedures(icu_tables, hadm_df),
                       "transfers": get_transfers(hosp_tables, hadm_df)}

    if return_as_cohort:
        # data for all admissions in the  hadm_id list
        return admissions_data
    else:
        # return dictionary for each hadm_id
        admissions_by_hadm_id = split_admissions_by_id_list(admissions_data, hadm_df)
        return admissions_by_hadm_id


def split_admissions_by_id_list(admissions_data, hadm_df):
    split = {}
    names = [key for key in admissions_data.keys() if key != "admission"]
    for name in names:
        split[name] = results_dictionary_by_id_list(admissions_data[name],
                                                    "hadm_id", hadm_df["hadm_id"].values.tolist())
    results = {}
    for n, group in admissions_data["admission"].groupby("hadm_id"):
        diagnoses_dict = extract_diagnoses_from_admission(split["diagnoses"][n])
        demographic_features = ["hadm_id", "race", "insurance", "gender",
                                "anchor_age", "dod", "admission_type", "hospital_expire_flag"]
        results[n] = {"hadm_id": n,
                      "subject_id": group["subject_id"].iat[0],
                      "demographics": group[demographic_features],
                      "admittime": group["admittime"].iat[0],
                      "dischtime": group["dischtime"].iat[0],
                      "admission": group.copy(),
                      "vitals": split["vitals"][n],
                      "labs": split["labs"][n],
                      "prescription_medications": split["prescription_medications"][n],
                      "emar_medications": split["emar_medications"][n],
                      "infusion_medications": split["infusion_medications"][n],
                      "procedures": split["procedures"][n],
                      "icu_procedures": split["icu_procedures"][n],
                      "primary_diagnosis": diagnoses_dict["primary_diagnosis"],
                      "diagnoses": diagnoses_dict["diagnoses"],
                      "transfers": split["transfers"][n]}
    return results


def results_dictionary_by_id_list(df, id_column,  id_list):
    """Extracts parts of a dataframe into a dictionary by list of ids"""
    result = {}
    for i in id_list:
        result[i] = df[df[id_column] == i].copy()
    return result


def get_vitals(icu_tables: dict, hadm_df: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(hadm_df, icu_tables.get("icustays", pd.DataFrame()), on="hadm_id",  how="left")
    result = pd.merge(result, icu_tables.get("chartevents", pd.DataFrame()), on="hadm_id", how="left")
    result = pd.merge(result, icu_tables.get("d_items", pd.DataFrame()), on="itemid", how="left")
    # filter by important vital measurements
    result = result[result["label"].str.contains("|".join(vitals_keywords), case=False, na=False)]
    return result


def get_labs(hosp_tables:  dict, hadm_df: pd.DataFrame) -> tuple:
    labs = pd.merge(hadm_df, hosp_tables.get("labevents", pd.DataFrame()), on="hadm_id", how="left")
    labs = pd.merge(labs, hosp_tables.get("d_labitems", pd.DataFrame())[["itemid", "label"]],
                      on="itemid", how="left")
    abnormal_labs = med_utils.get_abnormal_lab_tests(labs)
    return labs, abnormal_labs


def get_medications(hosp_tables: dict, icu_tables: dict, hadm_df: pd.DataFrame) -> tuple:
    prescriptions = pd.merge(hadm_df,  hosp_tables.get("prescriptions", pd.DataFrame()), on="hadm_id", how="left")
    prescriptions["label"] = (prescriptions[["drug", "dose_val_rx", "dose_unit_rx"]]
                            .apply(lambda x: " ".join(x.astype(str)), axis=1))

    emars = pd.merge(hadm_df, hosp_tables.get("emar", pd.DataFrame()).dropna(subset=["medication"]),
                     on="hadm_id", how="left")
    # TODO: filter further by event_text (not administred, stopped...)
    emars = emars[["hadm_id", "charttime", "medication",  "pharmacy_id"]]

    infusions = pd.merge(hadm_df, icu_tables.get("inputevents", pd.DataFrame()), on="hadm_id", how="left")
    infusions = infusions.merge(icu_tables.get("d_items", pd.DataFrame())[["itemid", "label"]], on="itemid", how="left")
    infusion_labels = infusions[["label", "rate", "rateuom"]].apply(lambda x: " ".join(x.astype(str)), axis=1)
    infusions = infusions[["hadm_id", "starttime", "endtime"]]
    infusions["label"] = infusion_labels

    return prescriptions, emars, infusions


def get_procedures(hosp_tables: dict, hadm_df: pd.DataFrame) -> pd.DataFrame:
    """Procedures billed by hospital"""
    result = pd.merge(hadm_df, hosp_tables.get("procedures_icd", pd.DataFrame()), on="hadm_id", how="left")
    result = pd.merge(result, hosp_tables.get("d_icd_procedures", pd.DataFrame()), on=["icd_code", "icd_version"],
                      how="left")
    return result


def get_icu_procedures(icu_tables: dict, hadm_df: pd.DataFrame) -> pd.DataFrame:
    #  procedureevents: procedures documented during the ICU stay
    # d_items: defines concepts recorded in the events table in the ICU module
    result = pd.merge(hadm_df, icu_tables.get("procedureevents", pd.DataFrame()), on="hadm_id", how="left")
    result = pd.merge(result, icu_tables.get("d_items", pd.DataFrame()), on="itemid", how="left")
    labels = result[["label", "value", "valueuom"]].apply(lambda x: " ".join(x.astype(str)), axis=1)
    result = result[["hadm_id", "starttime", "endtime"]]
    result["label"] = labels
    return result


def get_diagnoses(hosp_tables:  dict, hadm_df: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(hadm_df, hosp_tables.get("diagnoses_icd", pd.DataFrame()), on="hadm_id", how="left")
    result = pd.merge(result, hosp_tables.get("d_icd_diagnoses", pd.DataFrame()), on=["icd_code", "icd_version"],
                      how="left")
    return result


def get_transfers(hosp_tables: dict, hadm_df: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(hadm_df, hosp_tables.get("transfers", pd.DataFrame()), on="hadm_id", how="left")
    return result


def add_age_group_counts(df: pd.DataFrame, age_column: str) -> tuple[pd.DataFrame, pd.Series]:
    """
    Add age_group column to dataframe.
    :param df:
    :param age_column:
    :return: df
    """
    df["age_group"] = pd.cut(df[age_column],
                             bins=[0, 18, 30, 50, 65, 80, 100],
                             labels=["<18", "18-29", "30-49", "50-64", "65-79", "80+"])
    age_group_counts = df["age_group"].value_counts().sort_index()
    return df, age_group_counts


def clean_column_name(name, max_len=50):
    name = name.strip().replace(" ", "_").replace("/", "_").replace("-", "_")
    name = re.sub(r"(\.\d)\d+", r"\1", name)  # round dosages
    clean = re.sub(r"_{2,}", "_", name)  # Multiple occurrences
    return f"{clean[:max_len]}"


def date_and_time_to_datetime(df: pd.DataFrame, time_column: str) -> pd.DataFrame:
    df = df.copy()
    if "time" in time_column:
        df = df.dropna(subset=[time_column])
        df[time_column] = pd.to_datetime(df[time_column])
    if "date" in time_column:
        # Convert to datetime and set fixed time to 12:00
        df[time_column] = pd.to_datetime(df[time_column]).dt.normalize() + pd.Timedelta(hours=12)
    return df


def adjust_admittime_by_first_event(admission_dict):
    """
    Adjusts admission time if earlier events in the emergency department
    (e.g., medications, vitals, labs, procedures) start before the recorded admit time.

    Returns the earliest event time if it is earlier than the recorded admission time.
    """
    recorded_admit_time = pd.to_datetime(admission_dict["admittime"])

    event_times = []
    for src in mimic_iv_data_sources:
        df = admission_dict.get(src["name"])
        time_col = src["time_col"] if "time_col" in src.keys() else None
        start_col = src["start_col"] if "start_col" in src.keys() else None
        if df is not None and not df.empty and time_col is not None and time_col in df:
            earliest = pd.to_datetime(df[time_col].min())
            if pd.notna(earliest):
                event_times.append(earliest)
        if df is not None and not df.empty and start_col is not None and start_col in df:
            earliest = pd.to_datetime(df[start_col].min())
            if pd.notna(earliest):
                event_times.append(earliest)

    if not event_times:
        return recorded_admit_time

    earliest_event_time = min(event_times)
    return min(recorded_admit_time, earliest_event_time)


def get_admit_discharge_times(data_dict: dict, adjust_start: bool = True) -> tuple:
    """
    Sometimes in an emergency department events start before recorded admission time.
    Check and adjust admission and discharge times
    :param data_dict:  Dictionary containing "admit_time" and "discharge_time" as pd.Timestamp.
    :param adjust_start: Whether to adjust admission time to the start of the first event.
    :return admit_time: pd.Timestamp, discharge_time : pd.Timestamp, message: str
    """
    admit_time = pd.to_datetime(data_dict["admittime"])
    discharge_time = pd.to_datetime(data_dict["dischtime"])

    if pd.isna(admit_time) or pd.isna(discharge_time) or admit_time >= discharge_time:
        message = "QC failed: Invalid admit_time or discharge_time"
        return admit_time, discharge_time, message

    if adjust_start:
        # Shift admittime to first event.
        admit_time = adjust_admittime_by_first_event(data_dict)

    return admit_time, discharge_time, None


def filter_by_time_window_consistency(df: pd.DataFrame, start_window: pd.Timestamp, end_window: pd.Timestamp,
                                      start_event_col: str, end_event_col: str | None, adjust_start: bool,
                                      adjust_end: bool) -> tuple[pd.DataFrame, any]:
    """
    Events can be continuous or discrete (start_event only, for example: vitals measurements)
    :param df: Dataframe - a dataframe to filter.
    :param start_window: Datetime or date - keeps only events within window.
    :param end_window:  Datetime or date.
    :param start_event_col: Column_name for start event - datetime or date.
    :param end_event_col: Column_name for start event - datetime or date.
    :param adjust_start: bool - Shift start_event to the start_window if event started before start_window.
    :param adjust_end: bool - Shift end_event to the end_window if event started before start_window.
    :return: Filtered dataframe.
    """

    if start_event_col not in df.columns:
        return df, f"QC: failed filter_by_time_window_consistency. Missing start_event column."
    else:
        df = date_and_time_to_datetime(df, start_event_col)
        # Ensure event starts later than window
        valid_start = df[start_event_col] >= start_window
        df = df[valid_start | df[start_event_col].isna()]

        if adjust_start:
            # Shift start_event to start_window if event started before start_window
            df.loc[df[start_event_col] < start_window, start_event_col] = start_window

    if end_event_col is not None and end_event_col not in df.columns:
        return df, f"QC: failed filter_by_time_window_consistency. Missing end_event column."

    elif end_event_col is not None and end_event_col in df.columns:
        df = date_and_time_to_datetime(df, end_event_col)

        # Remove where start later than stop
        valid_times = df[start_event_col] <= df[end_event_col]
        df = df[valid_times | df[end_event_col].isna()]

        # inside window - adjust, but not drop events that started before or ended after.
        # df = df[(df[start_event_col] >= start_window) & (df[start_event_col] <= end_window)]

        if adjust_end:
            # Shift end_event to end_window if event continued past end_window
            df.loc[df[end_event_col] > end_window, end_event_col] = end_window
        return df, None
    else:
        return df, None


def filter_dataframe_by_dictionary(keyword_dict: dict, df: pd.DataFrame, columns_to_search: list) -> pd.DataFrame:
    """
    Extracts row which contain keywords from dictionary in specified columns.
    :param keyword_dict: {category: [keyword1, keyword2, ...], ...}
    :param df: Dataframe to filter.
    :param columns_to_search: Columns in which to search for keywords.
    :return: Filtered dataframe.
    """
    category_items_rows = []
    for category, keywords in keyword_dict.items():
        for keyword in keywords:
            for col in columns_to_search:
                matching_items = df[df[col].str.contains(keyword, case=False, na=False)]
                if not matching_items.empty:
                    matching_items = matching_items.copy()
                    matching_items["category"] = category
                category_items_rows.append(matching_items)

    sorted_df = pd.concat(category_items_rows).drop_duplicates()
    return sorted_df


def convert_icd_codes(codes: list, source_code: str, target_code: str) -> list:
    mapper = Mapper()
    # codes = ["29410", "5362", "NOT_A_CODE", "3669"] # sample usage
    mapped = mapper.map(codes, source=source_code, target=target_code)
    return mapped


def extract_diagnoses_from_admission(diagnoses_df: pd.DataFrame) -> dict:
    """
    Extracts primary diagnosis, creates binary codes for diagnoses
    :param diagnoses_df: Dataframe containing diagnoses data by admission_id
    :return: Dictionary with primary diagnosis and all_diagnoses_list
    """
    primary_diagnosis = diagnoses_df[diagnoses_df["seq_num"] == 1]["long_title"].iat[0]
    all_diagnoses = diagnoses_df["long_title"].unique().tolist()
    diagnoses_dict = {"primary_diagnosis": primary_diagnosis, "diagnoses": all_diagnoses}

    return diagnoses_dict


def add_temperature_celsius(df: pd.DataFrame, fahrenheit_column: str) -> pd.DataFrame:
    """Adds a Temperature_Celsius column based on Temperature_Fahrenheit."""
    if fahrenheit_column not in df.columns:
        raise KeyError(f"DataFrame must contain {fahrenheit_column} column.")
    df["Temperature_Celsius"] = (df[fahrenheit_column] - 32) * 5.0 / 9.0
    return df


def collect_and_save_patient_admission_data(data: dict, results_path: str):
    """Saves patient data to csv"""
    subject_id, hadm_id = data["subject_id"], data["hadm_id"]
    static_df = data["demographics"]
    static_df["subject_id"] = subject_id
    static_df["primary_diagnosis"] = data["primary_diagnosis"]
    static_df["diagnoses"] = ", ".join(data["diagnoses"])
    static_df.to_csv(join(results_path, f"patient_{subject_id}_admission_{hadm_id}_static.csv"),
                     index=False)

    # Dynamic features >  collect all  the time series data
    dynamic_df = data["time_grid"].copy()

    for data_source in ["vitals", "labs", "medications", "procedures", "icu_procedures", "transfers"]:
        if data_source in data and not data[data_source].empty:
            data = data[data_source].drop(["time_point"], axis=1, errors="ignore")
            dynamic_df = pd.merge(dynamic_df, data, how="left", on="hours_from_admission")

    dynamic_df.to_csv(join(results_path, f"patient_{subject_id}_admission_{hadm_id}_dynamic.csv"), index=False)

