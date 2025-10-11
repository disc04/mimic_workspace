from pathlib import Path
from os.path import join
import matplotlib.pyplot as plt
from utils import data_utils
from config.lab_test_context import labs_dashboard
from config.vitals_context import bp_columns, vitals_dashboard

# from utils.data_utils import extract_zip_file, dataframe_from_csv, load_mimic_iv_data, convert_icd_codes
# from utils.mimic_timeseries_utils import mimic_bin_timeseries_data
from config.project_configuration import medications_exclusions

from config.project_configuration import DATA_PATH

mimic4_path = join(Path(__file__).parent.parent,
                   DATA_PATH,
                   'mimic_eda_local-iv-clinical-database-demo-2.2')
results_path = join(Path(__file__).parent.parent, 'results')


def plot_medications(data, results_path=None):
    """
        Visualize medication administration patterns for a single patient
    :param data: dictionary with patient information dataframes
        prescription_medications (pd.DataFrame): Prescription data with time_point, hours_from_admission, Drug_dose
        emar_medications (pd.DataFrame): eMAR bolus data with time_point, hours_from_admission, drug columns
        infusion_medications (pd.DataFrame): Infusion data with time_point, hours_from_admission, drug columns
        transfers (pd.DataFrame): Care unit transfers with time_point, hours_from_admission, care_unit columns
        subject_id (int): Patient ID for plot title
        hadm_id (int): Admission ID for plot title
    :param results_path: Folder to save the figure
    """
    subject_id, hadm_id, diagnosis = data['subject_id'], data['hadm_id'], data['primary_diagnosis']
    time_grid = data['time_grid']

    fig = plt.figure(figsize=(16, 16))
    fig.suptitle(f'Patient: {subject_id}, Admission: {hadm_id}\n Primary diagnosis: {diagnosis}',
                 fontsize=14, fontweight='bold')

    # Panel 1: Medications from prescriptions
    ax1 = plt.axes([0.05, 0.6, 0.7, 0.25])

    medications = data['prescription_medications']
    med_cols = [c for c in medications.columns if c not in ['time_point', 'hours_from_admission']
                and c not in medications_exclusions]

    y_pos1, ax1 = plot_continuous(ax1, df=medications, cols=med_cols, grid=time_grid, y_pos=0,
                                  source_label='', n_examples=10)
    set_ax_design(ax1, grid=time_grid, xlabel='Hours from Admission', ylabel=None, title='Prescriptions medications')
    ax1.set_yticks([])
    plot_care_units_as_vertical_lines(ax1, data['transfers'], annotate=True)

    # Panel 2: Infusions (inputevents) medications and eMAR records
    ax2 = plt.axes([0.05, 0.05, 0.7, 0.45])

    infusions = data['infusion_medications']
    inf_cols = [c for c in infusions.columns if c not in ['time_point', 'hours_from_admission']
                and c not in medications_exclusions]

    y_pos1, ax2 = plot_continuous(ax2, df=infusions, cols=inf_cols, grid=time_grid, y_pos=0,
                                  source_label=" (inputevents)",
                                  n_examples=10)

    emar = data['emar_medications']
    emar_cols = [c for c in emar.columns if c not in ['time_point', 'hours_from_admission']
                 and c not in medications_exclusions]
    y_pos2, ax2 = plot_discrete(ax=ax2, df=emar, time_grid=time_grid, cols=emar_cols, y_pos=y_pos1,
                                source_label=" (eMAR)", n_examples=10)
    set_ax_design(ax2, grid=time_grid, ylabel="", xlabel='Hours from Admission',
                              title='Bolus and infusions medications')
    ax2.set_yticks([])
    plot_care_units_as_vertical_lines(ax2, data['transfers'], annotate=False)

    # plt.tight_layout()
    plt.savefig(f'{results_path}/patient_{subject_id}_admission_{hadm_id}_medications.png',
                dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def plot_discrete(ax, df, time_grid, cols, y_pos, source_label, n_examples=None):
    if n_examples is None:
        n_examples = -1

    markers = ["o", "D", "v", "^", "s", "P", "X"]
    y_pos = y_pos
    for i, col in enumerate(cols[:n_examples]):
        df_times = df[df[col] == 1]['hours_from_admission']
        if not df_times.empty:
            ax.scatter(df_times, [y_pos] * len(df_times), s=50, alpha=0.8, marker=markers[i % len(markers)],
                       label=f"{col[:20]}{source_label}")
            y_pos += 1
    return y_pos, ax


def plot_continuous(ax, df, cols, grid, y_pos, source_label, n_examples=None):
    if n_examples is None:
        n_examples = -1
    if cols:
        y_pos = y_pos
        for col in cols[:n_examples]:  # Limit to 15 medications
            med_active = df[df[col] == 1]
            if not med_active.empty:
                # Plot as continuous line for active periods
                ax.fill_between(med_active['hours_from_admission'], y_pos, y_pos + 0.4,
                                alpha=0.5, label=f"{col[:20]}{source_label}")
                # TODO clean drug names # col.replace('med_', '')[:20] + '...')
                y_pos += 1
    return y_pos, ax


def set_ax_design(ax, grid, xlabel, ylabel, title):
    if xlabel:
        ax.set_xlabel(xlabel, fontweight='bold')
    if ylabel:
        ax.set_ylabel(ylabel, fontweight='bold')
    if title:
        ax.set_title(title, fontweight='bold')
    ax.set_xlim(-0.5, len(grid) + 1)
    # ax.set_yticks([])
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def plot_lines(ax, df, cols, grid, n_examples=None):
    if n_examples is None:
        n_examples = -1
    if cols:
        for col in cols[:n_examples]:
            if df[col].notna().any():
                ax.plot(grid['hours_from_admission'], df[col], label=col[:20], linewidth=2, alpha=0.8)
    return ax


def plot_procedures_timeline(data, results_path=None):
    subject_id, hadm_id, diagnosis = data['subject_id'], data['hadm_id'], data['primary_diagnosis']
    time_grid = data['time_grid']

    fig = plt.figure(figsize=(16, 20))
    fig.suptitle(f'Patient: {subject_id}, Admission: {hadm_id}\n Primary diagnosis: {diagnosis}',
                 fontsize=14, fontweight='bold')

    # Panel 1: Vital Signs
    ax1 = plt.axes([0.05, 0.65, 0.7, 0.25])

    vitals = data["vitals"]
    vitals = data_utils.add_temperature_celsius(vitals, "Temperature_Fahrenheit")

    # plot blood pressure
    sys = vitals[bp_columns[0]]
    dia = vitals[bp_columns[1]]
    ax1.fill_between(vitals["hours_from_admission"], dia, sys, color="red", alpha=0.1, label="BP Range")

    # plot rest of signs
    vitals_cols = [c for c in vitals.columns if c in vitals_dashboard and c not in bp_columns]
    for i, col in enumerate(vitals_cols):
        col_df = vitals[[col, 'hours_from_admission']].copy().dropna()
        ax1.scatter(time_grid['hours_from_admission'], vitals[col], label=col[:30], s=50, zorder=2)
        ax1.plot(col_df['hours_from_admission'], col_df[col], linewidth=2, alpha=0.8)

    set_ax_design(ax1, grid=time_grid, xlabel='Hour from Admission', ylabel=None, title='Vital Signs')
    plot_care_units_as_vertical_lines(ax1, data['transfers'], annotate=True)

    # Panel 2: Laboratory Values
    ax2 = plt.axes([0.05, 0.35, 0.7, 0.25])
    labs = data['labs']
    selected_cols = [c for c in labs.columns if c in labs_dashboard]

    for i, col in enumerate(selected_cols):
        col_df = labs[[col, 'hours_from_admission']].copy().dropna()
        ax2.scatter(time_grid['hours_from_admission'], labs[col], label=col[:30], s=50, zorder=2)
        ax2.plot(col_df['hours_from_admission'], col_df[col], linestyle='-', linewidth=2,
                 alpha=0.8, zorder=1)

    set_ax_design(ax2, grid=time_grid,  ylabel=None, xlabel='Hours from Admission', title='Laboratory Values',)
    plot_care_units_as_vertical_lines(ax2, data['transfers'], annotate=False)

    # Panel 3: Procedures
    ax3 = plt.axes([0.05, 0.05, 0.7, 0.25])
    # procedures will be filtered by time and selected earliest procedures
    procedures = data['procedures']
    procedures_cols = [c for c in procedures.columns if c not in ['time_point', 'hours_from_admission'] and
                       not c.endswith('_present')]
    icu_procedures = data['icu_procedures']
    icu_procedures_cols = [c for c in icu_procedures.columns if c not in ['time_point', 'hours_from_admission'] and
                           not c.endswith('_present') and not c.endswith('_Received') and not c.endswith('_Sent')]

    y_pos1, ax3 = plot_continuous(ax3, df=icu_procedures, cols=icu_procedures_cols, grid=time_grid, y_pos=0,
                                  source_label=" (ICU)",
                                  n_examples=None)
    y_pos2, ax3 = plot_discrete(ax=ax3, df=procedures, time_grid=time_grid, cols=procedures_cols, y_pos=y_pos1,
                                source_label=" (Hospital)", n_examples=None)

    set_ax_design(ax3, time_grid, xlabel='Hours from Admission', ylabel=None, title='Procedures')
    plot_care_units_as_vertical_lines(ax3, data['transfers'], annotate=False)

    plt.savefig(f'{results_path}/patient_{subject_id}_admission_{hadm_id}_labs_procedures.png',
                dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def plot_care_units_as_vertical_lines(ax, df, annotate=True):
    care_units = [col for col in df.columns if col not in ['hours_from_admission', 'time_point']]

    for unit in care_units:
        active_times = df.loc[df[unit] == 1, 'hours_from_admission']
        for t in active_times:
            plt.axvline(x=t, linestyle='-', color='gray', alpha=0.7)
            if annotate:
                ax.text(t, ax.get_ylim()[1] * 1.005,  unit.replace("_", " "),
                        rotation=30, fontsize=12, alpha=0.7, fontweight='bold')

