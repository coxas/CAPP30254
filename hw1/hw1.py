# Alyssa Cox
# Machine Learning
# Homework 1

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
    # plt.plot(list_x, list_y)
    # plt.show()

def get_subgroups(file, column1, column2):
    df = get_df(file, column1)
    # num_total = num_cum_total(file, column)
    #
    grouped = df.groupby(column2).groups
    list_sorted = []
    list_dfs = []
    for subtype in grouped.items():
        list_sorted.append(subtype[0])
    for subtype in list_sorted:
        new_df = get_df(file, column2)
        new_df = new_df[new_df[column2] == str(subtype)]
        list_dfs.append(new_df)
        # requests_over_time(new_df)
    return list_dfs
        # for row in new_df.itertuples():
        #     if row["What Type of Surface is the Graffiti On?"] != str(subtype):
        #     new_df = new_df.drop

    #total_plot = df.plot(x="")


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
    #print(df_main.ix[0])

    sorted = df_main.groupby(characteristic).groups
    list_0 = []
    list_1 = []
    for i in sorted:
        list_0.append(i)
        list_1.append(len(sorted[i]))
    #     list_1.append(len(i[1]))
    new_df = pd.Series(list_1, list_0)
    print(new_df)

    df_subgroups = df_main.groupby(column).groups
    # for i in df_subgroups:
    #     print(df_subgroups[i][0])
    #
    #
    # return df_subgroups
    # # list_2 = []
    # # list_3 = []
    list_indices = []
    dict_zips = {}
    # # for i in df_subgroups:
    # #     # if df_main.loc(column) != i:
    # #         for  in df_main:
    # #             return row
    #         #df_sub = df_main(df_main[column] == i)
    #         #return df_sub
    for i in df_subgroups:
        #return df_subgroups[i]
        for index in df_subgroups[i]:
            zip = (df_main.iloc[index]["ZIP Code"])
            if math.isnan(zip):
                continue
            if zip not in dict_zips:
                dict_zips[zip] = 1
            else:
                dict_zips[zip] += 1
        print((i, dict_zips))
    #
    #         if df_main.iloc


        # list_indices.append(df_subgroups.iloc[i][0:])
        # return list_indices
        #return df_main.iloc[[0]]
        # for index in list_indices:
        #     #return df_main[index]
        # #list_2.append(df_main.ix[i])
        # return(list_indices)







    #list_chars = []
    # for row in df_main.itertuples():
    #     for i in row:
    #         print(i)
    #         if row[i][2] == characteristic:
    #             return column
    #     if row not in list_chars:
    #         list_chars.append(characteristic)
    # return list_chars







