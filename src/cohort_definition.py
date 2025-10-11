# Build parametrized cohort queries
# example for sepsis_code = A41%
from utils.bq_utils import execute_query


def define_sepsis_cohort(client,
                         project_id,
                         dataset_id,
                         condition_code: int = 'A41%',
                         output_table: str = 'sepsis_cohort'):
    query = f"""
    CREATE OR REPLACE TABLE `{output_table}` AS
    SELECT ...
    FROM `{project_id}.{dataset_id}.admissions` a
    JOIN `{project_id}.{dataset_id}.diagnoses_icd` d ON a.hadm_id = d.hadm_id
    WHERE d.icd_code LIKE {condition_code} 
    """
    execute_query(client, query)