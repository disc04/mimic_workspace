from pathlib import Path
from os.path import join
from utils import data_utils, local_cohort_plotting_utils
from utils import local_cohort_analysis_utils
from config.project_config import severity_scores_dictionary, drug_categories_dictionary
from config.project_config import DATA_PATH

mimic4_path = join(Path(__file__).parent.parent.parent,
                   DATA_PATH,
                   "mimic_iv-clinical-database-demo-2.2")
results_path = join(Path(__file__).parent.parent.parent, "results")


def analyze_multiple_admissions(hosp_tables: dict,
                                icu_tables: dict,
                                hadm_ids: list | None,
                                results_path: str = results_path) -> dict:
    """
    Analyze single patient admission with time-series binning and visualization.
    :param hosp_tables: Dictionary containing hospital tables.
    :param icu_tables: Dictionary containing ICU tables.
    :param hadm_ids: list or None  Hospital admission IDs.
    :param results_path: str Folder to save results.
    :returns: Dictionary containing patient admission analysis and time-series data.
    """

    results_dict = data_utils.extract_admissions_data(hosp_tables=hosp_tables,
                                                      icu_tables=icu_tables,
                                                      hadm_ids=hadm_ids,
                                                      return_as_cohort=True)

    local_cohort_analysis_utils.run_demographics_analysis(admissions=results_dict["admission"],
                                                          icu_stays=results_dict["vitals"],
                                                          diagnoses=results_dict["diagnoses"],
                                                          results_path=results_path)
    local_cohort_plotting_utils.plot_services_analysis(hosp_tables,
                                                       join(results_path, "Hospital_services_analysis.png"))

    local_cohort_analysis_utils.run_admission_readmission_analysis(results_dict["admission"],
                                                                   results_path)

    local_cohort_analysis_utils.run_severity_mortality_analysis(results_dict["admission"],
                                                                diagnoses=hosp_tables["diagnoses_icd"],
                                                                icu_stays=results_dict["vitals"],
                                                                icd_desc=hosp_tables["d_icd_diagnoses"],
                                                                chartevents=icu_tables["chartevents"],
                                                                d_items=icu_tables["d_items"],
                                                                severity_scores=severity_scores_dictionary,
                                                                results_path=results_path)

    local_cohort_analysis_utils.run_lab_tests_analysis(results_dict["labs"],
                                                       results_path)
    local_cohort_analysis_utils.run_prescriptions_analysis(results_dict["prescription_medications"],
                                                           drug_categories_dictionary,
                                                           results_path)
    local_cohort_analysis_utils.run_procedures_analysis(results_dict["procedures"],
                                                        results_dict["icu_procedures"],
                                                        results_path,
                                                        verbose=True)

    return results_dict


def main():
    # Load tables
    hosp_tables, icu_tables = data_utils.load_mimic_data(mimic4_path, verbose=False)
    hadm_ids = [24698912, 29974575]
    results = analyze_multiple_admissions(hosp_tables,
                                          icu_tables,
                                          hadm_ids=None,
                                          results_path=results_path)


if __name__ == "__main__":
    main()
