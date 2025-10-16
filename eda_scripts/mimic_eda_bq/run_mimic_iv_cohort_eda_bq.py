from os.path import join
from pathlib import Path
from utils.bq_utils import get_bq_client, extract_admissions_data_bq
from utils import data_utils, local_cohort_analysis_utils, local_cohort_plotting_utils, bq_utils
from config.project_config import DATA_PATH, drug_categories_dictionary

mimic4_path = join(Path(__file__).parent.parent.parent,
                   DATA_PATH,
                   "mimic-iv-clinical-database-demo-2.2")
results_path = join(Path(__file__).parent.parent.parent, "results")


# TODO rewrite cohort_analysis_utils.run_severity_mortality_analysis for BigQuery


def analyze_multiple_admissions_bq(project_id: str,
                                   dataset_id: str,
                                   hadm_ids: list | None,
                                   results_path: str = results_path) -> dict:
    """
    Analyze multiple admission.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param hadm_ids: list of hospital admission IDs, None for all hospital admissions.
    :param results_path: str Folder to save results.
    :returns: Dictionary containing patient admission analysis and time-series data.
    """

    # Initialize the client
    client = get_bq_client(project_id)

    results_dict = extract_admissions_data_bq(client,
                                              project_id,
                                              dataset_id,
                                              hadm_ids,
                                              return_as_cohort=True)

    local_cohort_analysis_utils.run_demographics_analysis(admissions=results_dict["admission"],
                                                          icu_stays=results_dict["vitals"],
                                                          diagnoses=results_dict["diagnoses"],
                                                          results_path=results_path)

    local_cohort_analysis_utils.run_admission_readmission_analysis(results_dict["admission"],
                                                                   results_path)

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


def analyze_services(client,
                     project_id,
                     dataset_id, ):
    """For total hospital services."""
    services = bq_utils.get_services(client, project_id, dataset_id)
    local_cohort_plotting_utils.plot_services_analysis(services,
                                                       join(results_path, "Hospital_services_analysis.png"))


def main():
    # Load tables
    hosp_tables, icu_tables = data_utils.load_mimic_data(mimic4_path, verbose=False)
    project_id = "mimic_eda_local-project"
    dataset_id = "mimic_iv"
    hadm_ids = [24698912, 29974575]

    results = analyze_multiple_admissions_bq(project_id,
                                             dataset_id,
                                             hadm_ids,
                                             results_path=results_path)


if __name__ == '__main__':
    main()
