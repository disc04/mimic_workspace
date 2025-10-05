import pandas as pd
import numpy as np
from os.path import join
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
plt.style.use("seaborn-v0_8")
# sns.set_palette("husl")
# plt.style.use("default")
sns.set_palette("Set2")
warnings.filterwarnings('ignore')


def plot_demographics(df, data_type, save_path):
    """Create demographics plots"""
    df = df.copy()
    df = df.replace([np.inf, -np.inf], np.nan)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f"{data_type} Demographics: Age and Gender Distributions", fontsize=16, fontweight="bold")

    # Age Distribution (Histogram)
    axes[0, 0].hist(df["anchor_age"], bins=20, alpha=0.7, color="skyblue", edgecolor="black")
    axes[0, 0].set_title("Age Distribution", fontweight="bold")
    axes[0, 0].set_xlabel("Age (years)")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].grid(True, alpha=0.3)

    # Add statistics text
    age_mean = df["anchor_age"].mean()
    age_median = df["anchor_age"].median()

    if np.isfinite(age_mean):
        axes[0, 0].axvline(age_mean, color="red", linestyle="--",
                           alpha=0.8, label=f"Mean: {age_mean:.1f}")
    if np.isfinite(age_median):
        axes[0, 0].axvline(age_median, color="green", linestyle="--",
                           alpha=0.8, label=f"Median: {age_median:.1f}")
    axes[0, 0].legend()

    # Gender Distribution (Bar Chart)
    gender_counts = df["gender"].value_counts()
    bars = axes[0, 1].bar(gender_counts.index, gender_counts.values, alpha=0.8, color=["lightcoral", "lightblue"])
    axes[0, 1].set_title("Gender Distribution", fontweight="bold")
    axes[0, 1].set_xlabel("Gender")
    axes[0, 1].set_ylabel("Count")

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width() / 2., height,
                        f"{int(height)} ({height / len(df) * 100:.1f}%)",
                        ha="center", va="bottom")

    # Age Distribution by Gender (Box Plot)
    sns.boxplot(data=df, x="gender", y="anchor_age", ax=axes[1, 0])
    axes[1, 0].set_title("Age Distribution by Gender", fontweight="bold")
    axes[1, 0].set_xlabel("Gender")
    axes[1, 0].set_ylabel("Age (years)")

    # Mortality by age (if available)
    if "hospital_expire_flag" in df.columns:
        df["age_group"] = df["age_group"].astype("str")
        mortality_by_age = df.groupby("age_group")["hospital_expire_flag"].agg(["count", "sum"])
        mortality_by_age["mortality_rate"] = mortality_by_age["sum"] / mortality_by_age["count"] * 100

        bars = axes[1, 1].bar(mortality_by_age.index, mortality_by_age["mortality_rate"])
        axes[1, 1].set_title("Mortality Rate by Age")
        axes[1, 1].set_xlabel("Age group")
        axes[1, 1].set_ylabel("Mortality Rate (%)")
        axes[1, 1].tick_params(axis="x", rotation=45)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width() / 2., height,
                            f"{height:.1f}%", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_length_of_stay(demo_data, data_type, save_path):
    """Create length of stay analysis plots"""
    los_col = "los_days" if data_type == "Hospital" else "los"

    # Remove outliers for better visualization
    los_data = demo_data[demo_data[los_col] <= demo_data[los_col].quantile(0.95)]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(f"{data_type} Length of Stay Analysis", fontsize=16, fontweight="bold")

    # Overall LOS distribution
    axes[0].hist(los_data[los_col], bins=50, alpha=0.7, edgecolor="black")
    axes[0].set_title(f"{data_type} Length of Stay Distribution")
    axes[0].set_xlabel("Length of Stay (days)")
    axes[0].set_ylabel("Frequency")
    axes[0].axvline(los_data[los_col].median(), color="red", linestyle="--",
                       label=f"Median: {los_data[los_col].median():.1f} days")
    axes[0].legend()

    # LOS by age group
    los_data = los_data.sort_values(by="age_group", ascending=True).reset_index(drop=True)
    if "age_group" in los_data.columns:
        sns.boxplot(data=los_data, x="age_group", y=los_col, ax=axes[1])
        axes[1].set_title(f"{data_type} LOS by Age Group")
        axes[1].set_xlabel("Age Group")
        axes[1].set_ylabel("Length of Stay (days)")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_clinical_conditions_analysis(diagnoses, save_path):
    """Analyze clinical conditions from ICD codes"""

    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    fig.suptitle("Hospital Clinical Conditions Analysis", fontsize=16, fontweight="bold")

    # Top 15 primary diagnoses (seq_num = 1)
    primary_diag = diagnoses[diagnoses["seq_num"] == 1]
    top_primary = primary_diag["long_title"].value_counts().head(15)
    y_pos = np.arange(len(top_primary))
    ax.barh(y_pos, top_primary.values)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([title[:50] + "..." if len(title) > 50 else title
                               for title in top_primary.index])
    ax.invert_yaxis()
    ax.set_xlabel("Number of Cases")
    ax.set_title("Top 15 Primary Diagnoses")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_services_analysis(hosp_tables, save_path):
    """Analyze hospital services"""

    services = hosp_tables["services"]
    curr_service_counts = services["curr_service"].value_counts().head(15)
    # service_descriptions = service_codes_dict

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("Hospital Services Analysis", fontsize=16, fontweight="bold")

    # Service types pie chart (grouped by medical vs surgical)
    service_types = []

    for service in curr_service_counts.index:
        if "SURG" in service or service in ["CSURG", "NSURG", "ORTHO", "PSURG", "TSURG", "VSURG"]:
            service_types.append("Surgical")
        elif service in ["MED", "CMED", "NMED", "OMED"]:
            service_types.append("Medical")
        elif service in ["NB", "NBB", "OBS"]:
            service_types.append("Maternal/Neonatal")
        else:
            service_types.append("Specialty")

    service_type_df = pd.DataFrame({"service": curr_service_counts.index,
                                    "count": curr_service_counts.values,
                                    "type": service_types})
    type_counts = service_type_df.groupby("type")["count"].sum()

    axes[0, 0].pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%")
    axes[0, 0].set_title("Service Types Distribution")

    # Current service distribution
    axes[0, 1].bar(range(len(curr_service_counts)), curr_service_counts.values)
    axes[0, 1].set_xticks(range(len(curr_service_counts)))
    axes[0, 1].set_xticklabels(curr_service_counts.index, rotation=45)
    axes[0, 1].set_xlabel("Service")
    axes[0, 1].set_ylabel("Number of Admissions")
    axes[0, 1].set_title("Top 15 Current Services")

    # Service transfers (when prev_service != curr_service)
    transfers = services[services["prev_service"] != services["curr_service"]]
    if not transfers.empty:
        transfer_counts = transfers.groupby(["prev_service", "curr_service"]).size().reset_index(name="count")
        top_transfers = transfer_counts.nlargest(10, "count")

        transfer_labels = [f"{row['prev_service']} → {row['curr_service']}"
                           for _, row in top_transfers.iterrows()]

        axes[1, 0].barh(range(len(top_transfers)), top_transfers["count"])
        axes[1, 0].set_yticks(range(len(top_transfers)))
        axes[1, 0].set_yticklabels(transfer_labels)
        axes[1, 0].invert_yaxis()
        axes[1, 0].set_xlabel("Number of Transfers")
        axes[1, 0].set_title("Top 10 Service Transfers")

    #  Number of service changes per patient
    service_changes = services.groupby("subject_id").size() - 1  # -1 because first entry is not a change
    service_changes = service_changes[service_changes >= 0]

    axes[1, 1].hist(service_changes, bins=range(0, min(10, service_changes.max() + 2)),
                    alpha=0.7, edgecolor="black")
    axes[1, 1].set_xlabel("Number of Service Changes per Patient")
    axes[1, 1].set_ylabel("Frequency")
    axes[1, 1].set_title("Distribution of Service Changes per Patient")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_admission_types_analysis(admissions_data, save_path):
    """Create admission types analysis plots"""

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Admission Types Analysis: Emergency vs Elective", fontsize=16, fontweight="bold")

    # Overall admission type distribution
    admission_counts = admissions_data["admission_category"].value_counts()
    axes[0, 0].pie(admission_counts.values, labels=admission_counts.index, autopct="%1.1f%%", startangle=90)
    axes[0, 0].set_title("Admission Categories Distribution")

    # Length of stay by admission category
    los_data = admissions_data[admissions_data["los_days"] <= admissions_data["los_days"].quantile(0.95)]
    sns.boxplot(data=los_data, x="admission_category", y="los_days", ax=axes[0, 1])
    axes[0, 1].set_title("Length of Stay by Admission Category")
    axes[0, 1].set_ylabel("Length of Stay (days)")

    #  Detailed admission types
    detailed_counts = admissions_data["admission_type"].value_counts()
    axes[1, 0].barh(range(len(detailed_counts)), detailed_counts.values, )
    axes[1, 0].set_yticks(range(len(detailed_counts)))
    axes[1, 0].set_yticklabels(detailed_counts.index, ha="right")
    axes[1, 0].set_title("Detailed Admission Types")
    axes[1, 0].set_xlabel("Number of Admissions")
    axes[1, 0].invert_yaxis()

    # Mortality by admission category
    if "hospital_expire_flag" in admissions_data.columns:
        mortality_by_category = admissions_data.groupby("admission_category")["hospital_expire_flag"].agg(
            ["count", "sum"])
        mortality_by_category["mortality_rate"] = mortality_by_category["sum"] / mortality_by_category["count"] * 100
        mortality_by_category = mortality_by_category.sort_values(by="admission_category", ascending=False)
        bars = axes[1, 1].bar(mortality_by_category.index, mortality_by_category["mortality_rate"])
        axes[1, 1].set_title("Mortality Rate by Admission Category")
        axes[1, 1].set_ylabel("Mortality Rate (%)")

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width() / 2., height,
                            f"{height:.1f}%", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_readmission_analysis(readmissions_df, patient_readmissions, save_path):
    """Create readmission analysis plots"""

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("Readmission Analysis", fontsize=16, fontweight="bold")

    # Distribution of total admissions per patient
    admission_counts = patient_readmissions["total_admissions"].value_counts().sort_index()
    axes[0].barh(admission_counts.index[:10], admission_counts.values[:10])
    axes[0].set_title("Distribution of Total Admissions per Patient")
    axes[0].set_ylabel("Number of Admissions")
    axes[0].set_xlabel("Number of Patients")
    axes[0].invert_yaxis()

    # Time between admissions
    if len(readmissions_df) > 0:
        days_between = readmissions_df["days_between_admissions"]
        days_between_filtered = days_between[days_between <= 365]  # Filter extreme outliers

        axes[1].hist(days_between_filtered, bins=50, alpha=0.7, edgecolor="black")
        axes[1].set_title("Days Between Admissions")
        axes[1].set_xlabel("Days Between Admissions")
        axes[1].set_ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_severity_scores(severity_scores, results_path, filename):

    if severity_scores is not None:
        available_types = severity_scores["label"].unique()
        # print(f"Available severity_scores types: {severity_scores.label.unique()}")
        for s_type in available_types:
            fig, ax = plt.subplots(1, 1, figsize=(6, 6))
            fig.suptitle("ICU Severity Scores Analysis", fontsize=16, fontweight="bold")
            score_data = severity_scores[severity_scores["label"] == s_type]["valuenum"]
            if len(score_data) > 0:
                ax.hist(score_data, bins=30, alpha=0.7, edgecolor="black")
                ax.set_title(f"{s_type} Score Distribution")
                ax.set_xlabel("Score Value")
                ax.set_ylabel("Frequency")
                ax.axvline(score_data.median(), color="red", linestyle="--",
                                label=f"Median: {score_data.median():.1f}")
                ax.legend()
                plt.tight_layout()
                plt.savefig(join(results_path,  s_type + "_" + filename), dpi=300, bbox_inches="tight")
                plt.show()
                plt.close()


def plot_mortality_analysis(hosp_mortality, icu_mortality, save_path):
    """Create mortality analysis plots"""

    fig, axes = plt.subplots(2,  figsize=(11, 11))
    fig.suptitle("Mortality Analysis by Condition", fontsize=16, fontweight="bold")

    # Top 20 highest mortality rate conditions (hospital)
    top_mortality = hosp_mortality.nlargest(20, "mortality_rate")

    y_pos = np.arange(len(top_mortality))
    axes[0].barh(y_pos, top_mortality["mortality_rate"])
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels([label[:40] + "..." if len(label) > 40 else label
                                for label in top_mortality.index], fontsize=12)
    axes[0].set_xlabel("Mortality Rate (%)")
    axes[0].set_title("Conditions by Hospital Mortality Rate")
    axes[0].invert_yaxis()

    # ICU mortality comparison
    if icu_mortality is not None:
        top_icu_mortality = icu_mortality.nlargest(15, "icu_mortality_rate")

        y_pos = np.arange(len(top_icu_mortality))
        axes[1].barh(y_pos, top_icu_mortality["icu_mortality_rate"])
        axes[1].set_yticks(y_pos)
        axes[1].set_yticklabels([label[:40] + "..." if len(label) > 40 else label
                                    for label in top_icu_mortality.index], fontsize=12)
        axes[1].set_xlabel("ICU Mortality Rate (%)")
        axes[1].set_title("Conditions by ICU Mortality Rate")
        axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_lab_tests_frequency(test_frequency,  tests_per_admission, save_path):
    fig, axes = plt.subplots(2,  figsize=(12, 12))
    fig.suptitle("Laboratory Test Frequency Analysis", fontsize=16, fontweight="bold")

    # Top 20 most frequent tests
    top_20_tests = test_frequency.head(20)
    y_pos = np.arange(len(top_20_tests))
    axes[0].barh(y_pos, top_20_tests["test_count"])
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels([label[:40] + "..." if len(label) > 40 else label
                                for label in top_20_tests["label"]], fontsize=8)
    axes[0].set_xlabel("Number of Tests")
    axes[0].set_title("Top 20 Most Frequently Ordered Lab Tests")
    axes[0].invert_yaxis()

    # Tests per admission distribution
    if tests_per_admission is not None:
        axes[1].hist(tests_per_admission, bins=50, alpha=0.7, edgecolor="black")
        axes[1].set_xlabel("Number of Tests per Admission")
        axes[1].set_ylabel("Number of Admissions")
        axes[1].set_title("Distribution of Tests per Admission")
        axes[1].axvline(tests_per_admission.median(), color="red", linestyle="--",
                           label=f"Median: {tests_per_admission.median():.0f}")
        axes[1].legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_prescribed_medications(drug_frequency, category_frequency, drug_type_frequency,
                                route_frequency, prescriptions_per_patient, unique_drugs_per_patient,
                                save_path):
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle("Medication Analysis: Most Prescribed Drugs and Categories", fontsize=16, fontweight="bold")

        # Top 20 most prescribed medications
        top_20_drugs = drug_frequency.head(20)
        y_pos = np.arange(len(top_20_drugs))
        axes[0, 0].barh(y_pos, top_20_drugs.values)
        axes[0, 0].set_yticks(y_pos)
        axes[0, 0].set_yticklabels([drug[:25] + "..." if len(drug) > 25 else drug
                                    for drug in top_20_drugs.index], fontsize=8)
        axes[0, 0].set_xlabel("Number of Prescriptions")
        axes[0, 0].set_title("Top 20 Most Prescribed Medications")
        axes[0, 0].invert_yaxis()

        # Drug categories
        axes[0, 1].pie(category_frequency.values, labels=category_frequency.index, autopct="%1.1f%%", startangle=90)
        axes[0, 1].set_title("Medication Categories Distribution")

        # Drug type distribution (if available)
        if drug_type_frequency is not None:
            axes[0, 2].bar(range(len(drug_type_frequency)), drug_type_frequency.values)
            axes[0, 2].set_xticks(range(len(drug_type_frequency)))
            axes[0, 2].set_xticklabels(drug_type_frequency.index, rotation=45, ha="right")
            axes[0, 2].set_ylabel("Number of Prescriptions")
            axes[0, 2].set_title("Drug Types Distribution")

        # Prescriptions per patient
        axes[1, 0].hist(prescriptions_per_patient, bins=50, alpha=0.7, edgecolor="black")
        axes[1, 0].set_xlabel("Number of Prescriptions per Patient")
        axes[1, 0].set_ylabel("Number of Patients")
        axes[1, 0].set_title("Distribution of Prescriptions per Patient")
        axes[1, 0].axvline(prescriptions_per_patient.median(), color="red", linestyle="--",
                           label=f"Median: {prescriptions_per_patient.median():.0f}")
        axes[1, 0].legend()

        # Unique drugs per patient
        axes[1, 1].hist(unique_drugs_per_patient, bins=30, alpha=0.7, edgecolor="black")
        axes[1, 1].set_xlabel("Number of Unique Drugs per Patient")
        axes[1, 1].set_ylabel("Number of Patients")
        axes[1, 1].set_title("Distribution of Unique Drugs per Patient")
        axes[1, 1].axvline(unique_drugs_per_patient.median(), color="red", linestyle="--",
                           label=f"Median: {unique_drugs_per_patient.median():.0f}")
        axes[1, 1].legend()

        # Route of administration (if available)
        if route_frequency is not None:
            top_routes = route_frequency.head(10)
            axes[1, 2].bar(range(len(top_routes)), top_routes.values)
            axes[1, 2].set_xticks(range(len(top_routes)))
            axes[1, 2].set_xticklabels(top_routes.index, rotation=45, ha="right")
            axes[1, 2].set_ylabel("Number of Prescriptions")
            axes[1, 2].set_title("Top 10 Routes of Administration")

        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close()


def plot_procedures(hosp_procedures, icu_procedures, save_path):
    fig, axes = plt.subplots(2, figsize=(10, 10))
    fig.suptitle("Procedure Frequency Analysis", fontsize=18, fontweight="bold")

    # Top 20 hosp_procedures
    top_20_procedures = hosp_procedures["procedure_frequency"].head(20)
    y_pos = np.arange(len(top_20_procedures))
    axes[0].barh(y_pos, top_20_procedures.values)
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels([proc[:40] + "..." if len(proc) > 40 else proc
                                            for proc in top_20_procedures.index], fontsize=8)
    axes[0].set_xlabel("Number of Procedures")
    axes[0].set_title("Top 20 Hospital Procedures")
    axes[0].invert_yaxis()

    # Top 20 ICU procedures
    top_20_icu_procedures = icu_procedures["procedure_frequency"].head(21)
    if "nan nan nan" in top_20_icu_procedures.keys():
        del top_20_icu_procedures["nan nan nan"]
    top_20_icu_procedures.index = [i.replace("1.0 nan", "") for i in top_20_icu_procedures.index]
    y_pos = np.arange(len(top_20_icu_procedures))
    axes[1].barh(y_pos, top_20_icu_procedures.values)
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels([proc.replace[:40] + "..." if len(proc) > 40 else proc
                                            for proc in top_20_icu_procedures.index], fontsize=8)
    axes[1].set_xlabel("Number of Procedures")
    axes[1].set_title("Top 20 ICU Procedures")
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()
