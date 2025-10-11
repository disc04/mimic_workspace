from os.path import join
from pathlib import Path
from utils.bq_utils import get_bq_client, extract_admissions_data_bq
from utils import data_utils, local_timeseries_utils
from config.project_configuration import DATA_PATH

mimic4_path = join(Path(__file__).parent.parent.parent,
                   DATA_PATH,
                   "mimic-iv-clinical-database-demo-2.2")
results_path = join(Path(__file__).parent.parent.parent, "results")

# TODO build timeseries utils in BigQuery, currently use local timeseries_utils


def analyze_single_admission_bq(project_id: str,
                                dataset_id: str,
                                hadm_id: int,
                                time_resolution_hours: int = 1,
                                observation_window_hours: int | None = None,
                                save_csv: bool = True,
                                results_path: str = results_path) -> dict:
    """
    Analyze single patient admission with time-series binning and visualization.
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_id: target admission id.
    :param time_resolution_hours: Time resolution for binning (e.g., 1 for hourly, 0.5 for 30min).
    :param observation_window_hours: Max hours to analyze (None for full stay).
    :param save_csv: Whether to save patients tables to csv files.
    :param results_path: Folder to save results.
    :returns: Dictionary containing patient admission analysis and time-series data.
    """

    # Initialize the client
    client = get_bq_client(project_id)

    results_dict = extract_admissions_data_bq(client,
                                              project_id,
                                              dataset_id,
                                              hadm_id,
                                              return_as_cohort=False)
    results = results_dict[hadm_id]

    ts_results, messages = local_timeseries_utils.generate_single_admission_time_series_data(
        data_dict=results,
        time_resolution_hours=time_resolution_hours,
        observation_window_hours=observation_window_hours)
    for m in messages:
        if m is not None:
            print(m)

    for key in ts_results.keys():
        results[key] = ts_results[key]

    if save_csv:
        data_utils.collect_and_save_patient_admission_data(results, results_path=results_path)

        return results


def main():
    project_id = "mimic_eda_local-project"
    dataset_id = "mimic_iv"
    hadm_ids = [24698912, 29974575]
    hadm_id = hadm_ids[0]
    results = analyze_single_admission_bq(project_id,
                                          dataset_id,
                                          hadm_id,
                                          time_resolution_hours=1,
                                          observation_window_hours=72,
                                          save_csv=True,
                                          results_path=results_path)


if __name__ == '__main__':
    main()
