import pandas as pd
from os.path import join
from utils import data_utils, cohort_plotting_utils


def run_demographics_analysis(admissions, icu_stays, diagnoses, results_path):
    print("Analysing demographics")
    # Create demographic summaries for plotting
    for col in ["admittime", "dischtime", "deathtime"]:
        admissions[col] = pd.to_datetime(admissions[col].copy())
    # Calculate length of stay
    admissions["los_days"] = (admissions["dischtime"] - admissions["admittime"]).dt.total_seconds() / (24 * 3600)
    admissions, _ = data_utils.add_age_group_counts(admissions, "anchor_age")
    admissions = clean_etnicity_data(admissions)

    # ICU length of stay is already provided as "los" in days
    icu_stays = icu_stays.drop_duplicates(subset=["hadm_id"])[["hadm_id", "intime", "outtime", "los"]]
    for col in ["intime", "outtime"]:
       icu_stays = data_utils.date_and_time_to_datetime(icu_stays, col)

    demography = admissions[["hadm_id", "subject_id", "anchor_age", "gender", "race", "insurance",
                            "admission_type", "hospital_expire_flag"]]
    icu_stays = icu_stays.merge(demography, on="hadm_id", how="left")
    icu_stays, _ = data_utils.add_age_group_counts(icu_stays, "anchor_age")
    icu_stays = clean_etnicity_data(icu_stays)

    # Write summary demographics into a text file
    generate_demographic_summary(admissions, icu_stays, join(results_path, "Demographics_summary.txt"))
    if len(admissions) > 5 and len(icu_stays) > 5:
        # Plot demographics
        data = [admissions, icu_stays]
        prefixes = ["Hospital", "ICU"]

        for df, prefix in zip(data, prefixes):
            cohort_plotting_utils.plot_demographics(df, prefix,
                                                    join(results_path, f"{prefix}_demographics_analysis.png"))
            cohort_plotting_utils.plot_length_of_stay(df, prefix,
                                                      join(results_path, f"{prefix}_los_analysis.png"))
            cohort_plotting_utils.plot_clinical_conditions_analysis(diagnoses,
                                                                    join(results_path,
                                                                         "Hospital_clinical_conditions_analysis.png"))

        print("Completed demographics analysis")


def run_admission_readmission_analysis(admissions, results_path):
    print("Analyzing admission-readmission")
    admissions_data = analyze_admission_types(admissions)
    cohort_plotting_utils.plot_admission_types_analysis(admissions_data,
                                                        join(results_path, "Admission_types_analysis.png"))

    # Readmissions analysis
    admissions, readmissions_df, patients_readmissions = analyze_readmissions(admissions)
    cohort_plotting_utils.plot_readmission_analysis(readmissions_df,
                                                    patients_readmissions,
                                                    join(results_path, "Readmission_analysis.png"))
    print("Completed admission-readmision analysis")


def clean_etnicity_data(df: pd.DataFrame) -> pd.DataFrame:
    if "race" in df.columns:
        df["race_clean"] = df["race"].fillna("UNKNOWN")
        # Group less common ethnicities
        race_counts = df["race_clean"].value_counts()
        top_races = race_counts.head(8).index
        df["race_grouped"] = df["race_clean"].apply(
            lambda x: x if x in top_races else "OTHER"
        )
    return df


def run_severity_mortality_analysis(admissions, diagnoses, icu_stays, icd_desc, chartevents, d_items,
                                    severity_scores, results_path):
    print("Analyzing severity scores and mortality by condition")
    severity_scores = analyze_severity_scores(chartevents,
                                              d_items,
                                              severity_scores=severity_scores)

    cohort_plotting_utils.plot_severity_scores(severity_scores,
                                               results_path=results_path,
                                               filename="severity_score.png")

    hosp_mortality, icu_mortality, mortality_df = analyze_mortality_by_condition(admissions=admissions,
                                                                                 diagnoses=diagnoses,
                                                                                 icu_stays=icu_stays,
                                                                                 icd_desc=icd_desc)

    cohort_plotting_utils.plot_mortality_analysis(hosp_mortality, icu_mortality,
                                                  join(results_path, "Mortality_analysis.png"))
    print("Completed mortality analysis")


def run_lab_tests_analysis(labs, results_path):
    print("Analysing lab tests")
    test_frequency, category_frequency, tests_per_patient, tests_per_admission = (
        analyze_lab_tests_frequency(labs))

    cohort_plotting_utils.plot_lab_tests_frequency(test_frequency,
                                                   tests_per_admission,
                                                   join(results_path, "Lab_test_frequency_analysis.png"))

    print("Completed lab tests analysis")


def run_prescriptions_analysis(prescriptions, drug_categories_dictionary, results_path):
    print("Analysing medication")
    medications_results = analyze_prescribed_medications(prescriptions,
                                                         drug_categories_dictionary,
                                                         verbose=False)
    (drug_frequency, category_frequency, drug_type_frequency, route_frequency,
     prescriptions_per_patient, unique_drugs_per_patient, prescriptions_per_admission,
     prescriptions) = medications_results
    cohort_plotting_utils.plot_prescribed_medications(drug_frequency,
                                                      category_frequency,
                                                      drug_type_frequency,
                                                      route_frequency, prescriptions_per_patient,
                                                      unique_drugs_per_patient,
                                                      join(results_path, "Medication_analysis.png"))
    print("Completed medication analysis")


def run_procedures_analysis(procedures, icu_procedures, results_path, verbose=True):
    print("Analysing procedures")
    hosp_procedures, icu_procedures = (analyze_procedures_frequency(procedures,
                                                                    icu_procedures,
                                                                    verbose=verbose))
    cohort_plotting_utils.plot_procedures(hosp_procedures, icu_procedures,
                                          join(results_path, "Procedures.png"))
    print("Completed procedures analysis")


def generate_demographic_summary(hosp_df: pd.DataFrame, icu_df: pd.DataFrame, save_path: str) -> None:
    """
    :param hosp_df: Hospital admissions df.
    :param icu_df: ICU stays df.
    :param save_path: Path to save summary statistics.
    """
    data = [hosp_df, icu_df]
    prefix = ["Hospital", "ICU"]

    with open(save_path, "w") as f:
        for df, prefix in zip(data, prefix):
            f.write(f"\n\n{prefix} DEMOGRAPHICS SUMMARY\n")
            f.write("-" * 40)
            f.write(f"\nTotal {prefix} Admissions: {len(df):,}\n")

            f.write(f"Unique Patients: {df['subject_id'].nunique():,}\n")
            unique_patients = df.drop_duplicates(subset=["subject_id"])
            f.write("\n\nGender Distribution:\n")
            gender_dist = unique_patients["gender"].value_counts()
            for gender, count in gender_dist.items():
                f.write(f"  {gender}: {count:,} ({count / len(unique_patients) * 100:.1f}%)\n")
            f.write("\n\nEthnicity Distribution:\n")
            race_dist = unique_patients["race_grouped"].value_counts()#.head(5)
            for race, count in race_dist.items():
                f.write(f"  {race}: {count:,} ({count / len(unique_patients) * 100:.1f}%)\n")

            f.write(f"\nAge - Mean: {df['anchor_age'].mean():.1f}, Median: {df['anchor_age'].median():.1f}")
            f.write(f"\nAge range: {df['anchor_age'].min()} - {df['anchor_age'].max()} years\n")
            _, age_group_counts = data_utils.add_age_group_counts(df=df, age_column="anchor_age")
            for age_group, count in age_group_counts.items():
                if len(df) > 0:
                    percentage = (count / len(df)) * 100
                else:
                    percentage = 0
                f.write(f"{age_group}: {count} patients ({percentage:.1f}%)\n")
            if "los_days" in df.columns:
                f.write(
                    f"\n\n{prefix} Length of Stay - Mean: {df['los_days'].mean():.1f} days, Median: {df['los_days'].median():.1f} days")
            if "los" in df.columns:
                f.write(
                    f"\n\n{prefix} Length of Stay - Mean: {df['los'].mean():.1f} days, Median: {df['los'].median():.1f} days")
            if "first_careunit" in df.columns:
                f.write("\n\nTop ICU Types:\n")
                icu_types = df["first_careunit"].value_counts().head(5)
                for icu_type, count in icu_types.items():
                    f.write(f"  {icu_type}: {count:,} ({count / len(icu_df) * 100:.1f}%)\n")

            mortality_rate = df["hospital_expire_flag"].mean() * 100
            f.write(f"\n\n{prefix} Mortality Rate: {mortality_rate:.1f}%\n")


def analyze_admission_types(admissions: pd.DataFrame) -> pd.DataFrame:
    """Analyze emergency vs elective admissions
    :param admissions: Admissions dataframe.
    :return: Admissions summary.
    """
    for col in ["admittime", "dischtime"]:
        admissions = data_utils.date_and_time_to_datetime(admissions, col)

    # Calculate length of stay
    admissions["los_hours"] = (admissions["dischtime"] - admissions["admittime"]).dt.total_seconds() / 3600
    admissions["los_days"] = admissions["los_hours"]/24

    # Categorize admission types into Emergency vs Elective
    emergency_types = ["DIRECT EMER.", "EW EMER.", "URGENT"]
    elective_types = ["ELECTIVE", "SURGICAL SAME DAY ADMISSION"]
    observation_types =["AMBULATORY OBSERVATION", "EU OBSERVATION",
                        "OBSERVATION ADMIT",  "DIRECT OBSERVATION"]

    admissions["admission_category"] = admissions["admission_type"].apply(
        lambda x: "Emergency" if x in emergency_types else
        "Elective" if x in elective_types else "Observation"
    )
    return admissions


def analyze_readmissions(admissions: pd.DataFrame) -> tuple:
    """Analyze patients with multiple visits and readmission patterns.
    :param admissions: Admissions dataframe.
    :return: Tuple of admission patterns and readmission patterns.
    """
    for col in ["admittime", "dischtime"]:
        admissions = data_utils.date_and_time_to_datetime(admissions, col)
    admissions = admissions.sort_values(["subject_id", "admittime"])

    # Calculate readmission metrics
    readmission_data = []

    for subject_id in admissions["subject_id"].unique():
        patient_admissions = admissions[admissions["subject_id"] == subject_id].copy()

        if len(patient_admissions) > 1:
            patient_admissions = patient_admissions.reset_index(drop=True)

            for i in range(1, len(patient_admissions)):
                prev_discharge = patient_admissions.loc[i - 1, "dischtime"]
                curr_admit = patient_admissions.loc[i, "admittime"]

                if pd.notna(prev_discharge):
                    days_between = (curr_admit - prev_discharge).total_seconds() / (24 * 3600)

                    readmission_data.append({
                        "subject_id": subject_id,
                        "readmission_number": i + 1,
                        "days_between_admissions": days_between,
                        "prev_hadm_id": patient_admissions.loc[i - 1, "hadm_id"],
                        "curr_hadm_id": patient_admissions.loc[i, "hadm_id"],
                        "is_30_day_readmission": days_between <= 30,
                        "is_90_day_readmission": days_between <= 90
                    })

    readmissions_df = pd.DataFrame(readmission_data)

    # Calculate patient-level readmission statistics
    patient_readmissions = admissions.groupby("subject_id").agg({
        "hadm_id": "count",
        "admittime": ["min", "max"],
        "hospital_expire_flag": "max"  # If patient died in any admission
    }).round(2)

    patient_readmissions.columns = ["total_admissions", "first_admission", "last_admission", "ever_died"]
    patient_readmissions["has_readmissions"] = patient_readmissions["total_admissions"] > 1

    return admissions, readmissions_df, patient_readmissions


def analyze_severity_scores(chartevents: pd.DataFrame, d_items: pd.DataFrame, severity_scores: dict) \
        -> pd.DataFrame | None:
    """Analyze GSD, SOFA, and SAPS-II severity scores
    :param chartevents: Admission events dataframe.
    :param d_items: Events descriptions.
    :param severity_scores: Dictionary with severity scores keywords.
    :return: Severity scores dataframe.
    """

    # Common severity score item IDs (these may vary by MIMIC version)
    severity_items_df = data_utils.filter_dataframe_by_dictionary(keyword_dict=severity_scores,
                                                       df=d_items,
                                                     columns_to_search=["label", "abbreviation"])
    # Merge with events
    if not severity_items_df.empty:
        severity_events = severity_items_df.merge(chartevents, how="left", on="itemid")
        severity_events["valuenum"] = pd.to_numeric(severity_events["valuenum"], errors="coerce")
        severity_events = severity_events.dropna(subset=["valuenum"])
        return severity_events
    else:
        print("No severity score data found with common item labels")
        return None


def analyze_mortality_by_condition(admissions: pd.DataFrame, diagnoses: pd.DataFrame,
                                   icu_stays: pd.DataFrame, icd_desc: pd.DataFrame) -> tuple:
    """Analyze in-hospital and ICU mortality rates by condition.
    :param admissions: Admissions dataframe.
    :param diagnoses: Diagnoses dataframe.
    :param icu_stays: ICU stays dataframe.
    :param icd_desc: Descriptors dataframe.
    :returns: Mortality rates summary.
    """
    # Get primary diagnoses with mortality outcomes
    primary_diagnoses = diagnoses[diagnoses["seq_num"] == 1]
    mortality_df = admissions[["hadm_id", "hospital_expire_flag", "deathtime"]].merge(primary_diagnoses,
                                           on="hadm_id", how="left")

    # Add diagnosis descriptions and calculate mortality rates by diagnosis
    mortality_df = mortality_df.merge(icd_desc, on=["icd_code", "icd_version"], how="left")
    hosp_mortality= mortality_df.groupby("long_title").agg({"hospital_expire_flag": ["count", "sum"],
                                                                     "hadm_id": "count"}).round(3)

    hosp_mortality.columns = ["total_cases", "deaths", "total_admissions"]
    hosp_mortality["mortality_rate"] = (hosp_mortality["deaths"] /
                                                hosp_mortality["total_cases"] * 100)

    # TODO: consider to filter significant cases with larger datasets
    # Filter for diagnoses with at least 10 cases for statistical significance
    # hosp_mortality = hosp_mortality[hosp_mortality["total_cases"] >= 5]

    # ICU mortality - merge ICU stays with admissions and diagnoses
    icu_with_diagnosis = icu_stays.merge(admissions[["hadm_id", "hospital_expire_flag"]],
                                            on="hadm_id", how="left")
    icu_with_diagnosis = icu_with_diagnosis.merge(primary_diagnoses, on="hadm_id", how="left")
    # merge with diagnosis_description
    icu_with_diagnosis = icu_with_diagnosis.merge(icd_desc, on=["icd_code", "icd_version"], how="left")
    icu_mortality = icu_with_diagnosis.groupby("long_title").agg({"hospital_expire_flag": ["count", "sum"]
                                                                  }).round(3)

    icu_mortality.columns = ["icu_total_cases", "icu_deaths"]
    icu_mortality["icu_mortality_rate"] = (icu_mortality["icu_deaths"] /
                                               icu_mortality["icu_total_cases"] * 100)
    # TODO: consider to filter significant cases with larger datasets
    # icu_mortality = icu_mortality[icu_mortality["icu_total_cases"] >= 5]

    return hosp_mortality, icu_mortality, mortality_df


def analyze_lab_tests_frequency(labs: pd.DataFrame) -> tuple:
    """
    Analyze laboratory test frequency: Most commonly ordered tests
    :param labs: DataFrame with laboratory tests.
    :returns: Lab test frequency analysis results.
    """
    # Calculate test frequency
    test_frequency = labs.groupby(["itemid", "label"]).size().reset_index(name="test_count")
    test_frequency = test_frequency.sort_values("test_count", ascending=False)
    category_frequency = labs.groupby("label").size().sort_values(ascending=False)
    # Calculate tests per patient
    tests_per_patient = labs.groupby("subject_id").size()
    # Calculate tests per admission
    if "hadm_id" in labs.columns:
        tests_per_admission = labs.groupby("hadm_id").size()
    else:
        tests_per_admission = None

    return test_frequency, category_frequency, tests_per_patient, tests_per_admission


def analyze_prescribed_medications(prescriptions: pd.DataFrame, drug_categories: dict,
                                   verbose: bool=True) -> tuple:
    """
    Analyze most prescribed medications: Drug categories and specific medications
    :param prescriptions: Dataframe with prescribed medications.
    :param drug_categories: Dictionary of grug categories.
    :param verbose: Print summary of prescribed medications.
    :returns: Medications frequencies results.
    """
    prescriptions["drug_clean"] = prescriptions["drug"].str.upper().str.strip()

    # Filter prescriptions by drug dictionary
    prescriptions = data_utils.filter_dataframe_by_dictionary(keyword_dict=drug_categories,
                                                   df=prescriptions, columns_to_search=["drug_clean"])

    # Analyze prescription frequency
    drug_frequency = prescriptions["drug_clean"].value_counts()
    category_frequency = prescriptions["category"].value_counts()

    # Analyze by drug type
    drug_type_frequency = prescriptions["drug_type"].value_counts() if "drug_type" in prescriptions.columns else None

    # Analyze prescription patterns per patient
    prescriptions_per_patient = prescriptions.groupby("subject_id").size()
    unique_drugs_per_patient = prescriptions.groupby("subject_id")["drug_clean"].nunique()

    # Analyze prescription patterns per admission
    prescriptions_per_admission = prescriptions.groupby(
        "hadm_id").size() if "hadm_id" in prescriptions.columns else None

    # Route of administration analysis
    route_frequency = prescriptions["route"].value_counts() if "route" in prescriptions.columns else None

    if verbose:
        print(f"Medication Analysis:")
        print(f"  Total prescriptions: {len(prescriptions):,}")
        print(f"  Unique medications: {drug_frequency.nunique():,}")
        print(f"  Most prescribed: {drug_frequency.index[0]} ({drug_frequency.iloc[0]:,} times)")
        print(f"  Most common category: {category_frequency.index[0]} ({category_frequency.iloc[0]:,} prescriptions)")

    return (drug_frequency, category_frequency, drug_type_frequency, route_frequency, prescriptions_per_patient,
            unique_drugs_per_patient, prescriptions_per_admission, prescriptions)


def analyze_procedures_frequency(procedures: pd.DataFrame, icu_procedures:pd.DataFrame,
                                 verbose: bool=True) -> tuple:
    """
    Analyze procedure frequency: Common interventions and procedures
    :param procedures: Hospital procedures df.
    :param icu_procedures: ICU procedures df.
    :param verbose: bool: Print summary.
    :returns: Summary dictionaries.
    """
    
    # Analyze procedure frequency
    hosp_procedures_results = {"procedure_frequency": procedures["long_title"].value_counts(),
                               "icd_version_dist": procedures["icd_version"].value_counts(),
                               "procedures_per_patient": procedures.groupby("subject_id").size(),
                               "procedures_per_admission": procedures.groupby("hadm_id").size(),
                                "total_procedures": len(procedures)}

    # Analyze ICU procedures
    icu_procedures_results = {"procedure_frequency": icu_procedures["label"].value_counts(),
                              "procedures_per_stay": icu_procedures.groupby("hadm_id").size(),
                              "total_icu_procedures": len(icu_procedures)}
    if verbose:
        print(f"Procedure Frequency Analysis Complete:")
        print(f"  Total ICD procedures: {hosp_procedures_results['total_procedures']:,}")
        print(f"  Most common ICD procedure: {hosp_procedures_results['procedure_frequency'].index[0]}")
        print(f"  Total ICU procedures: {icu_procedures_results['total_icu_procedures']:,}")
        print(f"  Most common ICU procedure: {icu_procedures_results['procedure_frequency'].index[0]}")

    return hosp_procedures_results, icu_procedures_results
