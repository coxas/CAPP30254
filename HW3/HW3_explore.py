# Alyssa Cox
# Machine Learning
# Homework 3: explore functions

import pandas as pd
import math

def get_df(file):
    '''
    Reads a csv file into a pandas dataframe

    Inputs:
        file: CSV file to read, as a string

    Returns: A pandas data frame
    '''
    df = pd.read_csv(file)
    return df


def get_mean(df, column):
    '''
    Calculates the mean value for a given column.

    Inputs:
            df: a pandas dataframe
            column: specific column from which to generate a mean value

    Returns: mean, an integer
    '''

    if type(column) is str:
        index = df.columns.get_loc(column) + 1
    elif type(column) is int:
        index = column
    list_mean = []
    for tup in df.itertuples():
        if math.isnan(tup[index]):
            continue
        else:
            list_mean.append(tup[index])
    list_mean.sort()
    total = 0
    for i in list_mean:
        total = total + i
    mean = total / len(list_mean)
    new_mean = float("{:.2f}".format(mean))
    return new_mean

def get_max_and_min(df, column):
    '''
    Retrieves the max and min values from a specified column.

     Inputs:
            df: a pandas dataframe
            column: specific column from which to generate max and min

    Returns: a tuple containing (min, max)
    '''

    index = df.columns.get_loc(column) + 1
    list_vals = []
    for tup in df.itertuples():
        list_vals.append(tup[index])
    list_vals.sort()
    min = list_vals[0]
    max = list_vals[-1]
    return(min, max)




