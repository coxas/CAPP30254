# Alyssa Cox
# Machine Learning
# Homework 2

import pandas as pd
from patsy import dmatrices
import math


# For part 1: Read Data
def get_df(file):
    '''
    Returns: A dataframe with a specific column with all values converted
    to datetime objects.

    Inputs:
        file: CSV file to read, as a string
        column: specific column to be converted to datetimes. Must
        contain dates.
                ex: "Creation Date"

    Returns: A dataframe sorted by the column with the datetime objects.
    '''
    df = pd.read_csv(file)
    return df

# Some functions for part 2: Explore Data
def get_count_by_characteristic(file, characteristic):
    '''
    Gets counts, in a dataframe grouped by a
    certain characteristic.

    Inputs:
            file: the CSV file to be read, as a string
            characteristic: the characteristic you want to see counts by

    Returns: dataframe where the first column is the characteristic and
    the second column is the count.
    '''
    df_main = get_df(file)

    sorted = df_main.groupby(characteristic).groups
    list_0 = []
    list_1 = []
    for i in sorted:
        list_0.append(i)
        list_1.append(len(sorted[i]))

    new_df = pd.Series(list_1, list_0)
    return new_df

def get_counts_by_value(file, column, value):
    '''
    Returns the count for any value specified
    It's like get_count_by_characteristic,
    but returns the count for one value, not all of them.

    Inputs:
            file: CSV to be read, as a string
            column: the column containing the specific value
            value: the specific value you want a count for

    Returns: Count, an int
    '''
    df = get_df(file)
    index = df.columns.get_loc(column) + 1
    count = 0
    for tup in df.itertuples():
        if tup[index] == value:
            count += 1
    return count

def get_most(file, column):
    '''
    Gets the specific value from a specific column that has the
    most requests of all the unique values in that column.

    Inputs:
            file: CSV file to be read, as a string
            column: the column from which you want the
            value with the highest count.
    Returns: Tuple containing the count and the value.
                ex: (5600, 60615)
    '''

    df = get_df(file)
    grouped = df.groupby(column).groups
    list_most = []
    for group in grouped:
        list_most.append((len(grouped[group]), group))
    most = 0
    most_tup = None
    for item in list_most:
        if item[0] > most:
            most = item[0]
            most_tup = (item)
    return most_tup

def get_mean(df, column):

    #df = get_df(file)
    #print(type(column))
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
    #df = get_df(file)
    index = df.columns.get_loc(column) + 1
    list_vals = []
    for tup in df.itertuples():
        list_vals.append(tup[index])
    list_vals.sort()
    min = list_vals[0]
    max = list_vals[-1]
    return(min, max)

def get_stat_summ(file, column):
    '''

    Inputs:
            file: csv to be read
            column: column must have integer data
    '''
    df = get_df(file)

    mean = get_mean(file, column)

    index = df.columns.get_loc(column) + 1
    list_vals = []
    for tup in df.itertuples():
        list_vals.append(tup[index])
    list_vals.sort()

    if len(list_vals) % 2 == 0:
        length = len(list_vals)
        med_1 = list_vals[int(length / 2) - 1]
        med_2 = list_vals[int(length / 2)]
        median = (med_1 + med_2) / 2
    elif len(list_vals) % 2 == 1:
        length = len(list_vals)
        median = (length // 2)

    most_tup = get_most(file, column)
    mode = most_tup[1]
    return ("Mean is " + str(mean) + ", median is " + str(median) +
            " , mode is " + str(mode))



def fill_values(df):
    #df = get_df(file)
    dict_means = {}
    headers = df.dtypes.index
    for row in df.itertuples():

            for i in range(len(row)):

                if math.isnan((row[i])):
                    #mean = get_mean(file, i)
                    col_name = headers[i - 1]
                    if col_name in dict_means:
                        mean = dict_means[col_name]
                    else:
                        mean = get_mean(df, i)
                        dict_means[col_name] = mean
                    df.set_value(row[0], col_name, mean)
                    #print(df.iloc[row[0], i-1])

    return df

def discretize(df, column, num_buckets):
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

def make_binary(df, column):
    #df = get_df(file)
    index = df.columns.get_loc(column) + 1
    for row in df.itertuples():
        if row[index] == 0:
            continue
        elif row[index] != 0:
            df.set_value(row[0], column, 1)
    return df

def log_reg(file, dis_var, num_buckets, bin_var):
    df = get_df(file)
    filled_df = fill_values(df)
    dis_df = discretize(filled_df, dis_var, num_buckets)
    bin_df = make_binary(dis_df, bin_var)
    return bin_df



