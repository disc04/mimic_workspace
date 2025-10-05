"""

Category Organization:

    Life-Saving: Airway, vascular access, mechanical ventilation
    Organ System: Cardiac, vascular, neuro, GI, orthopedic
    Procedure Type: Diagnostic (endoscopy, biopsy) vs therapeutic (surgery, stenting)
    Invasiveness: Minimally invasive (percutaneous) vs open surgery
    Complexity: Basic ED procedures vs complex OR procedures

"""

# Medical Procedures Categorization Dictionary

procedures_categories = {
    # TOP 10 COMMON ED PROCEDURES FOR DASHBOARD
    "ed_dashboard_procedures": [
        "Insertion of endotracheal tube",
        "Central venous catheter placement with guidance",
        "Arterial catheterization",
        "Insertion of (naso-)intestinal tube",
        "Venous catheterization, not elsewhere classified",
        "Thoracentesis",
        "Spinal tap",
        "Closed reduction of fracture with internal fixation, femur",
        "Insertion of Feeding Device into Stomach, Percutaneous Approach",
        "Drainage of Peritoneal Cavity, Percutaneous Approach"
    ],

    # Airway Management
    "airway_management": [
        "Insertion of endotracheal tube",
        "Insertion of Endotracheal Airway into Trachea, Via Natural or Artificial Opening",
        "Insertion of Endotracheal Airway into Trachea, Via Natural or Artificial Opening Endoscopic",
        "Laryngoscopy and other tracheoscopy",
        "Fiber-optic bronchoscopy",
        "Other bronchoscopy",
        "Inspection of Tracheobronchial Tree, Via Natural or Artificial Opening Endoscopic",
        "Inspection of Larynx, Via Natural or Artificial Opening Endoscopic"
    ],

    # Vascular Access - Central Lines
    "vascular_access_central": [
        "Central venous catheter placement with guidance",
        "Insertion of Infusion Device into Superior Vena Cava, Percutaneous Approach",
        "Insertion of Infusion Device into Right Atrium, Percutaneous Approach",
        "Insertion of Infusion Device into Right Internal Jugular Vein, Percutaneous Approach",
        "Insertion of Tunneled Vascular Access Device into Chest Subcutaneous Tissue and Fascia, Percutaneous Approach",
        "Removal of Tunneled Vascular Access Device from Trunk Subcutaneous Tissue and Fascia, External Approach"
    ],

    # Vascular Access - Arterial
    "vascular_access_arterial": [
        "Arterial catheterization",
        "Insertion of Infusion Device into Left Femoral Artery, Percutaneous Approach",
        "Insertion of Monitoring Device into Upper Artery, Percutaneous Approach"
    ],

    # Vascular Access - Peripheral
    "vascular_access_peripheral": [
        "Venous catheterization, not elsewhere classified",
        "Insertion of Infusion Device into Right Femoral Vein, Percutaneous Approach",
        "Introduction of Nutritional Substance into Peripheral Vein, Percutaneous Approach"
    ],

    # Mechanical Ventilation
    "mechanical_ventilation": [
        "Continuous invasive mechanical ventilation for less than 96 consecutive hours",
        "Continuous invasive mechanical ventilation for 96 consecutive hours or more",
        "Respiratory Ventilation, Less than 24 Consecutive Hours",
        "Respiratory Ventilation, 24-96 Consecutive Hours",
        "Respiratory Ventilation, Greater than 96 Consecutive Hours",
        "Non-invasive mechanical ventilation",
        "Assistance with Respiratory Ventilation, Greater than 96 Consecutive Hours, Continuous Positive Airway Pressure"
    ],

    # Bronchoscopy & Pulmonary Procedures
    "bronchoscopy": [
        "Closed [endoscopic] biopsy of bronchus",
        "Closed endoscopic biopsy of lung",
        "Open biopsy of lung",
        "Drainage of Right Main Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Left Main Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Right Lower Lobe Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Left Lower Lobe Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Right Middle Lung Lobe, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Right Upper Lobe Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Left Upper Lobe Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Excision of Right Main Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Excision of Left Main Bronchus, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Other diagnostic procedures on lung or bronchus"
    ],

    # Bronchial Interventions
    "bronchial_interventions": [
        "Extirpation of Matter from Left Main Bronchus, Via Natural or Artificial Opening Endoscopic",
        "Extirpation of Matter from Lung Lingula, Via Natural or Artificial Opening Endoscopic",
        "Extirpation of Matter from Left Lower Lung Lobe, Via Natural or Artificial Opening Endoscopic",
        "Extirpation of Matter from Right Lower Lung Lobe, Via Natural or Artificial Opening Endoscopic",
        "Extirpation of Matter from Left Lower Lobe Bronchus, Via Natural or Artificial Opening Endoscopic",
        "Dilation of Left Main Bronchus with Intraluminal Device, Via Natural or Artificial Opening Endoscopic",
        "Dilation of Right Main Bronchus with Intraluminal Device, Via Natural or Artificial Opening Endoscopic",
        "Destruction of Left Main Bronchus, Via Natural or Artificial Opening Endoscopic",
        "Destruction of Right Main Bronchus, Via Natural or Artificial Opening Endoscopic",
        "Destruction of Right Lower Lung Lobe, Via Natural or Artificial Opening Endoscopic"
    ],

    # Chest Tube & Pleural Procedures
    "chest_procedures": [
        "Insertion of intercostal catheter for drainage",
        "Thoracentesis",
        "Other incision of pleura",
        "Drainage of Right Pleural Cavity with Drainage Device, Percutaneous Approach",
        "Drainage of Left Pleural Cavity, Percutaneous Approach",
        "Drainage of Left Pleural Cavity, Percutaneous Approach, Diagnostic",
        "Drainage of Pericardial Cavity, Percutaneous Approach",
        "Drainage of Pericardial Cavity with Drainage Device, Percutaneous Approach"
    ],

    # Thoracic Surgery
    "thoracic_surgery": [
        "Reopening of recent thoracotomy site",
        "Thoracoscopic decortication of lung",
        "Thoracoscopic lobectomy of lung",
        "Other and unspecified pneumonectomy",
        "Excision of Right Lower Lung Lobe, Via Natural or Artificial Opening Endoscopic",
        "Excision of Right Middle Lung Lobe, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Other repair and plastic operations on bronchus",
        "Mediastinoscopy",
        "Other repair of chest wall",
        "Removal of other device from thorax"
    ],

    # Cardiac Catheterization - Diagnostic
    "cardiac_cath_diagnostic": [
        "Left heart cardiac catheterization",
        "Right heart cardiac catheterization",
        "Combined right and left heart cardiac catheterization",
        "Coronary arteriography using two catheters",
        "Angiocardiography of left heart structures",
        "Combined right and left heart angiocardiography",
        "Fluoroscopy of Right Heart using Other Contrast",
        "Measurement of Cardiac Sampling and Pressure, Left Heart, Percutaneous Approach",
        "Measurement of Cardiac Sampling and Pressure, Right Heart, Percutaneous Approach"
    ],

    # Coronary Angiography
    "coronary_angiography": [
        "Fluoroscopy of Multiple Coronary Arteries using Other Contrast",
        "Fluoroscopy of Multiple Coronary Arteries using Low Osmolar Contrast",
        "Procedure on single vessel",
        "Procedure on two vessels"
    ],

    # Percutaneous Coronary Intervention
    "pci": [
        "Percutaneous transluminal coronary angioplasty [PTCA]",
        "Insertion of drug-eluting coronary artery stent(s)",
        "Insertion of one vascular stent",
        "Dilation of Coronary Artery, One Artery with Drug-eluting Intraluminal Device, Percutaneous Approach",
        "Dilation of Coronary Artery, Two Arteries with Drug-eluting Intraluminal Device, Percutaneous Approach",
        "Extirpation of Matter from Coronary Artery, One Artery, Percutaneous Approach"
    ],

    # Coronary Artery Bypass Grafting
    "cabg": [
        "Single internal mammary-coronary artery bypass",
        "(Aorto)coronary bypass of one coronary artery",
        "(Aorto)coronary bypass of two coronary arteries",
        "(Aorto)coronary bypass of three coronary arteries",
        "(Aorto)coronary bypass of four or more coronary arteries",
        "Bypass Coronary Artery, One Artery from Left Internal Mammary, Open Approach",
        "Bypass Coronary Artery, One Artery from Left Internal Mammary with Autologous Arterial Tissue, Open Approach",
        "Bypass Coronary Artery, One Artery from Right Internal Mammary with Autologous Arterial Tissue, Open Approach",
        "Bypass Coronary Artery, One Artery from Aorta with Autologous Venous Tissue, Open Approach",
        "Bypass Coronary Artery, Three Arteries from Aorta with Autologous Venous Tissue, Open Approach",
        "Bypass Coronary Artery, Two Arteries from Coronary Artery, Open Approach"
    ],

    # CABG - Vessel Harvesting
    "cabg_harvest": [
        "Excision of Left Internal Mammary Artery, Percutaneous Endoscopic Approach",
        "Excision of Right Internal Mammary Artery, Percutaneous Endoscopic Approach",
        "Excision of Left Saphenous Vein, Percutaneous Endoscopic Approach",
        "Excision of Right Saphenous Vein, Percutaneous Endoscopic Approach",
        "Excision of Left Saphenous Vein, Open Approach"
    ],

    # Cardiac Surgery - Valve
    "cardiac_valve_surgery": [
        "Open and other replacement of aortic valve",
        "Open and other replacement of aortic valve with tissue graft",
        "Open heart valvuloplasty of mitral valve without replacement",
        "Percutaneous balloon valvuloplasty",
        "Replacement of Aortic Valve with Zooplastic Tissue, Open Approach",
        "Replacement of Aortic Valve with Zooplastic Tissue, Percutaneous Approach"
    ],

    # Cardiac Surgery - Other
    "cardiac_surgery_other": [
        "Extracorporeal circulation auxiliary to open heart surgery",
        "Repair of atrial septal defect with tissue graft",
        "Excision or destruction of other lesion or tissue of heart, open approach",
        "Excision or destruction of other lesion or tissue of heart, endovascular approach",
        "Other repair of vessel",
        "Repair of blood vessel with tissue patch graft"
    ],

    # Cardiac Rhythm Management
    "cardiac_rhythm": [
        "Implantation of cardiac resynchronization defibrillator, total system [CRT-D]",
        "Automatic implantable cardioverter/defibrillator (AICD) check",
        "Insertion or replacement of epicardial lead [electrode] into epicardium",
        "Cardiac mapping",
        "Other electric countershock of heart",
        "Catheter based invasive electrophysiologic testing",
        "Other electroshock therapy"
    ],

    # Cardiac Support Devices
    "cardiac_support": [
        "Assistance with Cardiac Output using Balloon Pump, Continuous",
        "Performance of Cardiac Output, Continuous",
        "Monitoring of Cardiac Output, Percutaneous Approach"
    ],

    # Cardiac Monitoring
    "cardiac_monitoring": [
        "Insertion of Monitoring Device into Pulmonary Trunk, Percutaneous Approach",
        "Monitoring of Arterial Pressure, Pulmonary, Percutaneous Approach",
        "Intravascular pressure measurement, other specified and unspecified vessels"
    ],

    # Vascular Surgery - Carotid
    "vascular_carotid": [
        "Restriction of Left Internal Carotid Artery with Intraluminal Device, Percutaneous Approach",
        "Extirpation of Matter from Right External Carotid Artery, Open Approach",
        "Supplement Right Common Carotid Artery with Nonautologous Tissue Substitute, Open Approach",
        "Supplement Right External Carotid Artery with Nonautologous Tissue Substitute, Open Approach",
        "Other operations on carotid body, carotid sinus and other vascular bodies",
        "Implantation or replacement of carotid sinus stimulation device, total system"
    ],

    # Vascular Surgery - Peripheral
    "vascular_peripheral": [
        "Bypass Left Femoral Artery to Popliteal Artery with Autologous Venous Tissue, Open Approach",
        "Occlusion of Right Femoral Artery with Intraluminal Device, Percutaneous Approach",
        "Repair Upper Artery, Open Approach"
    ],

    # Vascular Interventions - Embolization
    "vascular_embolization": [
        "Endovascular (total) embolization or occlusion of head and neck vessels",
        "Transcatheter embolization for gastric or duodenal bleeding",
        "Occlusion of Right Vertebral Artery with Intraluminal Device, Percutaneous Approach",
        "Occlusion of Gastric Artery with Intraluminal Device, Percutaneous Approach",
        "Occlusion of Hepatic Artery with Intraluminal Device, Percutaneous Approach",
        "Occlusion of Esophageal Vein with Extraluminal Device, Via Natural or Artificial Opening Endoscopic"
    ],

    # Vascular Interventions - Stenting
    "vascular_stenting": [
        "Insertion of non-drug-eluting peripheral (non-coronary) vessel stent(s)",
        "Angioplasty of other non-coronary vessel(s)",
        "Insertion of Intraluminal Device into Inferior Vena Cava, Percutaneous Approach",
        "Dilation of Left Common Iliac Vein with Intraluminal Device, Percutaneous Approach",
        "Dilation of Left External Iliac Vein with Intraluminal Device, Percutaneous Approach",
        "Dilation of Left Cephalic Vein, Percutaneous Approach",
        "Dilation of Left Brachial Vein, Percutaneous Approach"
    ],

    # Vascular Interventions - Thrombectomy
    "vascular_thrombectomy": [
        "Introduction of Other Thrombolytic into Central Vein, Percutaneous Approach",
        "Introduction of Other Thrombolytic into Peripheral Vein, Percutaneous Approach",
        "Injection or infusion of thrombolytic agent",
        "Extirpation of Matter from Left Femoral Vein, Percutaneous Approach",
        "Extirpation of Matter from Left Common Iliac Vein, Percutaneous Approach"
    ],

    # Vascular Surgery - Thoracic
    "vascular_thoracic": [
        "Resection of vessel with replacement, thoracic vessels",
        "Fluoroscopy of Superior Vena Cava using Other Contrast, Guidance"
    ],

    # Angiography - Abdominal
    "angiography_abdominal": [
        "Aortography",
        "Fluoroscopy of Abdominal Aorta",
        "Arteriography of other intra-abdominal arteries",
        "Fluoroscopy of Superior Mesenteric Artery using Other Contrast",
        "Fluoroscopy of Inferior Mesenteric Artery using Other Contrast",
        "Arteriography of renal arteries"
    ],

    # Angiography - Other
    "angiography_other": [
        "Arteriography of cerebral arteries",
        "Arteriography of other specified sites",
        "Arteriography of femoral and other lower extremity arteries",
        "Fluoroscopy of Left Lower Extremity Arteries using Other Contrast",
        "Other endovascular procedures on other vessels"
    ],

    # Venography
    "venography": [
        "Phlebography of the portal venous system using contrast material",
        "Fluoroscopy of Dialysis Shunt/Fistula using Low Osmolar Contrast",
        "Ultrasonography of Right Lower Extremity Veins, Guidance",
        "Ultrasonography of Right Jugular Veins, Intravascular",
        "Ultrasonography of Superior Vena Cava, Guidance"
    ],

    # Neurosurgery - Intracranial
    "neurosurgery_intracranial": [
        "Other craniotomy",
        "Other incision of brain",
        "Other excision or destruction of lesion or tissue of brain",
        "Clipping of aneurysm",
        "Restriction of Intracranial Artery with Intraluminal Device, Percutaneous Approach",
        "Extirpation of Matter from Intracranial Subdural Space, Open Approach",
        "Excision of Cerebral Ventricle, Open Approach"
    ],

    # Neurosurgery - CSF Management
    "neurosurgery_csf": [
        "Spinal tap",
        "Insertion or replacement of external ventricular drain [EVD]",
        "Drainage of Cerebral Ventricle with Drainage Device, Open Approach",
        "Insertion of catheter into spinal canal for infusion of therapeutic or palliative substances",
        "Injection of anesthetic into spinal canal for analgesia"
    ],

    # Neurosurgery - Dural
    "neurosurgery_dural": [
        "Supplement Dura Mater with Nonautologous Tissue Substitute, Open Approach"
    ],

    # Spine Surgery - Fusion
    "spine_fusion": [
        "Fusion or refusion of 2-3 vertebrae",
        "Lumbar and lumbosacral fusion of the posterior column, posterior technique",
        "Fusion of 8 or more Thoracic Vertebral Joints with Autologous Tissue Substitute, Posterior Approach, Posterior Column, Open Approach",
        "Fusion of Cervical Vertebral Joint with Interbody Fusion Device, Anterior Approach, Anterior Column, Open Approach",
        "Fusion of Cervical Vertebral Joint with Autologous Tissue Substitute, Posterior Approach, Posterior Column, Open Approach"
    ],

    # Spine Surgery - Discectomy
    "spine_discectomy": [
        "Excision of Cervical Vertebral Disc, Open Approach"
    ],

    # Orthopedic - Fracture Fixation
    "orthopedic_fracture": [
        "Closed reduction of fracture with internal fixation, femur",
        "Open reduction of fracture with internal fixation, humerus",
        "Internal fixation of bone without fracture reduction, femur",
        "Insertion of Intramedullary Internal Fixation Device into Left Upper Femur, Percutaneous Approach",
        "Reposition Right Tibia with Intramedullary Internal Fixation Device, Open Approach"
    ],

    # Orthopedic - Maxillofacial
    "orthopedic_maxillofacial": [
        "Reposition Right Mandible with Internal Fixation Device, Open Approach",
        "Reposition Left Maxilla with External Fixation Device, Percutaneous Approach",
        "Reposition Left Mandible with External Fixation Device, Percutaneous Approach"
    ],

    # Orthopedic - Bone Procedures
    "orthopedic_bone": [
        "Biopsy of bone, femur",
        "Other partial ostectomy, tarsals and metatarsals",
        "Local excision of lesion or tissue of bone, other bones",
        "Excision of bone for graft, unspecified site",
        "Excision of Right Metatarsal, Open Approach",
        "Biopsy of bone marrow",
        "Extraction of Iliac Bone Marrow, Percutaneous Approach, Diagnostic"
    ],

    # Orthopedic - Soft Tissue
    "orthopedic_soft_tissue": [
        "Excision of Right Foot Subcutaneous Tissue and Fascia, Open Approach",
        "Excision of Left Foot Tendon, Open Approach",
        "Excision of Left Lower Leg Subcutaneous Tissue and Fascia, Open Approach",
        "Extraction of Left Upper Leg Subcutaneous Tissue and Fascia, Open Approach",
        "Extraction of Left Lower Leg Subcutaneous Tissue and Fascia, Open Approach",
        "Other fasciectomy"
    ],

    # Orthopedic - Amputation
    "orthopedic_amputation": [
        "Detachment at Right 2nd Toe, Complete, Open Approach"
    ],

    # Orthopedic - Joint
    "orthopedic_joint": [
        "Drainage of Right Hip Joint, Percutaneous Approach, Diagnostic"
    ],

    # GI Endoscopy - Upper
    "gi_endoscopy_upper": [
        "Esophagogastroduodenoscopy [EGD] with closed biopsy",
        "Extraction of Stomach, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Drainage of Stomach, Percutaneous Approach, Diagnostic",
        "Extirpation of Matter from Stomach, Via Natural or Artificial Opening Endoscopic",
        "Endoscopic control of gastric or duodenal bleeding",
        "Destruction of Duodenum, Via Natural or Artificial Opening Endoscopic",
        "Repair Duodenum, Via Natural or Artificial Opening Endoscopic",
        "Introduction of Other Therapeutic Substance into Upper GI, Via Natural or Artificial Opening Endoscopic",
        "Dilation of Lower Esophagus with Intraluminal Device, Via Natural or Artificial Opening Endoscopic"
    ],

    # GI Endoscopy - Lower
    "gi_endoscopy_lower": [
        "Colonoscopy",
        "Excision of Cecum, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Excision of Descending Colon, Via Natural or Artificial Opening Endoscopic, Diagnostic",
        "Inspection of Lower Intestinal Tract, Via Natural or Artificial Opening Endoscopic",
        "Other cystoscopy"
    ],

    # GI Endoscopy - Small Bowel
    "gi_endoscopy_small_bowel": [
        "Other endoscopy of small intestine",
        "Inspection of Gastrointestinal Tract, Open Approach",
        "Inspection of Upper Intestinal Tract, Via Natural or Artificial Opening Endoscopic"
    ],

    # GI Surgery - Gastric
    "gi_surgery_gastric": [
        "Percutaneous [endoscopic] gastrostomy [PEG]",
        "Insertion of Feeding Device into Stomach, Percutaneous Approach",
        "Drainage of Stomach with Drainage Device, Percutaneous Approach",
        "Total esophagectomy"
    ],

    # GI Surgery - Small Bowel
    "gi_surgery_small_bowel": [
        "Ileostomy, not otherwise specified",
        "Other enterostomy",
        "Closure of stoma of small intestine",
        "Other partial resection of small intestine",
        "Release Small Intestine, Open Approach",
        "Other operations on intestines"
    ],

    # GI Surgery - Colon
    "gi_surgery_colon": [
        "Open and other right hemicolectomy",
        "Open and other cecectomy",
        "Open abdominoperineal resection of the rectum"
    ],

    # GI Surgery - Appendix
    "gi_surgery_appendix": [
        "Other appendectomy"
    ],

    # Hepatobiliary - ERCP
    "hepatobiliary_ercp": [
        "Endoscopic insertion of stent (tube) into bile duct",
        "Endoscopic insertion of stent (tube) into pancreatic duct",
        "Endoscopic sphincterotomy and papillotomy",
        "Endoscopic removal of stone(s) from biliary tract",
        "Replacement of stent (tube) in biliary or pancreatic duct"
    ],

    # Hepatobiliary - Surgery
    "hepatobiliary_surgery": [
        "Laparoscopic cholecystectomy",
        "Laparoscopic partial cholecystectomy",
        "Partial hepatectomy",
        "Anastomosis of hepatic duct to gastrointestinal tract",
        "Excision of other bile duct",
        "Other destruction of lesion of liver",
        "Percutaneous aspiration of liver"
    ],

    # Pancreatic Procedures
    "pancreatic": [
        "Drainage of pancreatic cyst by catheter",
        "Other excision or destruction of lesion or tissue of pancreas or pancreatic duct",
        "Closed [aspiration] [needle] [percutaneous] biopsy of pancreas"
    ],

    # Hernia Repair
    "hernia_repair": [
        "Repair of other hernia of anterior abdominal wall",
        "Other and open repair of other hernia of anterior abdominal wall with graft or prosthesis",
        "Other laparoscopic umbilical herniorrhaphy",
        "Other open umbilical herniorrhaphy",
        "Repair of rectocele with graft or prosthesis"
    ],

    # Abdominal - Peritoneal
    "abdominal_peritoneal": [
        "Drainage of Peritoneal Cavity, Percutaneous Approach",
        "Drainage of Peritoneal Cavity, Percutaneous Approach, Diagnostic",
        "Percutaneous abdominal drainage",
        "Peritoneal lavage",
        "Laparoscopic lysis of peritoneal adhesions",
        "Other lysis of peritoneal adhesions",
        "Other repair of mesentery"
    ],

    # Abdominal - Exploratory
    "abdominal_exploratory": [
        "Other laparotomy",
        "Reopening of recent laparotomy site",
        "Control Bleeding in Abdominal Wall, Open Approach"
    ],

    # Abdominal - Laparoscopic
    "abdominal_laparoscopic": [
        "Laparoscopic robotic assisted procedure"
    ],

    # Enteral Access
    "enteral_access": [
        "Insertion of (naso-)intestinal tube",
        "Insertion of Feeding Device into Duodenum, Via Natural or Artificial Opening Endoscopic",
        "Insertion of Feeding Device into Jejunum, Via Natural or Artificial Opening Endoscopic",
        "Introduction of Nutritional Substance into Upper GI, Via Natural or Artificial Opening",
        "Introduction of Nutritional Substance into Lower GI, Via Natural or Artificial Opening",
        "Change Feeding Device in Lower Intestinal Tract, External Approach"
    ],

    # Nutrition Support
    "nutrition_support": [
        "Parenteral infusion of concentrated nutritional substances",
        "Enteral infusion of concentrated nutritional substances",
        "Introduction of Nutritional Substance into Central Vein, Percutaneous Approach"
    ],

    # Genitourinary - Cystoscopy
    "gu_cystoscopy": [
        "Inspection of Bladder, Via Natural or Artificial Opening Endoscopic",
        "Fluoroscopy of Left Kidney, Ureter and Bladder using Other Contrast",
        "Fluoroscopy of Right Kidney, Ureter and Bladder using Other Contrast"
    ],

    # Genitourinary - Interventions
    "gu_interventions": [
        "Dilation of Right Ureter with Intraluminal Device, Via Natural or Artificial Opening Endoscopic",
        "Removal of Intraluminal Device from Ureter, Via Natural or Artificial Opening Endoscopic",
        "Irrigation of Genitourinary Tract using Irrigating Substance, Via Natural or Artificial Opening",
        "Closed [percutaneous] [needle] biopsy of kidney"
    ],

    # Gynecologic Surgery
    "gynecologic_surgery": [
        "Laparoscopic total abdominal hysterectomy",
        "Laparoscopic removal of both ovaries and tubes at same operative episode"
    ],

    # Breast Surgery
    "breast_surgery": [
        "Subtotal mastectomy",
        "Unilateral simple mastectomy",
        "Excision of axillary lymph node"
    ],

    # Dialysis
    "dialysis": [
        "Hemodialysis",
        "Performance of Urinary Filtration, Single",
        "Performance of Urinary Filtration, Intermittent, Less than 6 Hours Per Day",
        "Performance of Urinary Filtration, Multiple"
    ],

    # Transfusion & Infusion
    "transfusion_infusion": [
        "Infusion of 4-Factor Prothrombin Complex Concentrate",
        "Transfusion of Nonautologous 4-Factor Prothrombin Complex Concentrate into Vein, Percutaneous Approach",
        "Pheresis of Plasma, Multiple",
        "Introduction of Other Antineoplastic into Central Vein, Percutaneous Approach",
        "Injection or infusion of cancer chemotherapeutic substance",
        "Introduction of Other Therapeutic Substance into Peripheral Artery, Percutaneous Approach",
        "Introduction of Other Therapeutic Substance into Heart, Open Approach"
    ],

    # ENT Procedures
    "ent": [
        "Control of epistaxis by anterior nasal packing",
        "Rhinoscopy",
        "Pharyngoscopy",
        "Irrigation of ear",
        "Other diagnostic procedures on nasal sinuses"
    ],

    # Dental Procedures
    "dental": [
        "Excision of dental lesion of jaw",
        "Extraction of other tooth"
    ],

    # Wound Care
    "wound_care": [
        "Excisional debridement of wound, infection, or burn",
        "Nonexcisional debridement of wound, infection or burn",
        "Application of other wound dressing",
        "Other immobilization, pressure, and attention to wound",
        "Incision with removal of foreign body or device from skin and subcutaneous tissue",
        "Other incision with drainage of skin and subcutaneous tissue",
        "Excision of Abdomen Skin, External Approach, Diagnostic"
    ],

    # Skin Grafting
    "skin_grafting": [
        "Other skin graft to other sites",
        "Attachment of pedicle or flap graft to other sites",
        "Insertion of biological graft"
    ],

    # Lymph Node Procedures
    "lymph_node": [
        "Simple excision of other lymphatic structure",
        "Regional lymph node excision",
        "Radical excision of other lymph nodes",
        "Biopsy of lymphatic structure",
        "Excision of Thorax Lymphatic, Percutaneous Endoscopic Approach, Diagnostic"
    ],

    # Bone Marrow & Transplant
    "transplant": [
        "Allogeneic hematopoietic stem cell transpant without purging",
        "Transplant from live related donor"
    ],

    # Radiation Therapy
    "radiation_therapy": [
        "Beam Radiation of Chest using Photons 1 - 10 MeV",
        "Beam Radiation of Spleen using Photons 1 - 10 MeV",
        "Other radiotherapeutic procedure"
    ],

    # Imaging - Ultrasound
    "imaging_ultrasound": [
        "Diagnostic ultrasound of heart",
        "Diagnostic ultrasound of abdomen and retroperitoneum",
        "Diagnostic ultrasound of digestive system"
    ],

    # Neurostimulation
    "neurostimulation": [
        "Insertion or replacement of other neurostimulator pulse generator"
    ],

    # Venous Shunt
    "venous_shunt": [
        "Intra-abdominal venous shunt"
    ],

    # Anorectal
    "anorectal": [
        "Biopsy of anus"
    ],

    # Substance Use Treatment
    "substance_use": [
        "Alcohol detoxification"
    ],

    # Computer Assisted Surgery
    "computer_assisted": [
        "Other computer assisted surgery"
    ],

    # Device Management - Cardiac
    "device_cardiac": [
        "Removal of Infusion Device from Heart, External Approach",
        "Change Other Device in Trunk Subcutaneous Tissue and Fascia, External Approach"
    ],

    # Abdominal Wound Control
    "abdominal_adhesions": [
        "Application or administration of an adhesion barrier substance"
    ]
}


# Helper function to find procedure categories
def get_procedure_category(procedure_name):
    """Returns the category(ies) a procedure belongs to"""
    categories = []
    for category, procedures in procedures_categories.items():
        if procedure_name in procedures:
            categories.append(category)
    return categories if categories else ["uncategorized"]


# Helper function to identify emergency procedures
def is_emergency_procedure(procedure_name):
    """Check if procedure is in ED dashboard list"""
    return procedure_name in procedures_categories["ed_dashboard_procedures"]


# Example usage and statistics
if __name__ == "__main__":
    print("=" * 70)
    print("TOP 10 COMMON ED PROCEDURES FOR DASHBOARD")
    print("=" * 70)
    for i, proc in enumerate(procedures_categories["ed_dashboard_procedures"], 1):
        print(f"{i:2d}. {proc}")

    print(f"\n{'=' * 70}")
    print(f"SUMMARY STATISTICS")
    print(f"{'=' * 70}")
    print(f"Total Categories: {len(procedures_categories)}")
    print(f"Total Procedures: {sum(len(p) for p in procedures_categories.values())}")

    # Count by major system
    cardiac_categories = [k for k in procedures_categories.keys()
                          if 'cardiac' in k.lower() or 'coronary' in k.lower() or 'cabg' in k.lower()]
    cardiac_count = sum(len(procedures_categories[k]) for k in cardiac_categories)

    gi_categories = [k for k in procedures_categories.keys()
                     if 'gi_' in k.lower() or 'hepato' in k.lower() or 'pancrea' in k.lower()]
    gi_count = sum(len(procedures_categories[k]) for k in gi_categories)

    vascular_categories = [k for k in procedures_categories.keys()
                           if 'vascular' in k.lower() or 'angio' in k.lower()]
    vascular_count = sum(len(procedures_categories[k]) for k in vascular_categories)

    neuro_categories = [k for k in procedures_categories.keys()
                        if 'neuro' in k.lower() or 'spine' in k.lower()]
    neuro_count = sum(len(procedures_categories[k]) for k in neuro_categories)

    print(f"\nProcedures by Major System:")
    print(f"  Cardiac/Coronary: {cardiac_count}")
    print(f"  GI/Hepatobiliary/Pancreatic: {gi_count}")
    print(f"  Vascular/Angiography: {vascular_count}")
    print(f"  Neurological/Spine: {neuro_count}")
    print(f"  Airway Management: {len(procedures_categories['airway_management'])}")
    print(
        f"  Vascular Access: {sum(len(procedures_categories[k]) for k in ['vascular_access_central', 'vascular_access_arterial', 'vascular_access_peripheral'])}")
    print(f"  Mechanical Ventilation: {len(procedures_categories['mechanical_ventilation'])}")

    print(f"\n{'=' * 70}")
    print("PROCEDURE CATEGORIES OVERVIEW")
    print("=" * 70)

    category_groups = {
        "Airway & Respiratory": ["airway_management", "mechanical_ventilation", "bronchoscopy",
                                 "bronchial_interventions", "chest_procedures"],
        "Vascular Access": ["vascular_access_central", "vascular_access_arterial", "vascular_access_peripheral"],
        "Cardiac": ["cardiac_cath_diagnostic", "pci", "cabg", "cardiac_valve_surgery",
                    "cardiac_rhythm", "cardiac_support"],
        "Vascular Surgery": ["vascular_carotid", "vascular_peripheral", "vascular_embolization",
                             "vascular_stenting", "vascular_thrombectomy"],
        "Neurosurgery": ["neurosurgery_intracranial", "neurosurgery_csf", "spine_fusion"],
        "GI Procedures": ["gi_endoscopy_upper", "gi_endoscopy_lower", "gi_surgery_gastric",
                          "hepatobiliary_ercp", "enteral_access"],
        "Orthopedic": ["orthopedic_fracture", "orthopedic_bone", "orthopedic_soft_tissue"],
        "Critical Care": ["dialysis", "transfusion_infusion", "nutrition_support"]
    }

    for group_name, categories in category_groups.items():
        count = sum(len(procedures_categories.get(cat, [])) for cat in categories)
        print(f"{group_name:30s}: {count:3d} procedures")

    print(f"\n{'=' * 70}")
    print("KEY INSIGHTS FOR ED DASHBOARD")
    print("=" * 70)
