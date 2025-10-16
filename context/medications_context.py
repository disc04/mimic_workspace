import re

# Medication Categorization Dictionary
medications_categories = {
    # Sedatives & Analgesics
    "sedatives_analgesics": [
        "Fentanyl Citrate", "Fentanyl Patch", "Fentanyl PCA", "Fentanyl (Concentrate)"
        "Lorazepam", "Midazolam", "Midazolam (Versed)", "Diazepam", "Diazepam (Valium)",
        "ALPRAZolam", "ClonazePAM",
        "Propofol", "Dexmedetomidine", "Dexmedetomidine (Precedex)", "Etomidate", "Ketamine",
        "HYDROmorphone", "HYDROmorphone (Dilaudid)", "HYDROmorphone-HP", "Hydromorphone (Dilaudid)",
        "Morphine Sulfate", "Morphine Sulfate IR", "Morphine SR (MS Contin)",
        "Morphine Sulfate (Oral Solution) 2 mg/mL", "Morphine Sulfate (Oral Soln.)",
        "OxyCODONE (Immediate Release)", "OxycoDONE", "OxyCODONE SR (OxyconTIN)",
        "OxycoDONE Liquid", "Methadone", "Methadone Hydrochloride", "TraMADOL", "TraMADol (Ultram)",
        "Meperidine", "Acetaminophen w/Codeine"
    ],

    # Combination Analgesics
    "combination_analgesics": [
        "OxyCODONE--Acetaminophen (5mg-325mg)", "Oxycodone-Acetaminophen",
        "Oxycodone-Acetaminophen (5mg-325mg)", "OxycoDONE-Acetaminophen Elixir",
        "Hydrocodone-Acetaminophen", "HYDROcodone-Acetaminophen (5mg-325mg)",
        "Hydrocodone-Acetaminophen (5mg-500mg)", "Acetaminophen-Caff-Butalbital",
        "Guaifenesin-CODEINE Phosphate", "Acetaminophen-IV"
    ],

    # Non-Opioid Analgesics & NSAIDs
    "nsaids_analgesics": [
        "Acetaminophen", "Acetaminophen (Liquid)", "Acetaminophen IV",
        "Ibuprofen", "Ibuprofen Suspension", "Ketorolac", "Naproxen",
        "Indomethacin"
    ],

    # Insulin & Diabetes
    "insulin_diabetes": [
        "Insulin", "Insulin Pump (Self Administering Medication)",
        "Insulin Human Regular", "Insulin Regular Human (U-500)", "Insulin - Regular",
        "Insulin (Regular) for Hyperkalemia", "HumaLOG", "Insulin - NPH",
        "Insulin Glargine  (CVICU Protocol)", "Lantus", "Insulin - Glargine",
        "MetFORMIN (Glucophage)", "MetFORMIN XR (Glucophage XR)",
        "GlyBURIDE", "GlipiZIDE", "GlipiZIDE XL",
        "Insulin Syringe U-500"
    ],

    # Antibiotics - Penicillins
    "antibiotics_penicillins": ["Ampicillin",
        "Ampicillin Sodium", "Ampicillin-Sulbactam", "Amoxicillin",
        "Amoxicillin-Clavulanic Acid", "Piperacillin-Tazobactam", "Piperacillin"
    ],

    # Antibiotics - Cephalosporins
    "antibiotics_cephalosporins": [
        "CefazoLIN", "CefePIME", "CefTRIAXone", "CefTAZidime",
        "Cephalexin", "Cefpodoxime Proxetil"
    ],

    # Antibiotics - Fluoroquinolones
    "antibiotics_fluoroquinolones": [
        "Levofloxacin", "Ciprofloxacin HCl", "Ciprofloxacin",
        "Ciprofloxacin IV", "moxifloxacin"
    ],

    # Antibiotics - Glycopeptides
    "antibiotics_glycopeptides": [
        "Vancomycin", "Vancomycin Oral Liquid", "Vancomycin Enema"
    ],

    # Antibiotics - Carbapenems
    "antibiotics_carbapenems": [
        "Meropenem", "Ertapenem Sodium", "Aztreonam"
    ],

    # Antibiotics - Macrolides
    "antibiotics_macrolides": [
        "Azithromycin", "Clarithromycin", "Erythromycin"
    ],

    # Antibiotics - Other
    "antibiotics_other": [
        "Sulfameth/Trimethoprim DS", "Sulfameth/Trimethoprim SS",
        "Sulfamethoxazole-Trimethoprin", "Trimethoprim","Bactrim", "Sulfamethoxazole",
        "Linezolid", "Clindamycin", "MetRONIDAZOLE (FLagyl)", "MetroNIDAZOLE", "Metronidazole",
        "Doxycycline Hyclate", "Doxycycline", "Gentamicin", "Tobramycin Sulfate", "Tobramycin",
        "Tigecycline", "Daptomycin", "Nitrofurantoin Monohyd (MacroBID)",
        "Nitrofurantoin (Macrodantin)", "Rifaximin", "Neomycin Sulfate"
    ],

    # Antifungals
    "antifungals": [
        "Fluconazole", "Voriconazole", "Micafungin", "Ambisome",
        "Miconazole 2% Cream", "Miconazole Powder 2%",
        "Miconazole Nitrate Vag Cream 2%", "Clotrimazole", "Clotrimazole Cream",
        "Nystatin", "Nystatin Oral Suspension", "Nystatin Cream",
        "Nystatin-Triamcinolone Cream", "Terbinafine 1% Cream"
    ],

    # Antivirals
    "antivirals": [
        "Acyclovir", "OSELTAMivir", "Amantadine",
        "Darunavir", "RiTONAvir", "Raltegravir",
        "Emtricitabine-Tenofovir (Truvada)", "Stribild"
    ],

    # Anticoagulants
    "anticoagulants": [
        "Heparin", "Heparin Sodium", "Heparin (CRRT Machine Priming)",
        "Heparin (Hemodialysis)", "Heparin (IABP)",
        "Heparin Flush (10 units/ml)", "Heparin Flush (100 units/ml)",
        "Heparin Flush (1000 units/mL)", "Heparin Dwell (1000 Units/mL)",
        "Enoxaparin Sodium", "Enoxaparin (Prophylaxis)", "Enoxaparin (Lovenox)",
        "Warfarin", "Coumadin", "Apixaban", "Rivaroxaban", "Dabigatran Etexilate"
    ],

    # Antiplatelets
    "antiplatelets": [
        "Aspirin", "Aspirin EC", "Aspirin (Buffered)", "Aspirin 81 mg",
        "Clopidogrel", "TiCAGRELOR", "Prasugrel"
    ],

    # Anticoagulation Reversal
    "anticoag_reversal": [
        "Protamine Sulfate", "Phytonadione", "Kcentra",
        "Transfusion of Nonautologous 4-Factor Prothrombin Complex Concentrate into Vein, Percutaneous Approach",
        "Infusion of 4-Factor Prothrombin Complex Concentrate"
    ],

    # Thrombolytics
    "thrombolytics": [
        "Alteplase", "Alteplase (Catheter Clearance)",
        "Alteplase 1mg/2mL ( Clearance ie. PICC, tunneled access line )",
        "Alteplase 1mg/2mL ( Clearance ie. PICC, midline, tunneled access line, PA )"
    ],

    # Hemostatic Agents
    "hemostatic": [
        "Aminocaproic Acid", "Thrombin"
    ],

    # Cardiovascular - Antihypertensives (ACE/ARB)
    "cv_ace_arb": [
        "Lisinopril", "Enalapril Maleate", "Enalaprilat", "Captopril", "Ramipril",
        "Losartan Potassium", "Valsartan", "irbesartan", "Avapro",
        "Sacubitril-Valsartan (24mg-26mg)"
    ],

    # Cardiovascular - Beta Blockers
    "cv_beta_blockers": [
        "Metoprolol Tartrate", "Metoprolol Succinate XL", "Atenolol",
        "Carvedilol", "Propranolol", "Propranolol LA", "Labetalol",
        "Esmolol", "Nadolol", "Sotalol"
    ],

    # Cardiovascular - Calcium Channel Blockers
    "cv_calcium_blockers": [
        "Amlodipine", "NIFEdipine", "NIFEdipine CR", "Diltiazem",
        "Diltiazem Extended-Release", "Verapamil", "Verapamil SR",
        "NiCARdipine", "NiCARdipine IV", "Nicardipine", "Clevidipine",
        "Nimodipine", "Felodipine"
    ],

    # Cardiovascular - Diuretics
    "cv_diuretics": [
        "Furosemide", " Furosemide (Lasix)", "Furosemide-Heart Failure", "Torsemide", "Bumetanide", "Bumetanide (Bumex)"
        "Hydrochlorothiazide", "Chlorthalidone", "Chlorothiazide Sodium",
        "Chlorothiazide", "Spironolactone", "Metolazone",
        "AcetaZOLamide", "AcetaZOLamide Sodium"
    ],

    # Cardiovascular - Nitrates
    "cv_nitrates": [
        "Nitroglycerin", "Nitroglycerin SL", "Nitroglycerin Ointment  2%", "Nitroglycerin",
        "Isosorbide Dinitrate", "Isosorbide Dinitrate ER",
        "Isosorbide Mononitrate", "Isosorbide Mononitrate (Extended Release)"
    ],

    # Cardiovascular - Other Antihypertensives
    "cv_other_antihypertensives": [
        "HydrALAZINE", "CloNIDine", "Clonidine Patch 0.2 mg/24 hr",
        "Clonidine Patch 0.3 mg/24 hr", "Prazosin", "Doxazosin",
        "Midodrine", "Nitroprusside Sodium"
    ],

    # Cardiovascular - Inotropes & Pressors
    "cv_inotropes_pressors": [
        "DOBUTamine", "DOPamine", "Dobutamine", "Dopamine", "Epinephrine", "EPINEPHrine", "Epinephrine 1:1000",
        "NORepinephrine", "Norepinephrine", "PHENYLEPHrine", "Phenylephrine", "Vasopressin", "Milrinone"
    ],

    # Cardiovascular - Antiarrhythmics
    "cv_antiarrhythmics": [
        "Amiodarone", "Digoxin", " Digoxin (Lanoxin)", "Digox", "Dofetilide",
        "quiniDINE Gluconate E.R.", "Lidocaine"
    ],

    # Cardiovascular - Lipid Lowering
    "cv_lipids": [
        "Atorvastatin", "Simvastatin", "Rosuvastatin Calcium", "Pravastatin",
        "Gemfibrozil", "Fenofibrate", "Tricor", "Ezetimibe", "Niacin", "Niacin SR",
        "Fish Oil (Omega 3)"
    ],

    # Cardiovascular - Other
    "cv_other": [
        "Colchicine", "Cinacalcet"
    ],

    # Respiratory - Bronchodilators
    "respiratory_bronchodilators": [
        "Albuterol 0.083% Neb Soln", "Albuterol Inhaler", "Albuterol-Ipratropium",
        "Ipratropium-Albuterol Neb", "Ipratropium-Albuterol Inhalation Spray",
        "Ipratropium Bromide Neb", "Ipratropium Bromide MDI",
        "Levalbuterol Neb", "Xopenex Neb", "Tiotropium Bromide",
        "Racepinephrine"
    ],

    # Respiratory - Corticosteroids
    "respiratory_steroids": [
        "Fluticasone Propionate 110mcg", "Fluticasone Propionate NASAL",
        "Fluticasone-Salmeterol Diskus (100/50)", "Fluticasone-Salmeterol Diskus (250/50)",
        "Fluticasone-Salmeterol Diskus (500/50)", "Salmeterol Xinafoate Diskus (50 mcg)"
    ],

    # GI - Proton Pump Inhibitors
    "gi_ppi": [
        "Omeprazole", "Pantoprazole", " Pantoprazole (Protonix)", "Lansoprazole Oral Disintegrating Tab",
        "Esomeprazole sodium", "NexIUM", "Esomeprazole", "Omeprazole (Prilosec)"
    ],

    # GI - H2 Blockers
    "gi_h2_blockers": [
        "Famotidine", "Famotidine (IV)", "Ranitidine", "Ranitidine (Liquid)"
    ],

    # GI - Antiemetics
    "gi_antiemetics": [
        "Ondansetron", "Ondansetron (Zofran)", "Ondansetron ODT", "Metoclopramide",
        "Prochlorperazine", "Promethazine", "Meclizine",
        "Scopolamine Patch", "Dronabinol"
    ],

    # GI - Laxatives & Bowel Prep
    "gi_laxatives": [
        "Docusate Sodium", "Docusate Sodium (Liquid)", "Docusate",
        "Bisacodyl", "Senna", "Polyethylene Glycol", "Golytely", "MoviPrep",
        "Milk of Magnesia", "Magnesium Citrate", "Lactulose", "Lactulose Enema",
        "Fleet Enema", "Fleet Enema (Mineral Oil)", "Psyllium", "Psyllium Powder",
        "Psyllium Wafer", "Metamucil Fiber Singles", "Glycerin Supps"
    ],

    # GI - Antidiarrheals
    "gi_antidiarrheals": [
        "LOPERamide", "Opium Tincture", "Belladonna & Opium (16.2/30mg)"
    ],

    # GI - Other GI Medications
    "gi_other": [
        "Sucralfate", "Sulfasalazine", "Octreotide Acetate", "Octreotide",
        "Pancrelipase 5000", "Ursodiol", "Donnatal",
        "Aluminum Hydroxide Suspension", "Aluminum-Magnesium Hydrox.-Simethicone",
        "Simethicone", "Maalox/Lidocaine", "Maalox/Diphenhydramine/Lidocaine",
        "Methylnaltrexone", "Sodium Polystyrene Sulfonate"
    ],

    # Neurological - Antiepileptics
    "neuro_antiepileptics": [
        "LevETIRAcetam", "Levetiracetam (Keppra)", "LeVETiracetam Oral Solution", "Phenytoin",
        "Dilantin", "Phenytoin Sodium", "Phenytoin Sodium (IV)", "Phenytoin (Suspension)",
        "Phenytoin Infatab", "Fosphenytoin", "PHENObarbital",
        "PHENObarbital - ICU Alcohol Withdrawal (Loading Dose 1)",
        "PHENObarbital - ICU Alcohol Withdrawal (Loading Dose 2 and 3)",
        "PHENObarbital - ICU Alcohol Withdrawal (Initial Load / Rescue Dose)",
        "PHENObarbital Alcohol Withdrawal Dose Taper (Days 2-7)",
        "Valproic Acid", "Divalproex (DELayed Release)", "Divalproex (EXTended Release)",
        "Divalproex Sod. Sprinkles", "Carbamazepine", "LamoTRIgine",
        "Topiramate (Topamax)", "Gabapentin", "Pregabalin"
    ],

    # Neurological - Parkinson's & Movement Disorders
    "neuro_parkinsons": [
        "Benztropine Mesylate", "Amantadine"
    ],

    # Neurological - Dementia
    "neuro_dementia": [
        "Donepezil"
    ],

    # Neurological - Other
    "neuro_other": [
        "Baclofen", "Tizanidine", "Cyclobenzaprine", "Methocarbamol",
        "riluzole"
    ],

    # Psychiatric - Antidepressants (SSRI/SNRI)
    "psych_ssri_snri": [
        "Citalopram", "Escitalopram Oxalate", "Fluoxetine", "Sertraline",
        "Paroxetine", "Duloxetine"
    ],

    # Psychiatric - Antidepressants (Other)
    "psych_antidep_other": [
        "BuPROPion", "BuPROPion (Sustained Release)", "BuPROPion XL (Once Daily)",
        "Mirtazapine", "traZODONE", "Amitriptyline"
    ],

    # Psychiatric - Antipsychotics
    "psych_antipsychotics": [
        "Haloperidol", " Haloperidol (Haldol)", "OLANZapine", "OLANZapine (Disintegrating Tablet)",
        "QUEtiapine Fumarate", "RISperidone", "ARIPiprazole",
        "ZIPRASidone Hydrochloride", "Ziprasidone Mesylate",
        "Perphenazine"
    ],

    # Psychiatric - Anxiolytics
    "psych_anxiolytics": [
        "BusPIRone"
    ],

    # Psychiatric - Sleep Aids
    "psych_sleep": [
        "Zolpidem Tartrate", "Ramelteon"
    ],

    # Psychiatric - Stimulants
    "psych_stimulants": [
        "MethylPHENIDATE (Ritalin)"
    ],

    # Steroids - Systemic
    "steroids_systemic": [
        "PredniSONE", "MethylPREDNISolone Sodium Succ", "Methylprednisolone",
        "MethylPREDNISolone Sod Succ", "Dexamethasone",
        "Dexamethasone Sod Phosphate", "Hydrocortisone Na Succ.",
        "Fludrocortisone Acetate"
    ],

    # Steroids - Topical/Local
    "steroids_topical": [
        "Hydrocortisone", "Hydrocortisone Cream 2.5%",
        "Hydrocortisone (Rectal) 2.5% Cream",
        "Triamcinolone Acetonide 0.1% Cream", "Triamcinolone Acetonide 0.1% Ointment",
        "Triamcinolone Acetonide 0.025% Cream",
        "Clobetasol Propionate 0.05% Cream", "Clobetasol Propionate 0.05% Ointment"
    ],

    # Electrolytes - Potassium
    "electrolytes_potassium": [
        "Potassium Chloride", "Potassium Chloride (Powder)", "KCl (CRRT)",
        "Potassium Chloride Replacement (Critical Care and Oncology)",
        "Potassium Chloride Replacement (Oncology)",
        "Potassium Chl 20 mEq / 1000 mL NS", "Potassium Chl 40 mEq / 1000 mL NS",
        "Potassium Chl 20 mEq / 1000 mL D5LR", "Potassium Chl 20 mEq / 1000 mL D5NS",
        "Potassium Chl 40 mEq / 1000 mL D5NS",
        "Potassium Chl 20 mEq / 1000 mL D5 1/2 NS",
        "Potassium Chl 40 mEq / 1000 mL D5 1/2 NS",
        "Potassium Phosphate", "Potassium Phosphate Replacement (Oncology)"
    ],

    # Electrolytes - Calcium
    "electrolytes_calcium": [
        "Calcium Gluconate", "Calcium Gluconate sliding scale (Critical Care-Ionized calcium)",
        "Calcium Gluconate Replacement (Oncology)", "Calcium Gluconate (CRRT)",
        "Calcium Chloride", "Calcium Carbonate", "Calcium Acetate",
        "Calcium Replacement (Oncology)"
    ],

    # Electrolytes - Magnesium
    "electrolytes_magnesium": [
        "Magnesium Sulfate", "Magnesium Sulfate Replacement (Critical Care and Oncology)",
        "Magnesium Oxide"
    ],

    # Electrolytes - Phosphate
    "electrolytes_phosphate": [
        "Neutra-Phos", "Phosphorus", "Sodium Phosphate", "Na Phos",
        "Sodium Glycerophosphate"
    ],

    # Electrolytes - Sodium
    "electrolytes_sodium": [
        "Sodium Chloride", "Sodium Bicarbonate",
        "23.4% Sodium Chloride", "Sodium Chloride 3% (Hypertonic)",
        "Sodium Chloride 3% Inhalation Soln", "Sodium Chloride Nasal",
        "Sodium CITRATE 4%"
    ],

    # IV Fluids - Crystalloids
    "iv_fluids_crystalloids": [
        "0.9% Sodium Chloride", "NaCl", "NS", "Sodium Chloride 0.9%",
        "Sodium Chloride 0.9%  Flush", "0.9% Sodium Chloride (Mini Bag Plus)",
        "Iso-Osmotic Sodium Chloride", "Isotonic Sodium Chloride",
        "0.9% NaCl (EXCEL/ViaFLO BAG)", "0.83% Sodium Chloride",
        "0.45% Sodium Chloride",
        "Lactated Ringers", "LR", "PlasmaLyte",
        "Sterile Water", "SW"
    ],

    # IV Fluids - Dextrose
    "iv_fluids_dextrose": [
        "5% Dextrose", "D5W", "5% Dextrose (EXCEL BAG)", "Dextrose PN",
        "Dextrose 5%", "Iso-Osmotic Dextrose",
        "Dextrose 50%", "D10W", "D5NS", "D5LR",
        "D5 1/2NS", "D5 1/4NS"
    ],

    # IV Fluids - Colloids
    "iv_fluids_colloids": [
        "Albumin 5%", "Albumin 5% (12.5g / 250mL)", "Albumin 5% (25g / 500mL)",
        "Albumin 25%", "Albumin 25% (12.5g / 50mL)",
        "Dextran 40 10% in NS", "Dextran 40 in NaCl"
    ],

    # IV Fluids - TPN/Nutrition
    "iv_fluids_tpn": [
        "Amino Acids 4.25%-Dextrose 5%", "Amino Acids 5%-Dextrose 15%"
    ],

    # Vitamins & Supplements
    "vitamins_supplements": [
        "Multivitamins", "Multivitamins W/minerals", "Multivitamin IV",
        "Vitamin B Complex", "Vitamin B Complex w/C", "Vitamin B Complex W/C",
        "FoLIC Acid", " Folic Acid", "Cyanocobalamin", "Thiamine", "Pyridoxine",
        "Vitamin D", "Vitamin D3", "25-OH Vitamin D", "Calcitriol", "Doxercalciferol",
        "Vitamin D3 / Placebo", "Vitamin D3/ placebo",
        "Vitamin E", "Vitamin A", "Ascorbic Acid",
        "Nephrocaps", "Ferrous Sulfate", "Ferrous Sulfate (Liquid)",
        "Ferrous Gluconate", "Ferric Gluconate",
        "Zinc Sulfate", "Glutamine"
    ],

    # Thyroid Medications
    "thyroid": [
        "Levothyroxine Sodium", "Thyroid", "Methimazole"
    ],

    # Antihistamines
    "antihistamines": [
        "DiphenhydrAMINE", "Chlorpheniramine Maleate", "HYDROXYzine",
        "Cetirizine", "Fexofenadine", "Loratadine"
    ],

    # Cough & Cold
    "cough_cold": [
        "Guaifenesin", "Guaifenesin ER", "Guaifenesin-Dextromethorphan",
        "Dextromethorphan-Guaifenesin (Sugar Free)", "Benzonatate",
        "Pseudoephedrine", "Acetylcysteine 20%", "Acetylcysteine (IV)"
    ],

    # Nicotine Replacement
    "nicotine": [
        "Nicotine Polacrilex", "Nicotine Patch"
    ],

    # Urological
    "urological": [
        "Tamsulosin", "Finasteride", "Phenazopyridine",
        "Hyoscyamine", "Oxymetazoline"
    ],

    # Chemotherapy - Alkylating Agents
    "chemo_alkylating": [
        "Cytarabine", "Busulfan", "CARBOplatin"
    ],

    # Chemotherapy - Anthracyclines
    "chemo_anthracyclines": [
        "IDArubicin", "DAUNOrubicin", "Mitoxantrone", "Mitoxantrone HCl"
    ],

    # Chemotherapy - Antimetabolites
    "chemo_antimetabolites": [
        "Fludarabine Phosphate", "Methotrexate", "Decitabine", "Etoposide"
    ],

    # Chemotherapy - Targeted Therapy
    "chemo_targeted": [
        "venetoclax", "ruxolitinib", "Lenalidomide (Revlimide)15mg",
        "ibrutinib", "Hydroxychloroquine Sulfate"
    ],

    # Colony Stimulating Factors
    "csf_agents": [
        "Filgrastim", "Filgrastim-sndz", "Epoetin Alfa", "Epoetin alfa-epbx (Retacrit)"
    ],

    # Immunosuppressants
    "immunosuppressants": [
        "Tacrolimus", "Tacrolimus Suspension"
    ],

    # Neuromuscular Blockers
    "neuromuscular_blockers": [
        "Succinylcholine", "Vecuronium Bromide", "Rocuronium",
        "Cisatracurium Besylate"
    ],

    # Reversal Agents
    "reversal_agents": [
        "Naloxone", "Neostigmine", "Neostigmine (CVICU Reversal Protocol)",
        "Glycopyrrolate", "Glycopyrrolate (CVICU Reversal Protocol)",
        "Glucagon", "Desmopressin Acetate"
    ],

    # Hormones - Other
    "hormones_other": [
        "AndroGel", "Tamoxifen Citrate", "Estrogens Conjugated",
        "Calcitonin Salmon"
    ],

    # Gout Medications
    "gout": [
        "Allopurinol", "Febuxostat"
    ],

    # Osteoporosis
    "osteoporosis": [
        "Pamidronate"
    ],

    # Rheumatology
    "rheumatology": [
        "Hydroxychloroquine Sulfate", "Hydroxyurea"
    ],

    # Contrast & Diagnostic Agents
    "contrast_diagnostic": [
        "Iohexol 240", "Gastroview (Diatrizoate Meglumine & Sodium)",
        "Readi-Cat 2 (Barium Sulfate 2% Suspension)",
        "Tuberculin Protein", "Cosyntropin"
    ],

    # Vaccines
    "vaccines": [
        "Influenza Virus Vaccine", "Influenza Vaccine Quadrivalent",
        "Hepatitis B Vaccine", "PNEUMOcoccal 23-valent polysaccharide vaccine",
        "Pneumococcal Vac Polyvalent",
        "Tetanus-DiphTox-Acellular Pertuss (Adacel)"
    ],

    # Ophthalmology
    "ophthalmology": [
        "Gentamicin 0.3% Ophth. Soln", "Ciprofloxacin 0.3% Ophth Soln", "Ciprofloxacin",
        "Erythromycin 0.5% Ophth Oint",
        "Dorzolamide 2%/Timolol 0.5% Ophth.", "Dorzolamide 2% Ophth. Soln.",
        "Latanoprost 0.005% Ophth. Soln.", "Timolol Maleate 0.5%",
        "PrednisoLONE Acetate 1% Ophth. Susp.",
        "Dexamethasone Ophthalmic Susp 0.1%", "Dexamethasone Ophthalmic Soln 0.1%",
        "brimonidine", "Brimonidine Tartrate 0.15% Ophth.",
        "Artificial Tears", "Artificial Tears Preserv. Free", "Artificial Tear Ointment",
        "Phenylephrine 2.5 % Ophth Soln", "Phenylephrine",  "Tropicamide 1 %",
        "Cyclopentolate 1%", "Flurbiprofen 0.03%", "Tetracaine 0.5% Ophth Soln",
        "Atropine Sulfate 1%", "Atropine"
    ],

    # Topical Analgesics & Anesthetics
    "topical_analgesics": [
        "Lidocaine", "Lidocaine 1%", "Lidocaine 2%", "Lidocaine 0.5%",
        "Lidocaine 5% Patch", "Lidocaine 5% Ointment",
        "Lidocaine Jelly 2%", "Lidocaine Jelly 2% (Urojet)", "Lidocaine Jelly 2% (Glydo)",
        "Lidocaine Viscous 2%", "Lidocaine 1% (For PICC/Midline Insertions)",
        "Lidocaine-Prilocaine", "Capsaicin 0.025%", "Bengay Cream"
    ],

    # Topical Antibiotics
    "topical_antibiotics": [
        "Mupirocin Nasal Ointment 2%", "Mupirocin Cream 2%", "Mupirocin Ointment 2%",
        "Neomycin-Polymyxin-Bacitracin"
    ],

    # Dermatology
    "dermatology": [
        "Sarna Lotion", "Hydrocerin", "Aquaphor Ointment",
        "Collagenase Ointment", "Sodium Fluoride 1.1% (Dental Gel)",
        "Fluticasone Propionate NASAL"
    ],

    # Rectal/Hemorrhoid
    "rectal": [
        "Hemorrhoidal Suppository", "Tucks Hemorrhoidal Oint 1%"
    ],

    # Throat/Oral Care
    "throat_oral": [
        "Cepacol (Menthol)", "Cepacol (Sore Throat Lozenge)",
        "Cepastat (Phenol) Lozenge", "Chloraseptic Throat Spray",
        "Chlorhexidine Gluconate 0.12% Oral Rinse", "Caphosol",
        "Carbamide Peroxide 6.5%"
    ],

    # Oncology Supportive Care
    "oncology_supportive": [
        "Rasburicase", "Fosaprepitant"
    ],

    # Dialysis Solutions
    "dialysis_solutions": [
        "Prismasate (B22 K4)", "Prismasate (B32 K2)",
        "Citrate Dextrose 3% (ACD-A) CRRT", "ACD-A Citrate"
    ],

    # Other Specialized
    "specialized_other": [
        "Mannitol 20%", "Mannitol", "Ivermectin", "Januvia", "Orthopedic Solution"
    ],

    # Drug Delivery Devices
    "drug_delivery": [
        "Bag", "Vial", "Syringe", "Soln", "Soln.",
        "Yellow CADD Cassette", "Blue CADD Cassette",
        "Syringe (0.9% Sodium Chloride)", "Syringe (Chemo)",
        "Syringe (Iso-Osmotic Dextrose)", "Syringe (SW)"
    ],

    # Protocols & Infusions
    "protocols_infusions": [
        "HYDROmorphone Infusion – Comfort Care Guidelines",
        "Morphine Infusion – Comfort Care Guidelines",
        "Bupivacaine 0.1%", "Ropivacaine 0.2%",
        "Bupivacaine 0.1%|HYDROmorphone (Dilaudid)", "Hydromorphone (Dilaudid)"
    ],

    # Enteral Nutrition - Standard Formulas
    "enteral_nutrition": [
        "Osmolite",
        "Isosource 1.5 (Full)",
        "Jevity 1.2 (Full)",
        "Glucerna 1.2 (Full)",
        "Boost Glucose Control",
        "Nepro (Full) 10.0 mL/hour",
        "Peptamen 1.5 (Full)",
        "Peptamen Bariatric (Full)",
        "Replete with Fiber (Full)",
        "Vital 1.5",
        "Vital High Protein",
        "Vivonex",
        "Beneprotein"
    ],

    # Parenteral Nutrition
    "parenteral_nutrition": [
        "TPN w/Lipids",
        "TPN without Lipids",
        "Lipids (additive)"
    ],

    # Blood Products - Packed Cells
    "blood_products": [
        "Packed Red Blood Cells",
        "OR Packed RBC Intake",
        "Fresh Frozen Plasma",
        "OR FFP Intake",
        "Platelets",
        "OR Platelet Intake",
        "Cryoprecipitate",
        "OR Crystalloid Intake",
        "OR Colloid Intake nan nan",
        "PACU Crystalloid Intake"
    ]
}


# =============================================================================
# MEDICATION NAME CLEANING FUNCTIONS
# =============================================================================

def clean_medication_name(name):
    """
    Clean and standardize medication names.

    :param med_name : str
        Raw medication name
    :return str
        Cleaned medication name
    """
    if not isinstance(name, str):
        return ""

    name = name.strip().lower().capitalize().replace("nan", "")

    # Remove common suffixes/extra info in parentheses at the end  # but keep dose information
    name = re.sub(r'\s*\(self administering medication\)\s*', '', name)
    name = re.sub(r'\s*[-/]\s*', '-', name)  # Standardize spacing around hyphens and slashes
    name = re.sub(r'\s+', ' ', name)  # Remove extra whitespace
    name = re.sub(r'-{2,}', '-', name)  # Multiple occurrences
    name = re.sub(r'_{2,}', '_', name)  # Multiple occurrences
    name = re.sub(r"[.,;]+", "", name)  # Remove trailing punctuation except for %

    return name.strip()


def extract_drug_name(med_name):
    """
    Extract drug name by removing doses, routes, and formulations.

    :param med_name : str
        Medication name (cleaned or raw)
    returns str
        Generic drug name
    """
    cleaned = clean_medication_name(med_name)

    # Remove dose information in parentheses
    name = re.sub(r'\s*\([^)]*mg[^)]*\)', '', cleaned, flags=re.IGNORECASE)
    name = re.sub(r'\s*\([^)]*mcg[^)]*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*\([^)]*mL[^)]*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*\([^)]*units[^)]*\)', '', name, flags=re.IGNORECASE)

    # Remove formulation descriptors
    formulations = [
        'IV', 'Oral', 'Neb', 'Inhaler', 'Patch', 'Cream', 'Ointment',
        'Suspension', 'Solution', 'Soln', 'Tablet', 'Capsule',
        'Extended Release', 'ER', 'SR', 'XL', 'CR', 'LA',
        'Delayed Release', 'Sustained Release', 'Immediate Release',
        'IR', 'DR', 'EC', 'ODT', 'MDI', 'Liquid', 'Powder',
        'Ophth', 'Ophthalmic', 'Nasal', 'Topical', 'Rectal',
        'Suppository', 'Enema', 'Flush', 'Infusion'
    ]

    pattern = r'\b(' + '|'.join(formulations) + r')\b\.?'
    name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove concentration percentages but keep the drug name
    name = re.sub(r'\s+\d+\.?\d*%', '', name)

    # Remove "Chloride", etc. from salt forms for standardization
    # (optional - comment out if you want to keep salt forms)
    # salt_forms = [ 'Chloride', 'Hydrochloride', 'HCl', 'Sulfate',
    #               'Citrate', 'Tartrate', 'Mesylate', 'Maleate', 'Acetate',
    #               'Gluconate', 'Phosphate']
    # pattern = r'\b(' + '|'.join(salt_forms) + r')\b'
    # name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Clean up extra spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def get_medication_class(med_name):
    """
    Get the therapeutic class(es) of a medication.
    param:  med_name : str
        Medication name
    :return medication_classes: list
        List of therapeutic classes
    """
    classes = []
    for category, meds in medications_categories.items():
        if med_name in meds:
            classes.append(category)
    return classes if classes else ["uncategorized"]



if __name__ == "__main__":
    print("=" * 70)
    print("MEDICATION CATEGORIZATION SYSTEM")
    print("=" * 70)

    # Test cleaning functions
    test_meds = [
        "HYDROmorphone (Dilaudid)",
        "Potassium Chloride Replacement (Critical Care and Oncology)",
        "Insulin Pump (Self Administering Medication)",
        "OxyCODONE--Acetaminophen (5mg-325mg)",
        "Lidocaine 5% Patch",
        "Fluticasone-Salmeterol Diskus (250/50)"
    ]

    print("\nCLEANING FUNCTION TESTS:")
    print("-" * 70)
    for med in test_meds:
        cleaned = clean_medication_name(med)
        name = extract_drug_name(med)

        print(f"Original:     {med}")
        print(f"Cleaned:      {cleaned}")
        print(f"name:      {name}")
        print()

    # Statistics
    print("=" * 70)
    print("CATEGORY STATISTICS")
    print("=" * 70)
    total_meds = sum(len(meds) for meds in medications_categories.values())
    print(f"Total Categories: {len(medications_categories)}")
    print(f"Total Medications: {total_meds}")

    # Category groupings
    print("\n" + "=" * 70)
    print("MAJOR THERAPEUTIC AREAS")
    print("=" * 70)

    therapeutic_areas = {
        "Pain Management": ["sedatives_analgesics", "combination_analgesics", "nsaids_analgesics"],
        "Antibiotics": [k for k in medications_categories.keys() if k.startswith("antibiotics_")],
        "Cardiovascular": [k for k in medications_categories.keys() if k.startswith("cv_")],
        "Respiratory": [k for k in medications_categories.keys() if k.startswith("respiratory_")],
        "GI Medications": [k for k in medications_categories.keys() if k.startswith("gi_")],
        "Neurological": [k for k in medications_categories.keys() if k.startswith("neuro_")],
        "Psychiatric": [k for k in medications_categories.keys() if k.startswith("psych_")],
        "Electrolytes": [k for k in medications_categories.keys() if k.startswith("electrolytes_")],
        "IV Fluids": [k for k in medications_categories.keys() if k.startswith("iv_fluids_")],
        "Chemotherapy": [k for k in medications_categories.keys() if k.startswith("chemo_")]
    }

    for area, categories in therapeutic_areas.items():
        count = sum(len(medications_categories.get(cat, [])) for cat in categories)
        print(f"{area:25s}: {count:3d} medications ({len(categories)} subcategories)")

    # Top categories by count
    print("\nTop 10 Categories by Medication Count:")
    print("-" * 70)
    cat_counts = [(cat, len(meds)) for cat, meds in medications_categories.items()]
    cat_counts.sort(key=lambda x: x[1], reverse=True)
    for i, (cat, count) in enumerate(cat_counts[:10], 1):
        print(f"{i:2d}. {cat:40s}: {count:3d} medications")