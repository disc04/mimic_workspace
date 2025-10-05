

"""

Test Category Organization Logic:
Organ-based: Liver, kidney, cardiac, thyroid, pancreatic tests 
Function-based: Coagulation, inflammation, autoimmune markers
Sample type: Blood gases, urinalysis, body fluids (ascites, pleural, CSF)
Clinical purpose: Infection screening, drug monitoring, tumor markers
Technical groupings: Flow cytometry, morphology, therapeutic drug levels

Dashboard Markers:
Hemoglobin - Anemia/blood loss screening
WBC - Infection/immune status
Platelet Count - Bleeding risk
Creatinine - Kidney function
Glucose - Metabolic/diabetes screening
Sodium/Potassium - Critical electrolytes (life-threatening if abnormal)
ALT - Liver function/injury
Troponin T - Cardiac injury detection
CRP - Inflammation/infection severity

"""
labs_dashboard = ["White_Blood_Cells", "Hemoglobin", "CK-MB"
                  "Alanine_Aminotransferase_(ALT)", "Troponin-T", "C_Reactive_Protein",
                  "Sodium", "Potassium", "Glucose", "Chloride", "Bicarbonate",
                  "Blood_Urea_Nitrogen", "Potassium", "Creatinine"]

additional_dashboard = ["Platelet_Count"]

# Laboratory Tests Categorization Dictionary

lab_categories = {
    # CRITICAL DASHBOARD MARKERS
    "critical_dashboard": [
        "Hemoglobin",
        "White_Blood_Cells",
        "Platelet Count",
        "Creatinine",
        "Glucose",
        "Sodium",
        "Potassium",
        "Alanine Aminotransferase (ALT)",
        "Troponin T",
        "C_Reactive_Protein"
    ],

    # Complete Blood Count (CBC) & Red Cell Indices
    "hematology_rbc": [
        "Red Blood Cells",
        "Hemoglobin",
        "Hematocrit",
        "MCV",
        "MCH",
        "MCHC",
        "RDW",
        "RDW-SD",
        "Reticulocyte Count, Automated",
        "Reticulocyte Count, Absolute"
    ],

    # White Blood Cells & Differential
    "hematology_wbc": [
        "White Blood Cells",
        "Neutrophils",
        "Lymphocytes",
        "Monocytes",
        "Eosinophils",
        "Basophils",
        "Bands",
        "Absolute Neutrophil Count",
        "Absolute Lymphocyte Count",
        "Absolute Monocyte Count",
        "Absolute Eosinophil Count",
        "Absolute Basophil Count",
        "Atypical Lymphocytes",
        "Blasts",
        "Myelocytes",
        "Metamyelocytes",
        "Promyelocytes",
        "Immature Granulocytes",
        "Nucleated Red Cells",
        "Plasma Cells",
        "Granulocyte Count"
    ],

    # Platelets & Coagulation
    "coagulation": [
        "Platelet Count",
        "PT",
        "PTT",
        "INR(PT)",
        "Fibrinogen, Functional",
        "D-Dimer",
        "Fibrin Degradation Products",
        "Bleeding Time",
        "Thrombin",
        "Protein C, Functional",
        "Lupus Anticoagulant"
    ],

    # Blood Cell Morphology
    "cell_morphology": [
        "Platelet Smear",
        "Poikilocytosis",
        "Anisocytosis",
        "Microcytes",
        "Macrocytes",
        "Hypochromia",
        "Polychromasia",
        "Ovalocytes",
        "Teardrop Cells",
        "Spherocytes",
        "Schistocytes",
        "Bite Cells",
        "Acanthocytes",
        "Target Cells",
        "Elliptocytes",
        "Echinocytes",
        "Basophilic Stippling",
        "Pappenheimer Bodies",
        "Howell-Jolly Bodies",
        "Fragmented Cells",
        "RBC Morphology",
        "MacroOvalocytes",
        "H/O Smear",
        "Inpatient Hematology/Oncology Smear"
    ],

    # Basic Metabolic Panel (BMP)
    "electrolytes_bmp": [
        "Sodium",
        "Potassium",
        "Chloride",
        "Bicarbonate",
        "Glucose",
        "Urea Nitrogen",
        "Creatinine",
        "Calcium, Total"
    ],

    # Extended Electrolytes & Minerals
    "electrolytes_extended": [
        "Magnesium",
        "Phosphate",
        "Anion Gap",
        "Sodium, Whole Blood",
        "Potassium, Whole Blood",
        "Chloride, Whole Blood",
        "Calculated Bicarbonate, Whole Blood",
        "Free Calcium"
    ],

    # Renal Function
    "renal_function": [
        "Creatinine",
        "Creatinine, Serum",
        "Creatinine, Whole Blood",
        "Urea Nitrogen",
        "Estimated GFR (MDRD equation)",
        "Creatinine Clearance",
        "Uric Acid",
        "Beta-2 Microglobulin"
    ],

    # Liver Function Tests
    "liver_function": [
        "Alanine Aminotransferase (ALT)",
        "Asparate Aminotransferase (AST)",
        "Alkaline Phosphatase",
        "Bilirubin, Total",
        "Bilirubin, Direct",
        "Bilirubin, Indirect",
        "Albumin",
        "Protein, Total",
        "Globulin",
        "Gamma Glutamyltransferase"
    ],

    # Pancreatic Enzymes
    "pancreatic": [
        "Amylase",
        "Lipase"
    ],

    # Cardiac Markers
    "cardiac": [
        "Troponin T",
        "Creatine Kinase (CK)",
        "Creatine Kinase, MB Isoenzyme",
        "CK-MB Index",
        "Lactate Dehydrogenase (LD)",
        "NTproBNP"
    ],

    # Inflammation Markers
    "inflammation": [
        "C-Reactive Protein",
        "Sedimentation Rate"
    ],

    # Lipid Panel
    "lipids": [
        "Cholesterol, Total",
        "Cholesterol, HDL",
        "Cholesterol, LDL, Calculated",
        "Cholesterol, LDL, Measured",
        "Triglycerides",
        "Cholesterol Ratio (Total/HDL)",
        "Triglycer"
    ],

    # Diabetes Management
    "diabetes": [
        "Glucose",
        "% Hemoglobin A1c",
        "eAG",
        "Glyco A"
    ],

    # Iron Studies
    "iron_studies": [
        "Iron",
        "Ferritin",
        "Transferrin",
        "Iron Binding Capacity, Total",
        "Haptoglobin"
    ],

    # Thyroid Function
    "thyroid": [
        "Thyroid Stimulating Hormone",
        "Thyroxine (T4)",
        "Thyroxine (T4), Free",
        "Triiodothyronine (T3)",
        "Thyroglobulin",
        "Thyroid Peroxidase Antibodies",
        "Anti-Thyroglobulin Antibodies",
        "Uptake Ratio",
        "Calculated TBG",
        "Calculated Thyroxine (T4) Index"
    ],

    # Vitamins & Nutritional
    "vitamins": [
        "Vitamin B12",
        "Folate",
        "25-OH Vitamin D"
    ],

    # Hormones
    "hormones": [
        "Parathyroid Hormone",
        "Cortisol",
        "Prolactin",
        "Human Chorionic Gonadotropin",
        "HCG, Urine, Qualitative"
    ],

    # Tumor Markers
    "tumor_markers": [
        "Prostate Specific Antigen",
        "Alpha-Fetoprotein",
        "Carcinoembyronic Antigen (CEA)",
        "CA-125"
    ],

    # Immunoglobulins & Proteins
    "immunoglobulins": [
        "Immunoglobulin G",
        "Immunoglobulin A",
        "Immunoglobulin M",
        "Protein Electrophoresis",
        "Immunofixation",
        "Free Kappa",
        "Free Lambda",
        "Free Kappa/Free Lambda Ratio",
        "Prot. Electrophoresis, Urine",
        "Immunofixation, Urine"
    ],

    # Autoimmune & Rheumatology
    "autoimmune": [
        "Anti-Nuclear Antibody",
        "Anti-Nuclear Antibody, Titer",
        "Rheumatoid Factor",
        "Anti-Neutrophil Cytoplasmic Antibody",
        "Anticardiolipin Antibody IgG",
        "Anticardiolipin Antibody IgM",
        "Double Stranded DNA",
        "C3",
        "C4",
        "Anti-Smooth Muscle Antibody",
        "Anti-Mitochondrial Antibody",
        "Anti-DGP (IgA/IgG)",
        "Tissue Transglutaminase Ab, IgA"
    ],

    # Infectious Disease Serology
    "infectious_serology": [
        "Hepatitis A Virus Antibody",
        "Hepatitis A Virus IgM Antibody",
        "Hepatitis B Surface Antigen",
        "Hepatitis B Surface Antibody",
        "Hepatitis B Virus Core Antibody",
        "Hepatitis C Virus Antibody",
        "HIV Screen",
        "Treponema pallidum (Syphilis) Ab",
        "Treponema pallidum (syphilis) value"
    ],

    # Molecular Diagnostics/PCR
    "molecular": [
        "Influenza A by PCR",
        "Influenza B by PCR",
        "Chlamydia trachomatis",
        "Neisseria gonorrhoeae",
        "Trichomonas vaginalis",
        "HIV 1 Viral Load",
        "Hepatitis C Viral Load",
        "Cytomegalovirus Viral Load",
        "Norovirus Genogroup I",
        "Norovirus Genogroup II"
    ],

    # Flow Cytometry/Immunophenotyping
    "flow_cytometry": [
        "Immunophenotyping",
        "CD2", "CD3", "CD4", "CD5", "CD7", "CD8",
        "CD10", "CD11c", "CD13", "CD14", "CD15",
        "CD19", "CD20", "CD33", "CD34", "CD41",
        "CD45", "CD56", "CD64", "CD71", "CD117",
        "HLA-DR", "Kappa", "Lambda",
        "CD3 Cells, Percent",
        "CD4 Cells, Percent",
        "CD8 Cells, Percent",
        "Absolute CD3 Count",
        "Absolute CD4 Count",
        "Absolute CD8 Count",
        "CD4/CD8 Ratio",
        "WBC Count",
        "Lymphocytes, Percent"
    ],

    # Hemoglobin Variants
    "hemoglobin_variants": [
        "Hemogloblin A",
        "Hemoglobin C",
        "Hemogloblin S",
        "G6PD, Qualitative",
        "Quantitative G6PD"
    ],

    # Arterial Blood Gas (ABG)
    "blood_gas": [
        "pH",
        "pO2",
        "pCO2",
        "Oxygen Saturation",
        "Base Excess",
        "Calculated Total CO2",
        "Lactate",
        "Free Calcium",
        "Bicarbonate",
        "Carboxyhemoglobin",
        "Methemoglobin",
        "Required O2",
        "Alveolar-arterial Gradient"
    ],

    # Urinalysis
    "urinalysis": [
        "Urine Color",
        "Urine Appearance",
        "Specific Gravity",
        "pH",
        "Protein",
        "Glucose",
        "Ketone",
        "Blood",
        "Bilirubin",
        "Urobilinogen",
        "Nitrite",
        "Leukocytes",
        "WBC",
        "RBC",
        "Epithelial Cells",
        "Bacteria",
        "Yeast",
        "Urine Mucous",
        "Blood, Occult"
    ],

    # Urine Microscopy & Casts
    "urine_microscopy": [
        "Hyaline Casts",
        "Granular Casts",
        "Waxy Casts",
        "Calcium Oxalate Crystals",
        "Triple Phosphate Crystals",
        "Uric Acid Crystals",
        "Amorphous Crystals",
        "Urine Crystals, Other",
        "Transitional Epithelial Cells",
        "Renal Epithelial Cells",
        "WBC Clumps",
        "NonSquamous Epithelial Cell",
        "Envelope Cells"
    ],

    # 24-Hour Urine & Urine Chemistry
    "urine_chemistry": [
        "Creatinine, Urine",
        "Urine Creatinine",
        "24 hr Creatinine",
        "Urea Nitrogen, Urine",
        "Sodium, Urine",
        "Potassium, Urine",
        "Chloride, Urine",
        "Calcium, Urine",
        "Phosphate, Urine",
        "Magnesium, Urine",
        "Uric Acid, Urine",
        "Total Protein, Urine",
        "Albumin, Urine",
        "Albumin/Creatinine, Urine",
        "Protein/Creatinine Ratio",
        "Osmolality, Urine",
        "Bicarbonate, Urine",
        "Urine Volume",
        "Urine Volume, Total",
        "Length of Urine Collection",
        "Total Collection Time"
    ],

    # Toxicology & Drug Screening
    "toxicology": [
        "Ethanol",
        "Acetaminophen",
        "Salicylate",
        "Cocaine, Urine",
        "Opiate Screen, Urine",
        "Amphetamine Screen, Urine",
        "Benzodiazepine Screen",
        "Benzodiazepine Screen, Urine",
        "Barbiturate Screen",
        "Barbiturate Screen, Urine",
        "Tricyclic Antidepressant Screen",
        "Methadone, Urine",
        "Marijuana",
        "Oxycodone",
        "Fentanyl"
    ],

    # Therapeutic Drug Monitoring
    "drug_levels": [
        "Vancomycin",
        "Phenytoin",
        "Phenobarbital",
        "Carbamazepine",
        "Digoxin",
        "Lithium",
        "tacroFK",
        "Tobramycin"
    ],

    # Body Fluid Analysis - Ascites
    "ascites": [
        "Total Nucleated Cells, Ascites",
        "RBC, Ascites",
        "Polys",
        "Lymphs",
        "Monos",
        "Mesothelial Cell",
        "Macrophage",
        "Total Protein, Ascites",
        "Albumin, Ascites",
        "Glucose, Ascites",
        "Lactate Dehydrogenase, Ascites",
        "Bilirubin, Total, Ascites",
        "Amylase, Ascites",
        "Creatinine, Ascites",
        "Hematocrit, Ascites",
        "Cholesterol, Ascites"
    ],

    # Body Fluid Analysis - Pleural
    "pleural": [
        "Total Nucleated Cells, Pleural",
        "RBC, Pleural",
        "Total Protein, Pleural",
        "Albumin, Pleural",
        "Glucose, Pleural",
        "Lactate Dehydrogenase, Pleural",
        "Amylase, Pleural",
        "Cholesterol, Pleural",
        "Creatinine, Pleural",
        "Miscellaneous, Pleural"
    ],

    # Body Fluid Analysis - CSF
    "csf": [
        "Total Nucleated Cells, CSF",
        "RBC, CSF",
        "Glucose, CSF",
        "Total Protein, CSF",
        "Lymphs"
    ],

    # Body Fluid Analysis - Joint
    "joint_fluid": [
        "Total Nucleated Cells, Joint",
        "RBC, Joint Fluid",
        "Hematocrit, Joint Fluid",
        "Joint Crystals, Number"
    ],

    # Body Fluid Analysis - Other
    "body_fluid_other": [
        "Total Nucleated Cells, Other",
        "RBC, Other Fluid",
        "Hematocrit, Other Fluid",
        "Total Protein, Body Fluid",
        "Albumin, Body Fluid",
        "Glucose, Body Fluid",
        "LD, Body Fluid",
        "Amylase, Body Fluid",
        "Bilirubin, Total, Body Fluid",
        "Miscellaneous, Body Fluid",
        "Macrophages",
        "Mesothelial Cells",
        "Mesothelial cells",
        "Other Cell",
        "Other Cells"
    ],

    # Miscellaneous Chemistry
    "misc_chemistry": [
        "Osmolality, Measured",
        "Ammonia",
        "Lactate"
    ],

    # Ventilator Settings
    "ventilator": [
        "Temperature",
        "Oxygen",
        "O2 Flow",
        "PEEP",
        "Tidal Volume",
        "Ventilation Rate",
        "Assist/Control",
        "Ventilator",
        "Intubated"
    ],

    # Specimen Information & Quality Indicators
    "specimen_info": [
        "Specimen Type",
        "Urine Specimen Type",
        "Voided Specimen",
        "Problem Specimen",
        "Other"
    ],

    # Sample Holds/Storage
    "sample_holds": [
        "Green Top Hold (plasma)",
        "Red Top Hold",
        "Light Green Top Hold",
        "Blue Top Hold",
        "EDTA Hold",
        "Uhold",
        "Urine tube, held",
        "Plasma",
        "Anat Path Hold"
    ],

    # Platelet Function
    "platelet_function": [
        "Collagen",
        "ADP",
        "Arachadonic Acid"
    ],

    # Heparin Monitoring
    "heparin": [
        "Heparin",
        "Heparin, LMW"
    ],

    # Microbiology
    "microbiology": [
        "Blood Parasite Smear"
    ],

    # Undefined/Coded Values
    "undefined_codes": [
        "L", "H", "I",
        "HPE1", "HPE2", "HPE3", "HPE4", "HPE7",  # Histopathology probably
        "STX1", "STX2", "STX3", "STX4", "STX5", "STX6",
        "UTX1", "UTX2", "UTX3", "UTX4", "UTX5", "UTX6", "UTX7", "UTX9", "UTX10",
        "PAN1", "PAN2", "PAN3",
        "EE2", "ARCH-1", "RFXLDLM", "XUCU", "UCU2", "wbcp"

    ]
}


# Helper function to get category of a test
def get_test_category(test_name):
    """Returns the category(ies) a test belongs to"""
    categories = []
    for category, tests in lab_categories.items():
        if test_name in tests:
            categories.append(category)
    return categories if categories else ["uncategorized"]


# Example usage
if __name__ == "__main__":
    print("Top 10 Critical Dashboard Markers:")
    for i, test in enumerate(lab_categories["critical_dashboard"], 1):
        print(f"{i}. {test}")

    print(f"\n\nTotal Categories: {len(lab_categories)}")
    print(f"Total Tests Categorized: {sum(len(tests) for tests in lab_categories.values())}")
