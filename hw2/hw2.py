# Alyssa Cox
# Machine Learning
# Homework 2

import pandas as pd
import matplotlib.pyplot as plt
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

def get_mean(file, column):

    df = get_df(file)
    index = df.columns.get_loc(column) + 1
    list = []
    for tup in df.itertuples():
        list.append(tup[index])
    list.sort()
    total = 0
    for i in list:
        total = total + i
    mean = total / len(list)
    new_mean = float("{:.2f}".format(mean))
    return new_mean


def get_stat_summ(file, column):
    '''

    Inputs:
            file: csv to be read
            column: column must have integer data
    '''
    df = get_df(file)

    mean = get_mean(file, column)

    index = df.columns.get_loc(column) + 1
    list = []
    for tup in df.itertuples():
        list.append(tup[index])
    list.sort()

    if len(list) % 2 == 0:
        length = len(list)
        med_1 = list[int(length / 2) - 1]
        med_2 = list[int(length / 2)]
        median = (med_1 + med_2) / 2
    elif len(list) % 2 == 1:
        length = len(list)
        median = (length // 2)

    most_tup = get_most(file, column)
    mode = most_tup[1]
    return ("Mean is " + str(mean) + ", median is " + str(median) +
            " , mode is " + str(mode))


def fill_values(file):
    df = get_df(file)
    list_cols = []
    for row in df.itertuples():
        if row[0] == 0:
            for i in range(len(row)):
                print(type(row[i]))





