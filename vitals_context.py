
"""
Important Emergency Department features:

Heart Rate - Core vital, arrhythmia detection
BP Systolic/Diastolic - Hemodynamic stability (shock, hypertension)
Respiratory Rate - Respiratory distress, sepsis early warning
O2 Saturation - Immediate hypoxia detection
Temperature - Infection/sepsis screening
GCS Motor - Neurological status (most predictive GCS component)
Level of Consciousness - Rapid neuro assessment
Heart Rhythm - Critical arrhythmia identification
Pain level - Patient comfort, symptom assessment

Category Organization:
Core Vitals: Basic hemodynamics every ED patient needs
Invasive Monitoring: ICU-level parameters (arterial lines, PA catheters, ICP)
Neurological Tiered: GCS, consciousness, motor/sensory, cranial nerves
System-Based: Respiratory, cardiac, renal, GI organized by organ system
Device/Equipment: Ventilators, lines, drains, pacemakers
Assessments: Pain, sedation, delirium, functional status
Nursing Care Plans: Excluded from essential monitoring (documentation artifacts)

"""
bp_columns = ["Non_Invasive_Blood_Pressure_systolic", "Non_Invasive_Blood_Pressure_diastolic"]
vitals_dashboard = ["O2_saturation_pulseoxymetry", "Respiratory_Rate",
                    "Temperature_Celsius", "Heart_Rate", "Heart_Rhythm"]

# Clinical Parameters Categorization Dictionary
vitals_categories = {

    # Basic Vital Signs
    "basic_vitals": [
        "Non Invasive Blood Pressure sy",
        "Non Invasive Blood Pressure di",
        "O2_saturation pulseoxymetry",
        "Respiratory Rate",
        "Heart Rhythm",
        "Heart Rate",
        "Respiratory Rate (spontaneous)",
        "Respiratory Rate (Total)",
        "Temperature Celsius",
        "Temperature Fahrenheit",
        "Temperature Site"
    ],

    # Blood Pressure - Non-Invasive
    "blood_pressure_noninvasive": [
        "Non Invasive Blood Pressure systolic",
        "Non Invasive Blood Pressure diastolic",
        "Non Invasive Blood Pressure mean",
        "Non-Invasive Blood Pressure Alarm - High",
        "Non-Invasive Blood Pressure Alarm - Low",
        "NBP Alarm Source",
        "Manual Blood Pressure Systolic Left",
        "Manual Blood Pressure Diastolic Left",
        "Manual Blood Pressure Systolic Right",
        "Manual Blood Pressure Diastolic Right"
    ],

    # Blood Pressure - Arterial Line
    "blood_pressure_arterial": [
        "ART BP Systolic",
        "ART BP Diastolic",
        "ART BP Mean",
        "ART Blood Pressure Alarm - High",
        "ART Blood Pressure Alarm - Low",
        "ART Blood Pressure Alarm Source",
        "Arterial Blood Pressure systolic",
        "Arterial Blood Pressure diastolic",
        "Arterial Blood Pressure Alarm - High",
        "Arterial Blood Pressure Alarm - Low"
    ],

    # Orthostatic Vital Signs
    "orthostatic_vitals": [
        "Orthostatic BPs lying",
        "Orthostatic BPs sitting",
        "Orthostatic BPs standing",
        "Orthostatic BPd lying",
        "Orthostatic BPd sitting",
        "Orthostatic BPd standing",
        "Orthostatic HR lying",
        "Orthostatic HR sitting",
        "Orthostatic HR standing"
    ],

    # Oxygen & Pulse Oximetry
    "oxygenation": [
        "O2 saturation pulseoxymetry",
        "O2 Saturation Pulseoxymetry Alarm - High",
        "O2 Saturation Pulseoxymetry Alarm - Low",
        "O2 Delivery Device(s)",
        "O2 Flow",
        "O2 Flow (additional cannula)",
        "Arterial O2 Saturation",
        "Arterial O2 pressure",
        "PO2 (Mixed Venous)",
        "Venous O2 Pressure",
        "Mixed Venous O2% Sat",
        "Central Venous O2% Sat"
    ],

    # Cardiac Rhythm & ECG
    "cardiac_rhythm": [
        "Heart Rhythm",
        "Heart Sounds",
        "Ectopy Type",
        "Ectopy Frequency",
        "QTc",
        "ST Segment Monitoring On"
    ],

    # Hemodynamic Monitoring - Advanced
    "hemodynamics_advanced": [
        "Cardiac Output (thermodilution)",
        "Cardiac Output (CCO)",
        "Cardiac Index (CI NICOM)",
        "Cardiac Output (CO NICOM)",
        "Stroke Volume (SV NICOM)",
        "Stroke Volume Index (SVI NICOM)",
        "Stroke Volume Variation (SVV NICOM)",
        "CI (PiCCO)",
        "CO (PiCCO)",
        "SVI (PiCCO)",
        "SVV (PiCCO)",
        "SVI Change",
        "CO / CI Change"
    ],

    # Vascular Resistance & Perfusion
    "vascular_resistance": [
        "Total Peripheral Resistance (TPR) (NICOM)",
        "Total Peripheral Resistance Index (TPRI) (NICOM)",
        "SVRI (PiCCO)",
        "Thoracic Fluid Content (TFC) (NICOM)"
    ],

    # Pulmonary Artery Pressures
    "pulmonary_pressures": [
        "Pulmonary Artery Pressure systolic",
        "Pulmonary Artery Pressure diastolic",
        "Pulmonary Artery Pressure mean",
        "PCWP",
        "PAEDP",
        "PAP Alarm Source"
    ],

    # Central Venous & Right Heart
    "central_venous": [
        "Central Venous Pressure",
        "Central Venous Pressure Alarm - High",
        "Central Venous Pressure  Alarm - Low"
    ],

    # Intracranial & Cerebral Perfusion
    "neurological_pressures": [
        "Intra Cranial Pressure",
        "Intra Cranial Pressure #2",
        "Intra Cranial Pressure Alarm - High",
        "Intra Cranial Pressure Alarm - Low",
        "Intra Cranial Pressure #2 Alarm - High",
        "Intra Cranial Pressure #2 Alarm - Low",
        "Cerebral Perfusion Pressure",
        "Cerebral Perfusion Pressure Alarm - High",
        "Cerebral Perfusion Pressure Alarm - Low"
    ],

    # Ventilator Settings - Basic
    "ventilator_basic": [
        "Ventilator Type",
        "Ventilator Mode",
        "Respiratory Rate (Set)",
        "Tidal Volume (set)",
        "Tidal Volume (observed)",
        "Tidal Volume (spontaneous)",
        "PEEP set",
        "Total PEEP Level",
        "Inspired O2 Fraction"
    ],

    # Ventilator Settings - Advanced
    "ventilator_advanced": [
        "Peak Insp. Pressure",
        "Plateau Pressure",
        "Mean Airway Pressure",
        "Inspiratory Time",
        "Inspiratory Ratio",
        "Expiratory Ratio",
        "Flow Rate (L/min)",
        "Flow Pattern",
        "Flow Sensitivity",
        "Minute Volume",
        "Minute Volume Alarm - High",
        "Minute Volume Alarm - Low",
        "PSV Level",
        "PCV Level",
        "Pinsp (Draeger only)"
    ],

    # Ventilator - APRV Mode
    "ventilator_aprv": [
        "P High (APRV)",
        "P Low (APRV)",
        "T High (APRV)",
        "T Low (APRV)"
    ],

    # Ventilator - Special Modes
    "ventilator_special": [
        "Recruitment Mode",
        "Recruitment Duration",
        "Slope",
        "Vti High",
        "Paw High"
    ],

    # Non-Invasive Ventilation
    "noninvasive_ventilation": [
        "BiPap Mode",
        "BiPap IPAP",
        "BiPap EPAP",
        "BiPap O2 Flow",
        "BiPap Mask",
        "NIV Mask",
        "Continuous Pressure Machine",
        "Autoset/CPAP"
    ],

    # Respiratory Mechanics
    "respiratory_mechanics": [
        "Vital Cap",
        "Negative Insp. Force",
        "RSBI Deferred",
        "Spont RR",
        "Spont Vt",
        "Transpulmonary Pressure (Insp. Hold)",
        "Transpulmonary Pressure (Exp. Hold)"
    ],

    # Blood Gas - Arterial
    "blood_gas_arterial": [
        "PH (Arterial)",
        "Arterial CO2 Pressure",
        "Arterial Base Excess",
        "TCO2 (calc) Arterial",
        "EtCO2",
        "PeCO2"
    ],

    # Blood Gas - Venous
    "blood_gas_venous": [
        "PH (Venous)",
        "Venous CO2 Pressure",
        "TCO2 (calc) Venous"
    ],

    # Blood Gas - Other
    "blood_gas_other": [
        "SvO2",
        "SvO2 SQI",
        "Carboxyhemoglobin",
        "Methemoglobin"
    ],

    # Airway Management
    "airway": [
        "Airway Type",
        "ETT",
        "Trach Tube Type",
        "Trach Tube Size (I.D.)",
        "Trach Tube Manufacturer",
        "Cuff Pressure",
        "Cuff Volume (mL)",
        "Known difficult intubation",
        "Vented"
    ],

    # Respiratory Assessment
    "respiratory_assessment": [
        "Respiratory Pattern",
        "Respiratory Effort",
        "Breathing pattern/effort",
        "Resp Alarm - High",
        "Resp Alarm - Low",
        "Airway problems",
        "Cough Effort",
        "Cough Type",
        "Cough Reflex"
    ],

    # Neurological Assessment - GCS
    "neuro_gcs": [
        "GCS - Eye Opening",
        "GCS - Verbal Response",
        "GCS - Motor Response"
    ],

    # Neurological Assessment - Level of Consciousness
    "neuro_consciousness": [
        "Level of Consciousness",
        "Mental status",
        "Orientation to Person",
        "Orientation to Place",
        "Orientation to Time",
        "Orient/Clouding Sensory",
        "Commands",
        "Commands Response"
    ],

    # Neurological Assessment - Motor/Sensory
    "neuro_motor_sensory": [
        "Motor Deficit",
        "Motor L Arm",
        "Motor L Leg",
        "Motor R Arm",
        "Motor R Leg",
        "Strength L Arm",
        "Strength L Leg",
        "Strength R Arm",
        "Strength R Leg",
        "Sensory Level",
        "LUE Sensation",
        "RUE Sensation",
        "LLE Sensation",
        "RLE Sensation"
    ],

    # Neurological Assessment - Cranial Nerves
    "neuro_cranial": [
        "Pupil Size Left",
        "Pupil Size Right",
        "Pupil Response Left",
        "Pupil Response Right",
        "Extraocular Movements",
        "Corneal Reflex Left",
        "Corneal Reflex Right",
        "Gag Reflex",
        "Facial Droop",
        "Visual Field Cut"
    ],

    # Neurological Assessment - Cerebellar
    "neuro_cerebellar": [
        "Cerebellar - Finger -> Nose",
        "Cerebellar - Heel -> Shin",
        "Pronator Drift",
        "Pronator drift present",
        "Ataxia",
        "Sustained Nystagmus",
        "Shoulder Shrug"
    ],

    # Neurological - Other Signs
    "neuro_other": [
        "Spontaneous Movement",
        "Response to Stimuli (Type)",
        "Seizure",
        "Seizure Activity",
        "Seizure Duration",
        "Neurological Symptoms"
    ],

    # Sedation & Delirium Assessment
    "sedation_delirium": [
        "Richmond-RAS Scale",
        "Goal Richmond-RAS Scale",
        "Delirium assessment",
        "CAM-ICU MS Change",
        "CAM-ICU Altered LOC",
        "CAM-ICU Inattention",
        "CAM-ICU Disorganized thinking",
        "Drowsiness",
        "Agitation"
    ],

    # Pain Assessment - CPOT
    "pain_cpot": [
        "CPOT-Pain Assessment Method",
        "CPOT-Facial Expression (CPOTa)",
        "CPOT-Facial Expression (CPOTb)",
        "CPOT-Body Movements (CPOTa)",
        "CPOT-Body Movements (CPOTb)",
        "CPOT-Muscle Tension (CPOTa)",
        "CPOT-Muscle Tension (CPOTb)",
        "CPOT-Vocalization (CPOTa)",
        "CPOT-Vocalization (CPOTb)",
        "CPOT-Pain Management"
    ],

    # Pain Assessment - General
    "pain_general": [
        "Currently experiencing pain",
        "Baseline pain level",
        "Current Dyspnea Assessment"
    ],

    # CIWA Assessment (Alcohol Withdrawal)
    "ciwa_assessment": [
        "Nausea and Vomiting (CIWA)",
        "Tremor (CIWA)",
        "Paroxysmal Sweats",
        "Tactile Disturbances",
        "Auditory Disturbance",
        "Visual Disturbances",
        "Headache",
        "Anxiety"
    ],

    # Peripheral Circulation - Upper Extremity
    "circulation_upper": [
        "RUE Color",
        "RUE Temp",
        "LUE Color",
        "LUE Temp",
        "Radial Pulse L",
        "Radial Pulse R",
        "Ulnar Pulse L",
        "Ulnar Pulse R",
        "Brachial Pulse L",
        "Brachial Pulse R",
        "Capillary Refill L",
        "Capillary Refill R"
    ],

    # Peripheral Circulation - Lower Extremity
    "circulation_lower": [
        "RLE Color",
        "RLE Temp",
        "LLE Color",
        "LLE Temp",
        "Femoral Pulse L",
        "Femoral Pulse R",
        "Popliteal Pulse L",
        "Popliteal Pulse R",
        "PostTib. Pulses L",
        "PostTib. Pulses R",
        "Dorsal PedPulse L",
        "Dorsal PedPulse R"
    ],

    # Circulation - Other
    "circulation_other": [
        "Pulsus Paradoxus",
        "Graft/Flap Pulse",
        "AV Fistula L Bruit",
        "AV Fistula L Thrill",
        "AV Fistula R Bruit",
        "AV Fistula R Thrill"
    ],

    # Temperature Management
    "temperature_management": [
        "Arctic Sun/Alsius Temp",
        "Arctic Sun/Alsius Set Temp",
        "Arctic Sun Water Temp",
        "Arctic Sun Temp Location",
        "Cooling Device",
        "Shivering Assessment"
    ],

    # Mobility & Strength Assessment
    "mobility_strength": [
        "LL Strength/Movement",
        "LU Strength/Movement",
        "RL Strength/Movement",
        "RU Strength/Movement",
        "Activity Tolerance",
        "Range of Motion",
        "Range of Motion Location",
        "Range of Motion Status"
    ],

    # Functional Assessment - AM-PAC
    "functional_assessment": [
        "Basic Mobility (AM-PAC)",
        "Discharge Recommendations (AM-PAC)",
        "Activity / Mobility (JH-HLM)",
        "Sit to Stand",
        "Rolling",
        "Supine / Side-lying to Sit",
        "Turn"
    ],

    # Aerobic Capacity
    "aerobic_capacity": [
        "Rest HR - Aerobic Capacity",
        "Rest RR - Aerobic Capacity",
        "Rest O2 Sat - Aerobic Capacity",
        "Activity HR - Aerobic Capacity",
        "Activity RR - Aerobic Capacity",
        "Activity O2 Sat - Aerobic Capacity",
        "Recovery HR - Aerobic Capacity",
        "Recovery RR - Aerobic Capacity",
        "Recovery O2 Sat - Aerobic Capacity"
    ],

    # Fall Risk Assessment
    "fall_risk": [
        "History of falling (within 3 mnths)",
        "History of slips / falls",
        "High risk (>51) interventions",
        "Unintentional weight loss >10 lbs.",
        "Visual / hearing deficit",
        "Gait/Transferring",
        "Ambulatory aid"
    ],

    # Braden Scale (Pressure Ulcer Risk)
    "braden_scale": [
        "Braden Sensory Perception",
        "Braden Moisture",
        "Braden Activity",
        "Braden Mobility",
        "Braden Nutrition",
        "Braden Friction/Shear"
    ],

    # PAR Score (Post-Anesthesia Recovery)
    "par_score": [
        "PAR-Activity",
        "PAR-Respiration",
        "PAR-Circulation",
        "PAR-Consciousness",
        "PAR-Oxygen saturation",
        "PAR-Remain sedated"
    ],

    # Lung Sounds
    "lung_sounds": [
        "LUL Lung Sounds",
        "LLL Lung Sounds",
        "RUL Lung Sounds",
        "RLL Lung Sounds"
    ],

    # Sputum Assessment
    "sputum": [
        "Sputum Amount",
        "Sputum Color",
        "Sputum Consistency",
        "Sputum Source"
    ],

    # Weight & Fluid Balance
    "weight_fluid": [
        "Daily Weight",
        "Admission Weight (Kg)",
        "Admission Weight (lbs.)",
        "Feeding Weight",
        "Bladder Scan Estimate"
    ],

    # Skin Assessment
    "skin_assessment": [
        "Skin Color",
        "Skin Temperature",
        "Skin Condition",
        "Skin Integrity",
        "Edema Amount",
        "Edema Location"
    ],

    # Wound/Pressure Ulcer
    "wound_assessment": [
        "Pressure Ulcer",
        "Impaired Skin",
        "Impaired Skin Type",
        "Impaired Skin Width",
        "Impaired Skin Wound",
        "Impaired Skin Treatment",
        "Tunneling Present"
    ],

    # Incision Assessment
    "incision": [
        "Incision",
        "Incision Site",
        "Incision Appearance",
        "Incision Drainage",
        "Incision Drainage Amount",
        "Incision Dressing",
        "Incision Closure",
        "Incision Cleansing"
    ],

    # GI Assessment
    "gi_assessment": [
        "Bowel Sounds",
        "Nares L",
        "Nares R",
        "Appetite",
        "Difficulty swallowing"
    ],

    # Stool Assessment
    "stool": [
        "Stool Color",
        "Stool Consistency",
        "Stool Guaiac",
        "Stool Guaiac QC",
        "Flatus"
    ],

    # GI Tube Monitoring
    "gi_tube": [
        "GI Tube",
        "GI Intub",
        "GI pH",
        "GI Guaiac",
        "GI Guaiac QC"
    ],

    # Urine Assessment
    "urine_assessment": [
        "Urine Color",
        "Urine Appearance",
        "Urine Source",
        "PH (dipstick)",
        "Specific Gravity (urine)"
    ],

    # Emesis
    "emesis": [
        "Emesis Appearance"
    ],

    # Ostomy
    "ostomy": [
        "Ostomy",
        "Ostomy Appearance"
    ],

    # IABP Monitoring
    "iabp": [
        "Intra Aortic Balloon Pump Setting",
        "IABP Trigger",
        "IABP Mean",
        "IABP Balloon Waveform",
        "IABP Art. Waveform Appear",
        "IABP Arterial Waveform Source",
        "Assisted Systole",
        "Augmented Diastole",
        "Unassisted Systole",
        "Plateau Pressure (IABP)",
        "BAEDP"
    ],

    # Temporary Pacemaker
    "temp_pacemaker": [
        "Temporary Pacemaker Type",
        "Temporary Pacemaker Mode",
        "Temporary Pacemaker Rate",
        "Temporary Atrial Capture",
        "Temporary Ventricular Capture",
        "Temporary Atrial Sens",
        "Temporary Ventricular Sens",
        "Temporary Atrial Stim Setting mA",
        "Temporary Ventricular Stim Setting mA",
        "Temporary Atrial Sens Setting mV",
        "Temporary Ventricular Sens Setting mV",
        "Temporary Atrial Stim Threshold mA",
        "Temporary Venticular Stim Threshold mA",
        "Temporary Atrial Sens Threshold mV",
        "Temporary Venticular Sens Threshold mV",
        "Temporary AV interval"
    ],

    # Permanent Pacemaker
    "permanent_pacemaker": [
        "Permanent Pacemaker Mode"
    ],

    # Transcutaneous Pacing
    "transcutaneous_pacing": [
        "Transcutaneous Pacer Placement",
        "Baseline Current/mA",
        "Current Used/mA"
    ],

    # Neuromuscular Blockade
    "neuromuscular_blockade": [
        "TOF Response",
        "TOF Twitch",
        "NMB Medication",
        "Nerve Stimulated"
    ],

    # BIS Monitoring
    "bis_monitoring": [
        "BIS Index Range",
        "BIS - SQI",
        "BIS - EMG"
    ],

    # Chest Tube
    "chest_tube": [
        "Chest Tube Site",
        "CT Drainage",
        "CT Suction Type",
        "CT Suction Amount",
        "CT Fluctuate",
        "CT Leak",
        "CT Crepitus",
        "CT Dressing"
    ],

    # Pericardial Drain
    "pericardial_drain": [
        "Pericardial Drain Site",
        "Pericardial Drain Status",
        "Pericardial Drain Drainage",
        "Pericardial Drain Aspiration",
        "Pericardial Drain Flush"
    ],

    # Neuro Drain
    "neuro_drain": [
        "Neuro Drain",
        "Neuro Mon Line Type"
    ],

    # Bladder Management
    "bladder": [
        "Bladder Pressure",
        "Bladder scanned",
        "Bladder Irrigation"
    ],

    # Dialysis/CRRT Parameters
    "dialysis_crrt": [
        "CRRT mode",
        "Blood Flow (ml/min)",
        "Dialysate Fluid",
        "Dialysate Rate",
        "Replacement Fluid",
        "Replacement Rate",
        "Post Filter Replacement Rate",
        "PBP (Prefilter) Replacement Rate",
        "Ultrafiltrate Output",
        "Hourly Patient Fluid Removal",
        "Return Pressure",
        "Access Pressure",
        "Filter Pressure",
        "Effluent Pressure",
        "Trans Membrane Pressure",
        "Pressure Drop",
        "Reason for CRRT Filter Change",
        "Hemodialysis Output"
    ],

    # Citrate Anticoagulation
    "citrate": [
        "Citrate (ACD-A)"
    ],

    # PiCCO Monitoring
    "picco": [
        "Calibrated (PiCCO)",
        "CFI (PiCCO)",
        "GEDI (PiCCO)",
        "ELWI (PiCCO)"
    ],

    # CCO (Continuous Cardiac Output)
    "cco": [
        "Blood Temperature CCO (C)"
    ],

    # PCA (Patient Controlled Analgesia)
    "pca": [
        "PCA medication",
        "PCA concentrations",
        "PCA dose",
        "PCA  dose units",
        "PCA bolus",
        "PCA bolus units",
        "PCA lockout (min)",
        "PCA 1 hour limit",
        "PCA 1 hour limit units",
        "PCA basal rate (mL/hour)",
        "PCA attempt",
        "PCA inject",
        "PCA total dose",
        "PCA total dose units",
        "PCA cleared"
    ],

    # Epidural
    "epidural": [
        "Epidural Location",
        "Epidural Medication",
        "Epidural Appearance",
        "Epidural Infusion Rate (mL/hr)",
        "Epidural Bolus (mL)",
        "Epidural Total Dose (mL)"
    ],

    # Medication Administration
    "medication_admin": [
        "MDI #1 Drug",
        "MDI #1 Puff",
        "MDI #2 Drug",
        "MDI #2 Puff",
        "Small Volume Neb Drug/Dose #1",
        "Small Volume Neb Drug #2",
        "Cont Neb - Med",
        "Cont. Neb Med Dose"
    ],

    # Heparin
    "heparin": [
        "Heparin Dose (per hour)"
    ],

    # Lab Values - Commonly Monitored
    "labs_monitored": [
        "Glucose (serum)",
        "Glucose (whole blood)",
        "Glucose finger stick (range 70-100)",
        "Potassium (serum)",
        "Potassium (whole blood)",
        "Sodium (serum)",
        "Sodium (whole blood)",
        "Ionized Calcium",
        "Calcium non-ionized",
        "Magnesium",
        "Phosphorous",
        "Chloride (serum)",
        "Chloride (whole blood)",
        "HCO3 (serum)",
        "Hemoglobin",
        "Hematocrit (serum)",
        "Hematocrit (whole blood - calc)",
        "Platelet Count",
        "WBC",
        "Creatinine (serum)",
        "BUN",
        "Lactic Acid",
        "Lactate"
    ],

    # Lab Values - Cardiac
    "labs_cardiac": [
        "Troponin-T",
        "CK (CPK)",
        "CK-MB",
        "CK-MB fraction (%)",
        "Brain Natiuretic Peptide (BNP)"
    ],

    # Lab Values - Liver
    "labs_liver": [
        "ALT",
        "AST",
        "Alkaline Phosphate",
        "Total Bilirubin",
        "Direct Bilirubin",
        "Albumin",
        "Total Protein",
        "Ammonia"
    ],

    # Lab Values - Pancreas
    "labs_pancreas": [
        "Amylase",
        "Lipase"
    ],

    # Lab Values - Coagulation
    "labs_coagulation": [
        "PT",
        "PTT",
        "INR",
        "Prothrombin time",
        "Fibrinogen",
        "Thrombin",
        "Activated Clotting Time"
    ],

    # Lab Values - Inflammation
    "labs_inflammation": [
        "C Reactive Protein (CRP)",
        "Sed Rate"
    ],

    # Lab Values - Other Chemistry
    "labs_other": [
        "LDH",
        "Anion gap",
        "Serum Osmolality",
        "Uric Acid",
        "Cortisol"
    ],

    # Lab Values - Lipids
    "labs_lipids": [
        "Cholesterol",
        "Triglyceride",
        "HDL",
        "LDL calculated",
        "LDL measured"
    ],

    # Lab Values - Drug Levels
    "labs_drug_levels": [
        "Vancomycin (Trough)",
        "Vancomycin (Random)",
        "Tobramycin (Peak)",
        "Tobramycin (Random)",
        "Phenytoin (Dilantin)",
        "Phenobarbital",
        "Digoxin"
    ],

    # Lab Values - Differential
    "labs_differential": [
        "Absolute Count - Neuts",
        "Absolute Count - Lymphs",
        "Absolute Count - Monos",
        "Absolute Count - Eos",
        "Absolute Count - Basos",
        "Absolute Neutrophil Count",
        "Differential-Neuts",
        "Differential-Lymphs",
        "Differential-Monos",
        "Differential-Eos",
        "Differential-Basos",
        "Differential-Bands",
        "Differential-Atyps",
        "Differential - Immature Granulocytes"
    ],

    # Safety & Monitoring
    "safety_alarms": [
        "Alarms On",
        "Heart rate Alarm - High",
        "Heart Rate Alarm - Low",
        "SpO2 Desat Limit"
    ],

    # Activity & Self-Care
    "activity_selfcare": [
        "Activity",
        "Self ADL",
        "Bath",
        "Bed Bath",
        "UE Bathing",
        "Grooming",
        "Back Care",
        "Skin Care",
        "Eye Care",
        "Trach Care",
        "Cough/Deep Breath",
        "Incentive Spirometry",
        "Chest PT R/L"
    ],

    # Restraints & Safety Devices
    "restraints_safety": [
        "Restraint (Non-violent)",
        "Restraint Ordered (Non-violent)",
        "Restraint Device (Non-violent)",
        "Restraint Location",
        "Reason for Restraint (Non-violent)",
        "Restraints Evaluated",
        "Less Restrictive Measures",
        "Side  Rails",
        "Side Rails"
    ],

    # Positioning & Equipment
    "positioning": [
        "Head of Bed",
        "Balance",
        "Traction/Immobile #1",
        "PT Splint Location",
        "Cervical Collar Type",
        "Cervical Collar Status",
        "Collar Care"
    ],

    # Anti-Embolic Devices
    "antiembolic": [
        "Anti Embolic Device",
        "Anti Embolic Device Status",
        "Compression device"
    ],

    # Prophylaxis
    "prophylaxis": [
        "DVT Prophy",
        "GI Prophy",
        "VAP - Prophy",
        "Glucose Control - Prophy"
    ],

    # Ventilator Circuit & Humidification
    "vent_circuit": [
        "Circuit Changed",
        "Humidification",
        "Humidifier Water % Fill Level",
        "Humidifier Water Changed",
        "Inspired Gas Temp.",
        "In-line Suction Catheter Changed",
        "Subglottal Suctioning",
        "Ventilator Tank"
    ],

    # Spontaneous Breathing Trial
    "sbt": [
        "SBT"
    ],

    # Oxygen Delivery (Non-Ventilated)
    "oxygen_delivery": [
        "Required O2",
        "Alveolar-arterial Gradient"
    ],

    # Arterial Line Management
    "arterial_line": [
        "Arterial Line Discontinued",
        "Arterial Line placed in outside facility",
        "Arterial line Site Appear",
        "Arterial Line Dressing Occlusive",
        "Arterial line Waveform Appear",
        "Arterial Line Zero/Calibrate",
        "Arterial Line Tip Cultured",
        "ART Lumen Volume"
    ],

    # Central Lines - Multi Lumen
    "central_line_multilumen": [
        "Multi Lumen Line Discontinued",
        "Multi Lumen placed in outside facility",
        "Multi Lumen Placement Confirmed by X-ray",
        "Multi Lumen Site Appear",
        "Multi Lumen Dressing Occlusive",
        "Multi Lumen Waveform Appear",
        "Multi Lumen Zero/Calibrate",
        "Multi Lumen Line Tip Cultured"
    ],

    # Central Lines - Cordis/Introducer
    "central_line_cordis": [
        "Cordis/Introducer Discontinued",
        "Cordis/Introducer placed in outside facility",
        "Cordis/Introducer Placement Confirmed by X-ray",
        "Cordis/Introducer Site Appear",
        "Cordis/Introducer Dressing Occlusive",
        "Cordis/Introducer Line Tip Cultured"
    ],

    # Central Lines - Dialysis Catheter
    "dialysis_catheter": [
        "Dialysis Catheter Discontinued",
        "Dialysis Catheter placed in outside facility",
        "Dialysis Catheter Placement Confirmed by X-ray",
        "Dialysis Catheter Site Appear",
        "Dialysis Catheter Dressing Occlusive",
        "Dialysis Catheter Tip Cultured",
        "Dialysis Catheter Type",
        "Dialysis patient"
    ],

    # PICC Line
    "picc_line": [
        "PICC Line Discontinued",
        "PICC Line placed in outside facility",
        "PICC Line Placement Confirmed by X-ray",
        "PICC Line Site Appear",
        "PICC Line Dressing Occlusive",
        "PICC Line Tip Cultured",
        "PICC Line Power PICC",
        "PICC - Heparin Dependent"
    ],

    # Midline
    "midline": [
        "Midline Discontinued",
        "Midline placed in outside facility",
        "Midline Placement Confirmed by X-ray",
        "Midline Site Appear",
        "Midline Dressing Occlusive",
        "Midline Tip Cultured"
    ],

    # Peripheral IV
    "peripheral_iv": [
        "Gauge Reason Discontinued",
        "Gauge placed in outside facility",
        "Gauge placed in the field",
        "Gauge Site Appear",
        "Gauge Dressing Occlusive",
        "G Infiltration Scale",
        "G Phlebitis Scale",
        "IV/Saline lock"
    ],

    # Intraosseous
    "intraosseous": [
        "IO Placed in outside facility",
        "IO Site Appearance",
        "IO Dressing",
        "IO Wristband in place"
    ],

    # Port
    "port": [
        "Indwelling (PortaCath) Port",
        "Indwelling (PortaCath) Port Type",
        "Indwelling Port (PortaCath) placed in outside facility",
        "Indwelling Port (PortaCath) Site Appear",
        "Indwelling Port (PortaCath) Dressing Occlusive",
        "Indwelling Port (PortaCath) Power Port"
    ],

    # PA Catheter
    "pa_catheter": [
        "PA Catheter Discontinued",
        "PA Catheter placed in outside facility",
        "PA Catheter Placement Confirmed by X-ray",
        "PA Catheter Site Appear",
        "PA Catheter Dressing Occlusive",
        "PA Catheter Waveform Appear",
        "PA Catheter Zero/Calibrate",
        "PA Catheter Line Tip Cultured",
        "PA Line cm Mark"
    ],

    # CCO PAC
    "cco_pac": [
        "CCO PAC Discontinued",
        "CCO PAC placed in outside facility",
        "CCO PAC Placement Confirmed by X-ray",
        "CCO PAC Site Appear",
        "CCO PAC Dressing Occlusive",
        "CCO PAC Waveform Appear",
        "CCO PAC Zero/Calibrate"
    ],

    # AVA Line
    "ava_line": [
        "AVA Line placed in outside facility",
        "AVA Line Placement Confirmed by X-ray",
        "AVA Line Site Appear",
        "AVA Dressing Occlusive",
        "AVA Waveform Appearance",
        "AVA Line Zero/Calibrate",
        "AVA Line Tip Cultured",
        "VEN Lumen Volume"
    ],

    # Sheath
    "sheath": [
        "Sheath Line Discontinued",
        "Sheath placed in outside facility",
        "Sheath Placement Confirmed by X-ray",
        "Sheath Site Appear",
        "Sheath Dressing Occlusive",
        "Sheath Waveform Appear",
        "Sheath Zero/Calibrate",
        "Sheath Size"
    ],

    # Trauma Line
    "trauma_line": [
        "Trauma Line Discontinued",
        "Trauma Line placed in outside facility",
        "Trauma Line Placement Confirmed by X-ray",
        "Trauma Line Site Appear",
        "Trauma Line Dressing Occlusive",
        "Trauma Line Tip Cultured"
    ],

    # Pheresis Catheter
    "pheresis": [
        "Pheresis Catheter placed in outside facility",
        "Pheresis Catheter Placement Confirmed by X-ray",
        "Pheresis Catheter Site Appear",
        "Pheresis Catheter Type"
    ],

    # ICP Line
    "icp_line": [
        "ICP Line placed in outside facility",
        "ICP Line Site Appear",
        "ICP Line Dressing Occlusive",
        "ICP Line Waveform Appear",
        "ICP Line Zero/Calibrate",
        "ICP Line Tip Cultured"
    ],

    # IABP Line Management
    "iabp_line": [
        "IABP Line Discontinued",
        "IABP placed in outside facility",
        "IABP Placement Confirmed by X-ray",
        "IABP Site Appear",
        "IABP Dressing Occlusive",
        "IABP Position on leg",
        "IABP Size",
        "IABP Helium Tubing",
        "IABP Power Source",
        "IABP Alarms Activated",
        "IABP Zero/Calibrate"
    ],

    # LE Dressing (Lower Extremity)
    "le_dressing": [
        "LE Dressing"
    ],

    # Angio Site
    "angio": [
        "Angio Site",
        "Angio Appearance",
        "Angio Dressing"
    ],

    # Urinary Catheter
    "urinary_catheter": [
        "GU Catheter Size",
        "Foley Cath Insertion Location",
        "Indwelling Urinary Catheter Care",
        "Urinal/Bedpan"
    ],

    # Lines/Tubes Summary
    "lines_tubes": [
        "Lines/Tubes",
        "Line Type",
        "Intravenous  / IV access prior to admission"
    ],

    # Dressing General
    "dressing": [
        "Dressing Status"
    ],

    # Assistance Devices
    "assistance_devices": [
        "Assistance Device"
    ],

    # Insulin Pump
    "insulin_pump": [
        "Insulin pump"
    ],

    # Temporary Pacemaker Wires
    "temp_pacer_wires": [
        "Temporary Pacemaker Wire Condition",
        "Temporary Pacemaker Wires Atrial",
        "Temporary Pacemaker Wires Venticular"
    ],

    # Critically Ill Status
    "critical_status": [
        "Critically ill"
    ],

    # Sedation Management
    "sedation_mgmt": [
        "Daily Wake Up",
        "Daily Wake Up Deferred"
    ],

    # Acuity & Workload
    "acuity": [
        "Acuity Workload Question 1",
        "Acuity Workload Question 2"
    ],

    # Mobilization
    "mobilization": [
        "Mobilization Plan"
    ],

    # Blood Transfusion
    "transfusion": [
        "Blood Transfusion Consent"
    ],

    # CAUTI Prevention
    "cauti": [
        "CAUTI Info Given"
    ],

    # CHG Bath
    "chg_bath": [
        "CHG Bath"
    ],

    # Apnea
    "apnea": [
        "Apnea Interval"
    ],

    # Febrile
    "fever": [
        "Febrile last 24 hours"
    ],

    # Insomnia
    "sleep": [
        "Insomnia"
    ],

    # Slurred Speech
    "speech": [
        "Slurred Speech"
    ],

    # CO2 Production
    "co2_production": [
        "CO2 production"
    ],

    # NICOM - Leg Raise
    "nicom_tests": [
        "Leg Raise Result (NICOM)"
    ],

    # Swallow Assessment - OCAT
    "swallow_assessment": [
        "OCAT - Teeth",
        "OCAT - Lips Tongue Gums Palate",
        "OCAT - Saliva secretions, Voice quality",
        "OCAT - Swallow"
    ],

    # Nutrition & Diet
    "nutrition_diet": [
        "Nutrition",
        "Diet Type",
        "Food and Fluid",
        "Home TF"
    ],

    # Vascular Assessment
    "vascular_general": [
        "Vascular"
    ],

    # Cardiovascular Assessment
    "cardiovascular_general": [
        "Cardiovascular",
        "CV - past medical history"
    ],

    # Physical Exam Systems
    "physical_exam": [
        "HEENT",
        "Exam-Ext/MSK",
        "Exam-GU",
        "Exam-Neuro"
    ],

    # Constitutional
    "constitutional": [
        "Constitutional"
    ],

    # Abdominal Assessment
    "abdominal": [
        "Abdominal - (GI / Hepatic / Renal)",
        "Abdominal Assessment"
    ],

    # Social & Safety History
    "social_history": [
        "Living situation",
        "Recreational drug use",
        "ETOH",
        "Any fear in relationships",
        "Sexuality / reproductive problems"
    ],

    # Medications
    "medications": [
        "All Medications Tolerated without Adverse Side Effects",
        "Untoward Effect",
        "Medication Bolus - Adjunctive Pain Management"
    ],

    # Height
    "anthropometrics": [
        "Height"
    ]
}


# Helper function to find category
def get_vital_category(vital_name):
    """Returns the category(ies) a vital sign belongs to"""
    categories = []
    for category, vitals in vitals_categories.items():
        if vital_name in vitals:
            categories.append(category)
    return categories if categories else ["uncategorized"]


# Example usage
if __name__ == "__main__":

    print(f"\n{'=' * 60}")
    print(f"SUMMARY STATISTICS")
    print(f"{'=' * 60}")
    print(f"Total Categories: {len(vitals_categories)}")
    print(f"Total Vitals/Parameters: {sum(len(v) for v in vitals_categories.values())}")

    # Count by major category type
    basic_count = len(vitals_categories['basic_vitals'])
    neuro_categories = [k for k in vitals_categories.keys() if 'neuro' in k.lower()]
    neuro_count = sum(len(vitals_categories[k]) for k in neuro_categories)

    print(f"\nBasic Vital Signs: {basic_count}")
    print(f"Neurological Parameters: {neuro_count}")
    print(f"Lab Values Included: {sum(len(vitals_categories[k]) for k in vitals_categories.keys() if 'labs' in k)}")