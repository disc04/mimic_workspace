# MIMIC-IV Exploration Workspace

### Overview

The Medical Information Mart for Intensive Care (MIMIC-IV) is a large-scale, de-identified electronic health record (EHR) dataset that has become popular resource for clinical and data-driven research (Johnson et al., 2021).
Originally released in 2020 and continuously updated, MIMIC-IV maintains its raw, unprocessed data format—intentionally reflecting the complexity and nuance of real-world clinical information. This design choice invites researchers to apply rigorous analytical methods when working with the dataset.

Working effectively with EHR data such as MIMIC-IV requires both technical proficiency and a strong grounding in clinical knowledge. While several processing frameworks were published (Johnson et. al., 2018, Gupta et. al., 2022), researchers should remain cautious when relying solely on automated data cleaning. Algorithms that remove features based only on statistical properties risk discarding clinically meaningful variables, as they often lack the necessary medical context.
Multiple versions of MIMIC-IV are currently available via BigQuery, with access credentials obtainable through PhysioNet (Goldberger et al., 2000).

The dataset used in this workspace is the demonstration release available at: 
 - https://physionet.org/content/mimic-iv-demo/2.2/

#### Citations

 - Johnson, A., Bulgarelli, L., Pollard, T., Horng, S., Celi, L. A., & Mark, R. (2023). MIMIC-IV Clinical Database Demo (version 2.2). PhysioNet. RRID:SCR_007345. https://doi.org/10.13026/dp1f-ex47

 - Johnson, A., Bulgarelli, L., Pollard, T., Horng, S., Celi, L. A., & Mark, R. (2021). MIMIC-IV (version 1.0). PhysioNet. https://doi.org/10.13026/s6n6-xd98

 - Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220. RRID:SCR_007345.

 - Gupta M, Gallamoza B, Cutrona N, Dhakal P, Poulain R, Beheshti R. An Extensive Data Processing Pipeline for MIMIC-IV. Proc Mach Learn Res. 2022 Nov;193:311-325. PMID: 36686986; PMCID: PMC9854277.

 - The MIMIC Code Repository: enabling reproducibility in critical care research. Alistair E W Johnson, David J Stone, Leo A Celi, Tom J Pollard
Journal of the American Medical Informatics Association, Volume 25, Issue 1, January 2018, Pages 32–39, https://doi.org/10.1093/jamia/ocx084



### Motivation and Design

This workspace represent a lightweight, modular  MIMIC exploration environment—one that moves away from large, notebook-based or GUI-heavy solutions.
Its design prioritizes reproducibility, version control, and modularity through the systematic separation of medical logic from computational code.  This separation promotes transparency, easier maintenance, and adaptability to new clinical insights or research directions. 



### The standard exploratory workflow proceeds through the following stages:

- **Cohort Definition** – Define inclusion and exclusion criteria using BigQuery or local data.
- **Data Extraction** – Retrieve relevant clinical variables for the selected patient population.
- **Concept Mapping** – Apply standardized medical classifications via concept definition modules.
- **Quality Assessment** – Evaluate data completeness and clinical plausibility.
- **Feature Engineering** – Build analytical variables aligned with research goals.
- **Validation** – Compare cohort characteristics against established clinical expectations.



### Architecture

For exploratory Data Analysis, two distinct analytical pipelines are implemented:

- **Single Admission Analysis Pipeline:** Designed for in-depth examination of individual patient encounters.

- **Cohort Analysis Pipeline:** Optimized for multi-admission comparative studies and population-level analyses.

  

### Modular Knowledge Base

Medical domain knowledge is defined through dedicated, version-controlled modules to maintain clarity and flexibility:

- **vital_concept.py:** Defines vital signs and laboratory test categories.


- **procedures_context.py:** Contains logic for procedure categorization and taxonomic mappings.


- **medications_concept.py:** Implements drug classification frameworks and pharmacological groupings.



### Clinical Validity Assurance

Users are encouraged to validate extracted cohorts against clinical expectations, confirming that preprocessing steps preserve the integrity of medically relevant information. 


### Example output figures from the single admission pipeline.




**Figure 1.**
Visualization of data within MIMIC-IV for a single patient’s hospitalization. 
The annotated vertical gray line indicates care units for the patient throughout their stay. 
Vital signs are shown in the top panel: note the frequency of data collection for temperature is much higher at the start of the ICU stay due to the use of targeted temperature management. Laboratory measurements are shown in the middle panel. The bottom panel displays patient procedures from multiple sources, including from billing information, the provider order entry system, as well as the ICU information system. 




<img width="4555" height="5817" alt="patient_10015860_admission_24698912_labs_procedures" src="https://github.com/user-attachments/assets/514e7f66-8466-429e-b174-4003d75c06c0" />




**Figure 2.**
Visualization of medication information documented within MIMIC-IV for a single patient’s hospitalization. 
The annotated vertical gray line indicates care units for the patient throughout their stay. 
Prescription medications are shown in the top panel. At the bottom panel, bolus medications are indicated by markers, continuous infusions as filled boxes.




<img width="4560" height="4649" alt="patient_10015860_admission_24698912_medications" src="https://github.com/user-attachments/assets/40c5b336-db4d-45b0-b067-3177c60903be" />







### Summary figures from the entire sample dataset: 100 patients, more than 200 admissions.




**Figure 3.** Demographic data at the ICU department.




<img width="4770" height="3543" alt="ICU_demographics_analysis" src="https://github.com/user-attachments/assets/64c3dd87-830e-4dca-83d9-c106bff99370" />




**Figure 4.** Hospital primary diagnoses.




<img width="2068" height="1192" alt="Hospital_clinical_conditions_analysis" src="https://github.com/user-attachments/assets/3a140862-a4ca-41b7-bcfb-b70bc3378dee" />




**Figure 5.** Hospital services analysis.




<img width="2970" height="2369" alt="Hospital_services_analysis" src="https://github.com/user-attachments/assets/0be1ea57-19e9-4bb0-bd49-b5693813bf8a" />




**Figure 6.** Admission types analysis.




<img width="3571" height="2368" alt="Admission_types_analysis" src="https://github.com/user-attachments/assets/055b9d57-13ba-43a6-9b21-ea38a7d6a92a" />




**Figure 7.** Readmission analysis.




<img width="2968" height="1486" alt="Readmission_analysis" src="https://github.com/user-attachments/assets/eb192406-db35-4d96-8f5f-fb84a807d518" />




**Figure 8.** Medications analysis.




<img width="5970" height="3544" alt="Medication_analysis" src="https://github.com/user-attachments/assets/c94fd7de-05d2-4b05-8b27-f05e4e2f39c6" />




**Figure 9.** Procedures frequencies.




<img width="2969" height="2956" alt="Procedures" src="https://github.com/user-attachments/assets/821a73bd-4241-4360-9def-3825c9c0421b" />





**License:** This workspace adheres to the data use agreements and licensing terms specified by PhysioNet for MIMIC-IV dataset access.
