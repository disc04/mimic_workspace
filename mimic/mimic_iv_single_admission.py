from pathlib import Path
from os.path import join
from utils import data_utils
from utils import timeseries_utils
from utils import plotting_utils
from configuration import DATA_PATH

mimic4_path = join(Path(__file__).parent.parent,
                   DATA_PATH,
                   "mimic-iv-clinical-database-demo-2.2")
results_path = join(Path(__file__).parent.parent, "results")


# TODO: currently works with hourly resolution.
#  The Dates of the events are transformed to datetime (to 12:00)


def analyze_single_admission(hosp_tables: dict,
                             icu_tables: dict,
                             hadm_id: int,
                             time_resolution_hours: int = 1,
                             observation_window_hours: int | None = None,
                             save_csv: bool = True,
                             results_path: str = results_path) -> dict:
    """
    Analyze single patient admission with time-series binning and visualization
    :param hosp_tables: Dictionary containing hospital tables.
    :param icu_tables: Dictionary containing ICU tables.
    :param hadm_id: Hospital admission ID.
    :param time_resolution_hours: Time resolution for binning (e.g., 1 for hourly, 0.5 for 30min).
    :param observation_window_hours: Max hours to analyze (None for full stay).
    :param save_csv: Whether to save patients tables to csv files.
    :param results_path: Folder to save results.
    :returns: Dictionary containing patient admission analysis and time-series data.
    """

    results_dict = data_utils.extract_admissions_data(hosp_tables=hosp_tables,
                                                      icu_tables=icu_tables,
                                                      hadm_ids=hadm_id,
                                                      return_as_cohort=False)
    results = results_dict[hadm_id]

    ts_results, messages = timeseries_utils.generate_single_admission_time_series_data(
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


def print_summary(patient_data):
    print("Analysis completed successfully!")
    print(f"\nData Summary:")
    print(f"- Time points: {len(patient_data['time_grid'])}")
    print(f"- Vital signs tracked: {len([col for col in patient_data['vitals'].columns])}")
    print(f"- Lab tests tracked: {len([col for col in patient_data['labs'].columns])}")
    print(f"- Medications tracked: {len([col for col in patient_data['prescription_medications'].columns])}")
    print(f"- Procedures tracked: {len([col for col in patient_data['procedures'].columns])}")
    print(f"- Static features: {len(patient_data['diagnoses'])}")


def main():
    # Load tables
    hosp_tables, icu_tables = data_utils.load_mimic_data(mimic4_path, verbose=False)

    hadm_ids = [24698912, 29974575]  # 28503629

    # Get a sample patient for demonstration
    hadm_id = hadm_ids[0]
    print(f"Analyzing sample admission: {hadm_id}")
    patient_data = analyze_single_admission(hosp_tables,
                                            icu_tables,
                                            hadm_id=hadm_id,
                                            time_resolution_hours=1,
                                            observation_window_hours=72,  # First 72 hours only
                                            save_csv=True,
                                            results_path=results_path)
    if patient_data:
        print_summary(patient_data)
        plotting_utils.plot_medications(patient_data, results_path=results_path)
        plotting_utils.plot_procedures_timeline(patient_data, results_path=results_path)


if __name__ == '__main__':
    main()
