from typing import List, Set
import pandas as pd
from ratelimiter import RateLimiter
from google.cloud import bigquery  #, storage
import query_builder
from data_utils import split_admissions_by_id_list


# pip install google-cloud-bigquery, google-cloud-storage
# Python IS case-sensitive, BQ isn't case-sensitive in column names...


def get_bq_client(project_id: str):
    """Create or reuse a BigQuery client."""
    return bigquery.Client(project=project_id)


@RateLimiter(max_calls=1, period=5)
def execute_query(client, query, job_config=None, log=True):
    try:
        if log:
            print(f"Running query:\n{query[:200]}...")  # preview only
        job = client.query(query, job_config=job_config)
        result = job.result()
        print(f"Query finished in {job.ended - job.started}")
        return result
    except Exception as e:
        print(f"Query failed: {e}")
        raise


def get_valid_columns(client: bigquery.Client,
                      project_id: str,
                      dataset_id: str,
                      table_name: str,
                      ) -> Set[str]:
    """Return available column names for a target table.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param table_name: BigQuery target table"""

    table = client.get_table(f"{project_id}.{dataset_id}.{table_name}")
    return {field.name for field in table.schema}


def set_hadm_ids_config(hadm_ids: List[str]):
    """Create ArraQueryParemeter for hadm_ids list."""
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("hadm_ids", "INT64", hadm_ids)
        ]
    )
    return job_config


def extract_admissions_data_bq(client: bigquery.Client,
                               project_id: str,
                               dataset_id: str,
                               hadm_ids: int | list | None,
                               return_as_cohort: bool) -> dict:
    """
    Extract admission data from BigQuery.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: Can be int for single admission, list for multiple admissions, None for all admissions
    (returns all admissions).
    :param return_as_cohort: Return cohort data as dataframes. If False, return dictionary by admission_id key.
    :return: Dictionary with hadm_ids keys and admission dictionaries as values.
    """

    # Get available demographics columns
    available_demographics = get_valid_columns(client, project_id, dataset_id, "patients")

    # Get admissions
    admissions, hadm_ids = get_admissions_bq(client,
                                             project_id,
                                             dataset_id,
                                             list(available_demographics),
                                             hadm_ids)
    labs, _ = get_labs_bq(client,
                          project_id,
                          dataset_id,
                          hadm_ids)
    prescriptions_medications, emar_medications, infusions_medications = (get_medications_bq(client,
                                                                                             project_id,
                                                                                             dataset_id,
                                                                                             hadm_ids))
    admissions_data = {
        "admission": admissions,
        "diagnoses": get_diagnoses_bq(client,
                                      project_id,
                                      dataset_id, hadm_ids),
        "vitals": get_vitals_bq(client,
                                project_id,
                                dataset_id,
                                hadm_ids),
        "labs": labs,
        "prescription_medications": prescriptions_medications,
        "emar_medications": emar_medications,
        "infusion_medications": infusions_medications,
        "procedures": get_procedures_bq(client,
                                        project_id,
                                        dataset_id, hadm_ids),
        "icu_procedures": get_icu_procedures_bq(client,
                                                project_id,
                                                dataset_id,
                                                hadm_ids),
        "transfers": get_transfers_bq(client,
                                      project_id,
                                      dataset_id,
                                      hadm_ids)
    }

    if return_as_cohort:
        return admissions_data
    else:
        admissions_by_hadm_id = split_admissions_by_id_list(admissions_data,
                                                            hadm_ids)
        return admissions_by_hadm_id


def get_admissions_bq(client: bigquery.Client,
                      project_id: str,
                      dataset_id: str,
                      available_demographics: List[str],
                      hadm_ids: int | list | None) -> tuple:
    """
    Extracts single or multiple admissions from BigQuery.
    :param client: a BigQuery client.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_demographics: list of available columns in the patients table.
    :param hadm_ids: Can be int for single admission, list for multiple admissions, None for all admissions.
    :return: Filtered admission dataframe with single hadm_id or  multiple hadm_ids.
    """
    admission_query = query_builder.build_admissions_query(project_id,
                                                           dataset_id,
                                                           available_demographics,
                                                           hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    admissions = execute_query(client, admission_query, job_config).to_dataframe()
    hadm_ids = admissions["hadm_id"].unique().tolist()
    return admissions, hadm_ids


def get_vitals_bq(client,
                  project_id,
                  dataset_id,
                  hadm_ids: list) -> pd.DataFrame:
    """
    Retrieves vital signs from admission data
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: a dataframe with vital signs events
    """
    icustays = get_valid_columns(client, project_id, dataset_id, "icustays")
    chartevents = get_valid_columns(client, project_id, dataset_id, "chartevents")
    d_items = get_valid_columns(client, project_id, dataset_id, "d_items")
    vitals_query = query_builder.build_vitals_query(project_id,
                                                    dataset_id,
                                                    list(icustays),
                                                    list(chartevents),
                                                    list(d_items),
                                                    hadm_ids)

    job_config = set_hadm_ids_config(hadm_ids)
    return execute_query(client, vitals_query, job_config).to_dataframe()


def get_labs_bq(client,
                project_id,
                dataset_id,
                hadm_ids: list) -> tuple:
    """
    Retrieves laboratory test results from admission data.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: a dataframe with laboratory test events
    """
    labs = get_valid_columns(client, project_id, dataset_id, "labevents")
    descriptions = get_valid_columns(client, project_id, dataset_id, "d_labitems")
    query = query_builder.build_procedures_query(project_id,
                                                 dataset_id,
                                                 list(labs),
                                                 list(descriptions),
                                                 hadm_ids)

    job_config = set_hadm_ids_config(hadm_ids)
    lab_results = execute_query(client, query, job_config).to_dataframe()

    # Get abnormal labs (flagged as abnormal)
    abnormal_labs = lab_results[lab_results['flag'].notna() & (lab_results['flag'] != '')] if (
            len(labs) > 0) else pd.DataFrame()

    return labs, abnormal_labs


def get_medications_bq(client: bigquery.Client,
                       project_id: str,
                       dataset_id: str,
                       hadm_ids: list) -> tuple:
    """
    Retrieves medications from admission data.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: dataframes with prescribed medications, emar records, and infusions medications.
    """
    prescriptions = get_valid_columns(client, project_id, dataset_id, "prescriptions")
    emar = get_valid_columns(client, project_id, dataset_id, "emar")
    infusions = get_valid_columns(client, project_id, dataset_id, "inputevents")
    inf_descriptions = get_valid_columns(client, project_id, dataset_id, "d_items")

    prescriptions_query = query_builder.build_prescriptions_query(project_id,
                                                                  dataset_id,
                                                                  list(prescriptions),
                                                                  hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    prescriptions_results = execute_query(client, prescriptions_query, job_config).to_dataframe()

    # EMAR (medication administration records)
    emar_query = query_builder.build_emar_query(project_id,
                                                dataset_id,
                                                list(emar),
                                                hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    emar_results = execute_query(client, emar_query, job_config).to_dataframe()

    # Infusions (from ICU)
    infusions_query = query_builder.build_infusions_query(project_id,
                                                          dataset_id,
                                                          list(infusions),
                                                          list(inf_descriptions),
                                                          hadm_ids)

    job_config = set_hadm_ids_config(hadm_ids)
    infusions_results = execute_query(client, infusions_query, job_config).to_dataframe()

    return prescriptions_results, emar_results, infusions_results


def get_procedures_bq(client: bigquery.Client,
                      project_id,
                      dataset_id,
                      hadm_ids: list) -> pd.DataFrame:
    """Retrieves procedures billed by hospital.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: dataframes with hospital procedures.
    """
    procedures = get_valid_columns(client, project_id, dataset_id, "procedures_icd")
    descriptions = get_valid_columns(client, project_id, dataset_id, "d_icd_procedures")
    query = query_builder.build_procedures_query(project_id,
                                                 dataset_id,
                                                 list(procedures),
                                                 list(descriptions),
                                                 hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    return execute_query(client, query, job_config).to_dataframe()


def get_icu_procedures_bq(client: bigquery.Client,
                          project_id: str,
                          dataset_id: str,
                          hadm_ids: list) -> pd.DataFrame:
    """
    Retrieves procedures documented during the ICU stay.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: dataframes with icu procedures.
    """
    procedures = get_valid_columns(client, project_id, dataset_id, "procedureevents")
    descriptions = get_valid_columns(client, project_id, dataset_id, "d_items")
    query = query_builder.build_icu_procedures_query(project_id,
                                                     dataset_id,
                                                     list(procedures),
                                                     list(descriptions),
                                                     hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    return execute_query(client, query, job_config).to_dataframe()


def get_diagnoses_bq(client: bigquery.Client,
                     project_id: str,
                     dataset_id: str,
                     hadm_ids: list) -> pd.DataFrame:
    """
    Retrieves hospital diagnoses.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: dataframes with diagnoses.
    """
    diagnoses = get_valid_columns(client, project_id, dataset_id, "diagnoses_icd")
    descriptions = get_valid_columns(client, project_id, dataset_id, "d_icd_diagnoses")
    query = query_builder.build_diagnoses_query(project_id,
                                                dataset_id,
                                                diagnoses,
                                                descriptions,
                                                hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    return execute_query(client, query, job_config).to_dataframe()


def get_transfers_bq(client: bigquery.Client,
                     project_id: str,
                     dataset_id: str,
                     hadm_ids: list) -> pd.DataFrame:
    """Retrieves transfers between the departments during the hospital stay.
    :param client: a BigQuery client
    :param project_id: BigQuery project name
    :param dataset_id: BigQuery dataset name
    :param hadm_ids: list of hadm_ids
    :return: dataframes with icu transfers. """
    available_cols = get_valid_columns(client, project_id, dataset_id, "transfers")

    query = query_builder.build_transfers_query(project_id,
                                                dataset_id,
                                                list(available_cols),
                                                hadm_ids)
    job_config = set_hadm_ids_config(hadm_ids)
    return execute_query(client, query, job_config).to_dataframe()


def get_services(client: bigquery.Client,
                 project_id: str,
                 dataset_id: str) -> pd.DataFrame:
    """For total hospital services."""
    services_query = query_builder.build_services_query(project_id,
                                                        dataset_id)
    return execute_query(client, services_query).to_dataframe()


# TODO
def export_table_to_gcs(client, table_name, gcs_uri):
    pass
