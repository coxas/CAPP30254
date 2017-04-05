# Alyssa Cox
# Machine Learning
# Homework 1, part 1

import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import timedelta

def get_df(file, column):
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
    df[column] = pd.to_datetime(df[column])

    #sort by datetime, from earliest
    sorted = df.sort([column])
    return sorted

def requests_over_time(df):
    '''
    Calculates both the span of time and the number of requests for use
    in creating a plot from matplotlib to show requests over time.

    Inputs:
            df: a dataframe

    Returns: A tuple of two lists, one for the x axis of the plot (dates over time) and
    one for the y-axis of the plot (requests over time).
    '''
    list_y = []
    total = 0
    list_x = []
    for row in df.itertuples():
        s = str(row[1])
        date = s.replace(" 00:00:00", "")
        new_date = date.replace("-", "")
        if new_date.isdigit():
            list_x.append(int(new_date))

    # the number of requests is equal to the length of list_x.
    # for each request, the total number of requests increases by one.
    for i in range(len(list_x)):
        total = total + 1
        list_y.append(total)

    return(list_x, list_y)

def get_subgroups(file, column, subgroup):
    '''
    Creates a dataframe that only contains rows from a certain subgroup.

    Inputs:
            file: the CSV file to be read, as a string
            column: the column containing the subgroup, as a string
                    ex: for Graffiti, "What Type of Surface is the Graffiti on?"
                        if you want to receive info about graffiti on metal
                        specifically. Can also be "ZIP Code", "Ward", etc.
            subgroup: the specific subgroup to return, as a string
                    ex: for the example above, the subgroup would be "Metal"
    Returns: a dataframe
    '''

    df = pd.read_csv(file)

    grouped = df.groupby(column).groups
    list_sorted = []

    for subtype in grouped.items():
        list_sorted.append(subtype[0])

    new_df = None
    for subtype in list_sorted:
        if subtype == subgroup:
            new_df = pd.read_csv(file)
            new_df = new_df[new_df[column] == str(subtype)]

    return new_df

def get_plot_main_group(file, column1):
    '''
    Creates a plot of the number of requests over time for a main group.

    Inputs:
        file: CSV file to be read, as a string
        column1: specific column to be converted to datetimes. Must
        contain dates, as a string
                ex: "Creation Date"

    Returns: plot from matplotlib.
    '''

    df = get_df(file, column1)
    (list_x, list_y) = requests_over_time(df)
    plt.plot(list_x, list_y)
    plt.show()

def get_plots_subgroup(file, column1, column2, subgroup):
    '''
    Creates a plot of the number of requests over time for a main group.

    Inputs:
        file: the CSV file to be read, as a string
        column1: specific column to be converted to datetimes. Must
        contain dates, as a string
                ex: "Creation Date"
        column 2: column: the column containing the subgroup, as a string
        subgroup: the specific subgroup to return, as a string

    Returns: plot from matplotlib

    '''
    df = get_subgroups(file, column2, subgroup)
    df[column1] = pd.to_datetime(df[column1])
    sorted = df.sort([column1])
    (list_x, list_y)= requests_over_time(sorted)
    plt.plot(list_x, list_y)
    plt.show

def get_summ_by_characteristic(file, characteristic):
    '''
    Gets counts, in a dataframe of a certain 311 request grouped by a
    certain characteristic.

    Inputs:
            file: the CSV file to be read, as a string
            characteristic: the characteristic you want to see counts by
                    ex: using "ZIP Code" for "Graffiti.csv" will
                    tell you how many Graffiti calls were made from
                    each Zip Code.

    Returns: dataframe where the first column is the characteristic and
    the second column is the count.
    '''
    df_main = pd.read_csv(file)

    sorted = df_main.groupby(characteristic).groups
    list_0 = []
    list_1 = []
    for i in sorted:
        list_0.append(i)
        list_1.append(len(sorted[i]))

    new_df = pd.Series(list_1, list_0)
    return new_df


def get_response_time(file, column1, column2):
    '''
    Computes the average request response time for a dataframe.

    Inputs:
            file: CSV file to read, as a string
            column1: Column header corresponding to request
            creation date
            column2: Column header corresponding to request
            completion date

    Returns: Average request time, as a float.
    '''

    df = get_df(file, column1)
    df[column2] = pd.to_datetime(df[column2])
    list_response_times = []
    for row in df.itertuples():
        if str(row[3]) != "NaT":
            list_response_times.append(row[3] - row[1])
    full_time = 0
    for time in list_response_times:
        full_time = full_time + time.days
    full_time_float = full_time
    avg_time = full_time_float / len(list_response_times)

    return avg_time

def get_most(file, column):
    '''
    Gets the specific value from a specific column that has the
    most requests of all the unique values in that column.

    '''
    df = pd.read_csv(file)
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

def get_counts_by_value(file, column, value):
    df = pd.read_csv(file)
    index = df.columns.get_loc(column) + 1
    count = 0
    for tup in df.itertuples():
        if tup[index] == value:
            count += 1
    return count






