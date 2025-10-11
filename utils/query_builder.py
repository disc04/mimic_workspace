from typing import List
import re
from config.project_configuration import (patients_columns, vitals_keywords, transfers_columns,
                                          diagnoses_icd_columns, d_icd_diagnoses_columns,
                                          procedureevents_columns, d_items_columns, procedures_icd_columns,
                                          d_icd_procedures_columns, prescriptions_columns, emar_columns, inputevents_columns,
                                          labevents_columns, d_labitems_columns, icustays_columns, chartevents_columns)


def build_admissions_query(project_id: str,
                           dataset_id: str,
                           available_demographics: List[str],
                           hadm_ids: int | list | None) -> str:
    """
    Defines query for single or multiple admissions from BigQuery.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_demographics: list of available columns in the patients table.
    :param hadm_ids: Can be int for single admission, list for multiple admissions, None for all admissions.
    :return: sql query.
    """
    selected_demographics = [col for col in patients_columns if col in available_demographics]
    demographics_str = ", ".join([f"p.{col}" for col in selected_demographics])

    if hadm_ids is None:
        admissions_query = f"""SELECT *,
                           {demographics_str}
                           FROM `{project_id}.{dataset_id}.admissions` AS a
                           LEFT JOIN `{project_id}.{dataset_id}.patients` AS p
                           ON a.subject_id = p.subject_id
                           """
    else:
        if isinstance(hadm_ids, int):
            hadm_ids = [hadm_ids]

        admissions_query = f"""SELECT  a.*,  
                            {demographics_str} 
                            FROM `{project_id}.{dataset_id}.admissions` AS a
                            JOIN UNNEST(@hadm_ids) AS hadm_id
                            ON a.hadm_id = hadm_id
                            LEFT JOIN `{project_id}.{dataset_id}.patients` AS p
                            ON a.subject_id = p.subject_id
                        """
    return admissions_query


def build_vitals_query(project_id: str,
                       dataset_id: str,
                       available_icustays: list[str],
                       available_chartevents: list[str],
                       available_d_items,
                       hadm_ids: list[str]) -> str:
    """
    Defines query for recorded vital signs data.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_icustays: list of available columns in the icustays table.
    :param available_chartevents: list of available columns in the chartevents table.
    :param available_d_items: list of available column sin the d_items table.
    :param hadm_ids: list of target hadm_ids.
    :return: sql query.
    """
    events_str = prepare_column_string(available_chartevents,
                                       chartevents_columns,
                                       available_d_items,
                                       d_items_columns)
    times_str = ", ".join([f"stays.{col}" for col in icustays_columns if col in available_icustays])
    cols_str = ", ".join([events_str, times_str])

    # escape non-alphanumeric characters
    # prevents accidental regex misinterpretation (e.g., "O2 (sat)" → "O2 \(sat\)")
    vitals_pattern = '|'.join(re.escape(k) for k in vitals_keywords)

    query = f"""SELECT {cols_str}
            FROM `{project_id}.{dataset_id}.icustays` AS times
            JOIN `{project_id}.{dataset_id}.chartevents` AS event
            ON times.hadm_id = event.hadm_id
            JOIN `{project_id}.{dataset_id}.d_items` AS event_desc
                ON event.itemid = event_desc.itemid
            JOIN UNNEST(@hadm_ids) AS hadm_id
                ON event.hadm_id = hadm_id
            WHERE event_desc.label IS NOT NULL
                AND REGEXP_CONTAINS(event_desc.label, '(?i){vitals_pattern}')
            """
    return query


def build_labs_query(project_id: str,
                     dataset_id: str,
                     available_labs: list[str],
                     available_d_labitems: list[str],
                     hadm_ids: list[str]):
    """
    Defines query for lab tests results.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_labs: list of available columns in the labevents table.
    :param available_d_labitems: list of available columns in the d_labitems table.
    :param hadm_ids: List of target hadm_ids.
    :return: sql query.
    """
    cols_str = prepare_column_string(available_labs,
                                     labevents_columns,
                                     available_d_labitems,
                                     d_labitems_columns)
    query = f""" SELECT {cols_str}
                FROM `{project_id}.{dataset_id}.labevents` AS  event
                JOIN `{project_id}.{dataset_id}.d_labitems` AS event_desc 
                ON event.itemid = event_desc.itemid
                JOIN UNNEST(@hadm_ids) AS hadm_id
                ON event.hadm_id = hadm_id
            """
    return query


def build_infusions_query(project_id: str,
                          dataset_id: str,
                          available_inputevents: List[str],
                          available_d_items: List[str],
                          hadm_ids: List[int]) -> str:
    """
    Defines query for infusions medications.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_inputevents: list of available columns in the inputevents table.
    :param available_d_items: list of available columns in the d_items table.
    :param hadm_ids: List of target hadm_ids.
    :return: sql query.
    """
    cols_str = prepare_column_string(available_inputevents,
                                     inputevents_columns,
                                     available_d_items,
                                     d_items_columns)
    # Coalesce to avoid NULL values
    infusions_query = f"""SELECT {cols_str},
                    CONCAT(event_desc.label, ' ', 
                    COALESCE(CAST(event.rate AS STRING), ''), ' ',
                    COALESCE(event.rateuom, '')) AS label_full
                    FROM `{project_id}.{dataset_id}.inputevents` AS event
                    JOIN `{project_id}.{dataset_id}.d_items` AS event_desc
                    ON event.itemid = event_desc.itemid
                    JOIN UNNEST(@hadm_ids) AS hadm_id
                    ON event.hadm_id = hadm_id
                    """
    return infusions_query


def build_emar_query(project_id: str,
                     dataset_id: str,
                     available_emar: List[str],
                     hadm_ids: List[int]) -> str:
    """
    Defines query for EMAR records medications .
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_emar: list of available columns in the emar table.
    :param hadm_ids: list of target hadm_ids.
    :return: sql query.
     """
    selected = [c for c in emar_columns if c in available_emar]
    cols_str = ", ".join([f"em.{col}" for col in selected])
    emar_query = f"""SELECT {cols_str}
                 FROM `{project_id}.{dataset_id}.emar` as em
                 WHERE medication IS NOT NULL
                 JOIN UNNEST(@hadm_ids) AS hadm_id
                 ON em.hadm_id = hadm_id
                 """
    return emar_query


def build_prescriptions_query(project_id: str,
                              dataset_id: str,
                              available_prescriptions: List[str],
                              hadm_ids: List[int]) -> str:
    """
    Defines query for prescriptions medications.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_prescriptions: list of available columns in the prescriptions table.
    :param hadm_ids: list of terget hadm_ids.
    :return: sql query.
    """
    selected = [c for c in prescriptions_columns if c in available_prescriptions]
    cols_str = ", ".join([f"pr.{col}" for col in selected])
    prescriptions_query = f"""SELECT {cols_str}
                          CONCAT(drug, ' ', CAST(dose_val_rx AS STRING), ' ', dose_unit_rx) as label
                          FROM `{project_id}.{dataset_id}.prescriptions` AS pr
                          JOIN UNNEST(@hadm_ids) AS hadm_id
                          ON pr.hadm_id = hadm_id
                          """
    return prescriptions_query


def build_procedures_query(project_id: str,
                           dataset_id: str,
                           available_procedures: List[str],
                           available_d_icd_procedures: List[str],
                           hadm_ids: List[int]) -> str:
    """
    Defines query for hospital procedures.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_procedures: list of available columns in the procedures_icd table.
    :param available_d_icd_procedures: list of available columns in the d_icd_procedures table.
    :param hadm_ids: list of target hadm_ids.
    :return: sql query.
    """
    cols_str = prepare_column_string(available_procedures,
                                     procedures_icd_columns,
                                     available_d_icd_procedures,
                                     d_icd_procedures_columns)
    query = f"""SELECT {cols_str}
                FROM `{project_id}.{dataset_id}.procedures_icd` event
                JOIN `{project_id}.{dataset_id}.d_icd_procedures` event_desc 
                    ON event.icd_code = event_desc.icd_code 
                    AND event.icd_version = event_desc.icd_version
                JOIN UNNEST(@hadm_ids) AS hadm_id
                ON event.hadm_id = hadm_id
                """
    return query


def build_icu_procedures_query(project_id: str,
                               dataset_id: str,
                               available_procedureevents: List[str],
                               available_d_items: List[str],
                               hadm_ids: List[int]) -> str:
    """
    Defines query for ICU stays procedures.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_procedureevents: list of available columns in the procedureevents table.
    :param available_d_items: list of available columns in the d_items table.
    :param hadm_ids: list of target hadm_ids.
    :return: sql query.
    """
    cols_str = prepare_column_string(available_procedureevents,
                                     procedureevents_columns,
                                     available_d_items,
                                     d_items_columns)
    query = f"""SELECT {cols_str}
                CONCAT(event_desc.label, ' ', CAST(event.value AS STRING), ' ', event.valueuom) as label_full
                FROM `{project_id}.{dataset_id}.procedureevents` event
                JOIN `{project_id}.{dataset_id}.d_items` event_desc ON event.itemid = di.itemid
                JOIN UNNEST(@hadm_ids) AS hadm_id
                ON event.hadm_id = hadm_id
               """
    return query


def prepare_column_string(available_events: List[str],
                          events_features: List[str],
                          available_descriptions: List[str],
                          descriptions_features: List[str]) -> str:
    """Prepares column string from column names of the event dataframe and description dataframe."""
    selected_events = [c for c in events_features if c in available_events]
    selected_descriptions = [c for c in descriptions_features if c in available_descriptions]
    events_str = ", ".join([f"event.{col}" for col in selected_events])
    descriptions_str = ", ".join([f"event_desc.{col}" for col in selected_descriptions])
    cols_str = ", ".join([events_str, descriptions_str])
    return cols_str


def build_diagnoses_query(project_id: str,
                          dataset_id: str,
                          available_diagnoses: List[str],
                          available_d_icd_diagnoses: List[str],
                          hadm_ids: List[int]):
    """
    Defines query for hospital diagnoses.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_diagnoses: list of available columns in the diagnoses table.
    :param available_d_icd_diagnoses: list of available columns in the d_icd_diagnoses table.
    :param hadm_ids: list of target hadm_ids.
    :return: sql query.
    """
    cols_str = prepare_column_string(available_diagnoses,
                                     diagnoses_icd_columns,
                                     available_d_icd_diagnoses,
                                     d_icd_diagnoses_columns)
    query = f"""SELECT {cols_str}
                FROM `{project_id}.{dataset_id}.diagnoses_icd` event
                JOIN `{project_id}.{dataset_id}.d_icd_diagnoses` event_desc
                    ON event.icd_code = event_desc.icd_code 
                    AND event.icd_version = event_desc.icd_version
                JOIN UNNEST(@hadm_ids) AS hadm_id
                    ON event.hadm_id = hadm_id
                ORDER BY event.hadm_id, event.seq_num
                """
    return query


def build_transfers_query(project_id: str,
                          dataset_id: str,
                          available_transfers: List[str],
                          hadm_ids: List[int]) -> str:
    """
    Retrieves transfers between the departments during the hospital stay.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :param available_transfers: a list of available columns in the transfers table.
    :param hadm_ids: list of hadm_ids.
    :return: sql query
    """

    selected = [c for c in transfers_columns if c in available_transfers]
    cols_str = ", ".join([f"t.{col}" for col in selected])

    query = f"""
                SELECT {cols_str}
                FROM `{project_id}.{dataset_id}.transfers` AS event
                JOIN UNNEST(@hadm_ids) AS hadm_id
                    ON event.hadm_id = hadm_id
                ORDER BY hadm_id, intime
                """
    return query


def build_services_query(project_id: str,
                         dataset_id: str):
    """
    Query to retrieve services table.
    :param project_id: BigQuery project name.
    :param dataset_id: BigQuery dataset name.
    :return: sql query
    """
    services_query = f"""SELECT *
                           FROM `{project_id}.{dataset_id}.services`
                           """
    return services_query

