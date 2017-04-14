# Alyssa Cox
# Machine Learning
# Homework 2

import pandas as pd
from patsy import dmatrices
import math
import numpy as np
from sklearn.linear_model import LogisticRegression


# For part 1: Read Data
def get_df(file):
    '''
    Reads a csv file into a pandas dataframe

    Inputs:
        file: CSV file to read, as a string

    Returns: A pandas data frame
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

def get_stat_summ(file, column):
    '''
    Calculates the mean, median, and mode of a specific column

    Inputs:
            file: csv to be read
            column: column must have integer data

    Returns: string detailing the values of the mean, median, and mode
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


# For Part 3: Pre-Process and Clean Data
def fill_values(df):
    '''
    Fills in NaN cell values with the mean from that column

    Inputs:
            df: a pandas data frame

    Returns: pandas data frame with no missing values
    '''
    dict_means = {}
    headers = df.dtypes.index
    for row in df.itertuples():

            for i in range(len(row)):

                if math.isnan((row[i])):
                    col_name = headers[i - 1]
                    if col_name in dict_means:
                        mean = dict_means[col_name]
                    else:
                        mean = get_mean(df, i)
                        dict_means[col_name] = mean
                    df.set_value(row[0], col_name, mean)

    return df

# For Part 4: Generate Features, Predictors
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

def make_binary(df, column):
    '''
    Turns a categorical variable into a binary/dummy variable.

    Inputs:
            df: a pandas dataframe
            column: specific column to make binary

    Returns: dataframe where column values greater than 0 have been replaced with 1's.
    '''
    index = df.columns.get_loc(column) + 1
    for row in df.itertuples():
        if row[index] == 0:
            continue
        elif row[index] != 0:
            df.set_value(row[0], column, 1)
    return df

# Parts 5 and 6: Build and Evaluate Classifier
def log_reg(file, dis_var, num_buckets, bin_var):
    '''
    Uses patsy and sklearn to perform a logistic regression on data.

    Inputs:
            file: csv file to be read
            dis_var: variable (column name) to be discretized
            num_buckets: number of intervals for discrete variable
            bin_var: variable (column name) to be turned into dummy var

    Returns: Accuracy score for the regression
    '''
    df = get_df(file)
    filled_df = fill_values(df)
    dis_df = discretize(filled_df, dis_var, num_buckets)
    bin_df = make_binary(dis_df, bin_var)
    # I learned how to do the following from this example:
    # http://nbviewer.jupyter.org/gist/justmarkham/6d5c061ca5aee67c4316471f8c2ae976
    # Not sure if this is what we were supposed to do or not
    y, X = dmatrices('SeriousDlqin2yrs ~ RevolvingUtilizationOfUnsecuredLines + age + '
                     'DebtRatio + NumberOfOpenCreditLinesAndLoans + zipcode + '
                     'MonthlyIncome + NumberOfOpenCreditLinesAndLoans + NumberOfTimes90DaysLate',
                     bin_df, return_type="dataframe")
    y = np.ravel(y)
    model = LogisticRegression()
    model_fitted = model.fit(X, y)
    return model_fitted.score(X, y)





