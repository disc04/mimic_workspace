import os
from os.path import join
from pathlib import Path

# PROJECT_ROOT_PATH = Path(__file__).parent.parent
MODEL_PATH = Path("models")
RESULTS_PATH = Path("results")
DATA_PATH = Path("data")

mimic_iv_data_sources = [{"name": "transfers", "datatype": "categorical", "time_col": "intime",
                          "value_col": None, "label_col": "careunit"},

                         {"name": "vitals", "datatype": "discrete", "time_col": "charttime", "value_col": "valuenum",
                          "label_col": "label"},

                         {"name": "labs", "datatype": "discrete", "time_col": "charttime",
                         "value_col": "valuenum", "label_col": "label"},

                         {"name": "prescription_medications", "datatype": "continuous", "start_col": "starttime",
                          "end_col": "stoptime", "value_col": None,  "label_col": "label"},

                         {"name": "infusion_medications", "datatype": "continuous", "start_col": "starttime",
                          "end_col": "endtime", "value_col": None, "label_col": "label"},

                         {"name": "emar_medications", "datatype": "categorical", "time_col": "charttime",
                          "value_col": None, "label_col": "medication"},

                         {"name": "procedures", "datatype": "categorical", "time_col": "chartdate",
                          "value_col": None, "label_col": "long_title"},

                         {"name": "icu_procedures", "datatype": "continuous", "start_col": "starttime",
                          "end_col": "endtime", "value_col": None,  "label_col": "label"}]


service_codes_dict = {'CMED': 'Cardiac Medical',
                      'CSURG': 'Cardiac Surgery',
                      'DENT': 'Dental',
                      'ENT': 'Ear, nose, and throat',
                      'EYE': 'Eye diseases',
                      'GU': 'Genitourinary',
                      'GYN': 'Gynecological',
                      'MED': 'Medical',
                      'NB': 'Newborn',
                      'NBB': 'Newborn baby',
                      'NMED': 'Neurologic Medical',
                      'NSURG': 'Neurologic Surgical',
                      'OBS': 'Obstetrics',
                      'ORTHO': 'Orthopaedic',
                      'OMED': 'Oncologic Medical',
                      'PSURG': 'Plastic',
                      'PSYCH': 'Psychiatric',
                      'SURG': 'Surgical',
                      'TRAUM': 'Trauma',
                      'TSURG': 'Thoracic Surgical',
                      'VSURG': 'Vascular Surgical'}

vitals_keywords = ['Heart Rate', 'HR', 'Blood Pressure', 'BP',
                   'Temperature', 'Respiratory Rate', 'RR', 'SpO2', 'O2 sat']

# common MIMIC itemids
vital_signs_dictionary = {'Heart Rate': ['Heart Rate', 'HR', 'heart rate'],
                          'Blood Pressure Systolic': ['NBP Systolic', 'Arterial BP Systolic', 'ART BP Systolic',
                                                      'systolic'],
                          'Blood Pressure Diastolic': ['NBP Diastolic', 'Arterial BP Diastolic', 'ART BP Diastolic',
                                                       'diastolic'],
                          'Temperature': ['Temperature', 'Temp', 'temperature'],
                          'Respiratory Rate': ['Respiratory Rate', 'RR', 'Resp Rate', 'respiratory rate'],
                          'SpO2': ['SpO2', 'O2 saturation', 'oxygen saturation']}

# Common MIMIC severity scores
severity_scores_dictionary = {'SOFA': ['SOFA', 'Sequential Organ Failure Assessment'],
                              'SAPS': ['SAPS', 'Simplified Acute Physiology Score'],
                              'GCS': ['Glasgow Coma Scale', 'GCS']}

ventilator_keywords = [
        'ventilator', 'mechanical ventilation', 'PEEP', 'FiO2', 'tidal volume',
        'respiratory rate', 'vent', 'intubat', 'extubat', 'weaning',
        'pressure support', 'CPAP', 'BiPAP', 'assist control'
    ]

# Focus on common cardiovascular and respiratory medications
target_meds = ['METOPROLOL', 'PROPRANOLOL', 'ATENOLOL', 'FUROSEMIDE', 'LISINOPRIL',
               'ALBUTEROL', 'IPRATROPIUM', 'NITROGLYCERIN', 'DOPAMINE', 'NOREPINEPHRINE']

# Drugs which we do not want to see in a plot
medications_exclusions = ['Vial', 'Bag', 'Lidocaine_Jelly_2%_(Urojet)', 'Vitamin_B_Complex', 'Multivitamins',
                          'Senna', 'Vitamin_E', 'Syringe_(SW)', 'Sterile_Water', 'Vitamin_D',
                          'Fluticasone_Propionate_NASAL', 'Artificial_Tears',
                          'Polyethylene_Glycol', 'Chlorhexidine_Gluconate_0.12%_']
drug_categories_dictionary = {'Cardiovascular': ['METOPROLOL', 'AMLODIPINE', 'LISINOPRIL', 'ATENOLOL', 'CARVEDILOL',
                                                 'FUROSEMIDE', 'ASPIRIN', 'DIGOXIN', 'WARFARIN', 'HEPARIN'],
                              'Antibiotics': ['VANCOMYCIN', 'CIPROFLOXACIN', 'LEVOFLOXACIN', 'CEFTRIAXONE',
                                              'AZITHROMYCIN', 'AMOXICILLIN', 'CLINDAMYCIN', 'DOXYCYCLINE',
                                              'PENICILLIN', 'AMPICILLIN'],
                              'Pain/Analgesics': ['MORPHINE', 'FENTANYL', 'OXYCODONE', 'HYDROMORPHONE',
                                                  'ACETAMINOPHEN', 'IBUPROFEN', 'TRAMADOL', 'CODEINE', 'DILAUDID',
                                                  'PERCOCET'],
                              'Sedatives/Psychiatric': ['LORAZEPAM', 'MIDAZOLAM', 'PROPOFOL', 'HALOPERIDOL',
                                                        'QUETIAPINE', 'OLANZAPINE', 'RISPERIDONE', 'SERTRALINE',
                                                        'CITALOPRAM', 'TRAZODONE'],
                              'Gastrointestinal': ['PANTOPRAZOLE', 'OMEPRAZOLE', 'RANITIDINE', 'METOCLOPRAMIDE',
                                                   'ONDANSETRON','SIMETHICONE', 'DOCUSATE', 'LACTULOSE', 'SENNOSIDES'],
                              'Diabetes/Endocrine': ['INSULIN', 'METFORMIN', 'GLIPIZIDE', 'GLYBURIDE', 'LEVOTHYROXINE',
                                                     'PREDNISONE', 'HYDROCORTISONE', 'DEXAMETHASONE'],
                              'Respiratory': ['ALBUTEROL', 'IPRATROPIUM', 'PREDNISONE', 'METHYLPREDNISOLONE',
                                              'BUDESONIDE'],
                              'IV Fluids/Electrolytes': ['SODIUM CHLORIDE', 'POTASSIUM CHLORIDE', 'MAGNESIUM',
                                                         'CALCIUM', 'DEXTROSE', 'LACTATED RINGERS']
                              }