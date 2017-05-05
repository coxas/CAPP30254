# Alyssa Cox
# Machine Learning HW3: Pre-processing of Data

import math
import pandas as pd
from HW3_explore import get_df, get_mean, get_max_and_min

def find_nans(df):
    col_nans = []
    headers = df.dtypes.index
    for row in df.itertuples():
            for i in range(len(row)):
                if math.isnan((row[i])):
                    col_name = headers[i - 1]
                    if col_name in col_nans:
                        continue
                    else:
                        col_nans.append(col_name)
    return col_nans

def fill_values(df, column, fill_val="mean"):
    '''
    Fills in NaN cell values with either the mean from that column or a pre-determined value

    Inputs:
            df: a pandas data frame
            column: column to fill in nan values
            fill_val: default is mean value of column, but can be specified by user for
            categorical or binary vars

    Returns: pandas data frame with no missing values for the column specified
    '''

    if fill_val == "mean":
        mean = get_mean(df, column)
        df[column].fillna(mean, inplace=True)
    else:
        df[column].fillna(fill_val, inplace=True)

    return df

def discretize(df, column, num_buckets):
    '''
    Turns a continuous variable into a discrete one by separating
    continuous values into intervals

    Inputs:
            df: a pandas data frame
            column: specific column to discretize (must have numerical data)
            num_buckets: the number of intervals to separate the data into

    Returns: pandas data frame where the value in the specified column is the maximum
    value in the interval into which the original data fell.
        ex: values range from 0 - 100, user specifies 10 buckets/intervals, [0-10],[11-20], etc.
            a row with the value 15 will fit into interval [11-20] and will thus be replaced
            with the number 20.
    '''
    index = df.columns.get_loc(column) + 1
    min = get_max_and_min(df, column)[0]
    max = get_max_and_min(df, column)[1]
    partition = round((max - min) / num_buckets)
    for i in range(num_buckets):
        for row in df.itertuples():
            if row[index] > partition * (i) and row[index] < partition * (i + 1):
                range_part = partition * (i + 1)
                df.set_value(row[0], column, range_part)
    return df

def make_dummies(df, column_list):
    '''
       Turns a categorical variable into a binary/dummy variable.

       Inputs:
               df: a pandas dataframe
               columns: the columns to make binary, as a list

       Returns: dataframe with columns added that correspond to the dummy vars and values
       '''

    dummies_df = pd.get_dummies(df, columns=column_list)
    return dummies_df
