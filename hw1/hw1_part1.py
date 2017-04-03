# Alyssa Cox
# Machine Learning
# Homework 1, part 1

import pandas as pd
import matplotlib.pyplot as plt
import math

def get_df(file, column):
    df = pd.read_csv(file)
    df[column] = pd.to_datetime(df[column])
    sorted = df.sort([column])
    return sorted

def requests_over_time(df):
    list_y = []
    total = 0
    for i in range(len(df.index)):
        total = total + 1
        list_y.append(total)

    list_x = []
    for row in df.itertuples():
        s = str(row[1])
        date = s.replace(" 00:00:00", "")
        new_date = date.replace("-", "")
        list_x.append(int(new_date))

    return(list_x, list_y)

def get_subgroups(file, column1, column2):
    df = get_df(file, column1)

    grouped = df.groupby(column2).groups
    list_sorted = []
    list_dfs = []

    for subtype in grouped.items():
        list_sorted.append(subtype[0])
    for subtype in list_sorted:
        new_df = get_df(file, column2)
        new_df = new_df[new_df[column2] == str(subtype)]
        list_dfs.append(new_df)
    return list_dfs

def get_plot_main_group(file, column1):
    df =  get_df(file, column1)
    (list_x, list_y) = requests_over_time(df)
    plt.plot(list_x, list_y)
    plt.show()

def get_plots_subgroups(file, column1, column2):
    list_dfs = get_subgroups(file, column1, column2)
    for df in list_dfs:
        (list_x, list_y)= requests_over_time(df)
        plt.plot(list_x, list_y)
        plt.show

def get_summ_by_characteristic(file, characteristic, column):
    df_main = pd.read_csv(file)

    sorted = df_main.groupby(characteristic).groups
    list_0 = []
    list_1 = []
    for i in sorted:
        list_0.append(i)
        list_1.append(len(sorted[i]))

    new_df = pd.Series(list_1, list_0)
    print(new_df)

    df_subgroups = df_main.groupby(column).groups

    dict_zips = {}

    for i in df_subgroups:
        for index in df_subgroups[i]:
            zip = (df_main.iloc[index]["ZIP Code"])
            if math.isnan(zip):
                continue
            if zip not in dict_zips:
                dict_zips[zip] = 1
            else:
                dict_zips[zip] += 1
        print((i, dict_zips))

def get_response_time(file, column1, column2):
    df = get_df(file, column1)
    df[column2] = pd.to_datetime(df[column2])
    list_response_times = []
    for row in df.itertuples():
        cd = str(row[1])
        creation_date = cd.replace(" 00:00:00", "")
        int_creation_date = creation_date.replace("-", "")
        cod = str(row[3])
        completion_date = cod.replace(" 00:00:00", "")
        int_completion_date = completion_date.replace("-", "")
        list_response_times.append(int(int_completion_date) - int(int_creation_date))
    return list_response_times


def get_most(file, column):
    df = pd.read_csv(file)
    grouped = df.groupby(column).groups
    list_most = []
    for group in grouped:
        list_most.append((len(grouped[group]), group))
    most = 0
    for item in list_most:
        if item[0] > most:
            most = item[0]
            most_tup = (item)
    return most_tup





