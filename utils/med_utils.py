import pandas as pd
import numpy as np


def get_abnormal_lab_tests(labs):

    # Filter for tests with reference ranges
    has_ref_range = labs[(labs['ref_range_lower'].notna()) |
                         (labs['ref_range_upper'].notna())].copy()
    # Convert values to numeric
    has_ref_range['valuenum'] = pd.to_numeric(has_ref_range['valuenum'], errors='coerce')
    has_ref_range = has_ref_range.dropna(subset=['valuenum'])
    has_ref_range = has_ref_range[has_ref_range['ref_range_upper'] > 0].copy()  # drop reference ranges[0, 0]

    # Calculate abnormal values
    abnormal_analysis = []

    for itemid in has_ref_range['itemid'].unique():
        item_data = has_ref_range[has_ref_range['itemid'] == itemid]
        lower_ref = item_data['ref_range_lower'].iat[0]
        upper_ref = item_data['ref_range_upper'].iat[0]
        values = item_data['valuenum'].tolist()

        count_abnormal_low = np.multiply((values < lower_ref), 1).sum()
        count_abnormal_high = np.multiply((values > upper_ref), 1).sum()

        abnormal_high = item_data[item_data['valuenum'] > upper_ref]
        abnormal_low = item_data[item_data['valuenum'] < lower_ref]
        abnormal = pd.concat([abnormal_low, abnormal_high])
        if not abnormal.empty:
            abnormal_analysis.append(abnormal)

    abnormal_df = pd.concat(abnormal_analysis)
    return abnormal_df
