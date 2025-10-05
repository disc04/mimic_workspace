import pandas as pd
import numpy as np
from datetime import timedelta
from utils.data_utils import (get_admit_discharge_times, clean_column_name,
                              date_and_time_to_datetime, filter_by_time_window_consistency)
from configuration import mimic_iv_data_sources


def generate_single_admission_time_series_data(data_dict: dict,
                                               time_resolution_hours: float,
                                               observation_window_hours: float
                                               ) -> tuple:
    """
    Generate time-series data for a single admission, aligned to a common time grid.
    :param data_dict: Dictionary containing different events DataFrames.
    :param time_resolution_hours: Bin width in hours for the time grid.
    :param observation_window_hours: float
    :return: Dictionary with time grid and binned time-series for each data type.
    """
    messages = []
    admit_time, discharge_time, message = get_admit_discharge_times(data_dict, adjust_start=True)
    messages.append(message)

    time_grid = create_time_grid(data_dict, time_resolution_hours, observation_window_hours)

    results = {"admit_time": admit_time, "discharge_time": discharge_time, "time_grid": time_grid}

    for src in mimic_iv_data_sources:

        df = data_dict.get(src["name"], pd.DataFrame())
        if df is not None and not df.empty:
            if src["datatype"] == "continuous":
                df, message = filter_by_time_window_consistency(df=df,
                                                                start_window=admit_time,
                                                                end_window=discharge_time,
                                                                start_event_col=src["start_col"],
                                                                end_event_col=src["end_col"],
                                                                adjust_start=True,
                                                                adjust_end=True)
                if message:
                    messages.append(f"{src['name']} filter_by_time_window_consistency: {message}")
                results[src["name"]] = continuous_to_ts(df=df,
                                                        time_grid=time_grid,
                                                        start_col=src["start_col"],
                                                        end_col=src["end_col"],
                                                        label_col=src["label_col"],
                                                        value_col=src["value_col"])

            elif src["datatype"] == "discrete":
                df, message = filter_by_time_window_consistency(df=df,
                                                                start_window=admit_time,
                                                                end_window=discharge_time,
                                                                start_event_col=src["time_col"],
                                                                end_event_col=None,
                                                                adjust_start=True,
                                                                adjust_end=False)
                if message:
                    messages.append(f"{src['name']} filter_by_time_window_consistency: {message}")
                results[src["name"]] = discrete_to_ts(df.copy(),
                                                      time_column=src["time_col"],
                                                      time_grid=time_grid,
                                                      value_col=src["value_col"],
                                                      label_col=src["label_col"])
            elif src["datatype"] == "categorical":
                results[src["name"]] = categorical_to_ts(df=df.copy(),
                                                         time_grid=time_grid,
                                                         event_column=src["label_col"],
                                                         time_column=src["time_col"], )

            else:
                messages.append(f"{src['name']} unknown datatype: {src['datatype']}")

    return results, messages


def create_time_grid(data_dict: dict,
                     time_resolution_hours: float,
                     observation_window_hours: float | None
                     ) -> pd.DataFrame:
    """
    Create a regular time grid for an admission episode.
    :param data_dict: Dictionary containing "admit_time" and "discharge_time" as pd.Timestamp.
    :param time_resolution_hours: Spacing between grid points, in hours.
    :param observation_window_hours: Length of observation window in hours. If None, extends until discharge_time.
    :return: DataFrame with "time_point" > pd.Timestamp grid points and
         "hours_from_admission" > elapsed hours since admission
    """
    admit_time = pd.to_datetime(data_dict["admittime"])
    discharge_time = pd.to_datetime(data_dict["dischtime"])

    # Determine end time: earliest of observation window or discharge
    if observation_window_hours is not None:
        max_end = admit_time + timedelta(hours=observation_window_hours)
        end_time = min(max_end, discharge_time)
    else:
        end_time = discharge_time
    if end_time < admit_time:  # Ensure valid range
        raise ValueError("End time is earlier than admit time. Check input data.")

    freq = f"{time_resolution_hours}H"  # Generate time grid
    time_points = pd.date_range(start=admit_time, end=end_time, freq=freq)

    return pd.DataFrame({
        "time_point": time_points,
        "hours_from_admission": (time_points - admit_time) / pd.Timedelta(hours=1)})


def continuous_to_ts(df: pd.DataFrame,
                     time_grid: pd.DataFrame,
                     start_col: str,
                     end_col: str,
                     label_col: str,
                     value_col: str | None = None,
                     default_value: int | float = 0
                     ) -> pd.DataFrame:
    """
    Converts interval-based events (e.g., medications, ICU procedures)
    into a time-series aligned to a time grid.
    :param df: Input events with start, end, and label columns.
    :param time_grid: Target time grid with "time_point".
    :param start_col: Column with event start times.
    :param end_col: Column with event end times.
    :param label_col: Column identifying the event label/category.
    :param value_col: Numeric values to assign instead of binary 0/1 (e.g., dose).
    :param default_value: Value to assign when event is not active (default=0).
    :return ts_df: Time-series DataFrame aligned to `time_grid`, with one column per unique label in df.
    """
    if df.empty:
        return time_grid

    ts_df = time_grid.copy()
    df = df.copy()
    df[start_col] = pd.to_datetime(df[start_col])
    df[end_col] = pd.to_datetime(df[end_col]).fillna(
        time_grid["time_point"].iloc[-1] + pd.Timedelta(hours=1))

    # Initialize columns
    cols = {}
    for label in df[label_col].dropna().unique():
        clean_name = clean_column_name(label)
        cols[clean_name] = default_value

    # Add all columns at once
    ts_df = pd.concat([ts_df, pd.DataFrame(cols, index=ts_df.index)], axis=1)

    # For each time point, mark active events
    # Build mapping from labels to cleaned column names
    label_map = {label: clean_column_name(label) for label in df[label_col].unique()}

    time_points = time_grid["time_point"].to_numpy()

    for label, col in label_map.items():
        # Choose dtype depending on whether a value_col is used
        if value_col is None:
            ts_df[col] = np.zeros(len(time_grid), dtype=np.int8)  # categorical presence
        else:
            ts_df[col] = np.zeros(len(time_grid), dtype=df[value_col].dtype)  # same dtype as source

    # For each event interval, fill in matching time indices
    for _, row in df.iterrows():
        start, end, label = row[start_col], row[end_col], row[label_col]
        col = label_map[label]

        mask = (time_points >= start) & (time_points < end)
        if value_col is None:
            ts_df.loc[mask, col] = 1
        else:
            ts_df.loc[mask, col] = np.array(row[value_col], dtype=ts_df[col].dtype)
    return ts_df


def discrete_to_ts(df: pd.DataFrame,
                   time_column: str,
                   time_grid: pd.DataFrame,
                   value_col: str,
                   label_col: str
                   ) -> pd.DataFrame:
    """
    Bin irregular time-series data into a fixed time grid.
    :param df: Input events with time, label, and values.
    :param time_column: Column containing timestamps.
    :param time_grid: Reference grid with "time_point".
    :param value_col: Column containing numeric values.
    :param label_col: Column containing categorical labels (e.g., measurement names).
    :returns ts_df: Time-series aligned to the grid with one column per label and
        an additional "_present" flag column per label.
    """
    ts_df = time_grid.copy().reset_index(drop=True)
    n_bins = len(time_grid)

    # get resolution from grid
    resolution = time_grid["time_point"].diff().dropna().min()
    last_edge = time_grid["time_point"].iloc[-1] + resolution

    bins = pd.concat([time_grid["time_point"], pd.Series([last_edge])], ignore_index=True)
    df["bin"] = pd.cut(df[time_column], bins=bins, right=False, labels=False)

    new_cols = {}
    grouped = (df.groupby([label_col, "bin"])[value_col]
               .agg(["mean", "count"])
               .reset_index())
    for label, group in grouped.groupby(label_col):
        clean_name = clean_column_name(label)
        mean_series = group.set_index("bin")["mean"].reindex(range(n_bins))
        count_series = group.set_index("bin")["count"].reindex(range(n_bins), fill_value=0)

        # if we want forward-fill the means: new_cols[clean_name] = mean_series.ffill().to_numpy()
        new_cols[clean_name] = mean_series.to_numpy()
        new_cols[f"{clean_name}_present"] = (count_series > 0).astype(int).to_numpy()

    cols_df = pd.DataFrame(new_cols, index=ts_df.index)
    ts_df = pd.concat([ts_df, cols_df], axis=1)

    return ts_df.copy()


def categorical_to_ts(df, time_grid, event_column, time_column):
    """
    Convert categorical event data into a time-series aligned to a time grid.
    :param df: Event data with at least [time_col, value_col].
    :param time_grid: Target time grid with "time_point".
    :param event_column: Name of the categorical value column in df.
    :param time_column: Name of the time column in df.
    :return ts_df: Time-series DataFrame aligned to `time_grid`.
    """
    if df.empty or event_column not in df.columns:
        return time_grid

    df = date_and_time_to_datetime(df=df, time_column=time_column)
    df.rename(columns={time_column: "time_point", event_column: "label"}, inplace=True)
    df = df.dropna(subset=["label"])
    bin_edges = pd.concat([time_grid["time_point"], pd.Series([time_grid["time_point"].iloc[-1] +
                                                               pd.Timedelta(days=1)])])
    df["bin"] = pd.cut(df["time_point"], bins=bin_edges, labels=False, right=False)
    df_ts = time_grid.copy()

    for name in df["label"].unique():
        df_ts[clean_column_name(name)] = 0
        bins_with_event = df[df["label"] == name]["bin"].dropna().astype(int)
        df_ts.loc[bins_with_event, clean_column_name(name)] = 1

    return df_ts
