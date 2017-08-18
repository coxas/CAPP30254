# Alyssa Cox
# Machine Learning
# Homework 1, part 2


from hw1 import get_df
import requests
import pandas as pd
import json
from urllib.request import urlopen

Buildings_df = get_df("Buildings.csv", "DATE SERVICE REQUEST WAS RECEIVED")
Buildings_daterow = 3
Sanitation_df = get_df("Sanitation.csv", "Creation Date")
Sanitation_daterow = 1
latest_date = 20170401



def to_integer(dt_time):
    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day

def truncate_df(df, date_column_name, date_column_no, months, latest_date):
    df.sort(date_column_name, ascending=False)
    new_df = []
    for row in df.itertuples():
        date_int = to_integer(row[date_column_no])
        time_frame = latest_date - (months * 100)
        if date_int > time_frame:
            new_df.append(row[0])
    length = len(new_df)
    return df[-length:]

def get_request(url):
    '''
    Open a connection to the specified URL and if successful
    read the data.

    Inputs:
        url: must be an absolute URL

    Outputs:
        request object or None
    '''

    try:
        r = requests.get(url)
        if r.status_code == 404 or r.status_code == 403:
            r = None
    except:
        # fail on any kind of error
        r = None

    return r

def get_loc(lat, long):
        FIPS_url = 'http://data.fcc.gov/api/block/find?format=json&latitude={}&longitude={}&showall=true'.format(lat,long)
        response = urlopen(FIPS_url)
        FIPS = response.read().decode("utf-8")
        FIPS = json.loads(FIPS)
        return FIPS['Block']['FIPS']

def get_locs_for_df(df):
    pop_white_list = []
    stemdegrees_list = []
    disabilities_list = []
    for row in df.itertuples():
        lat = row[21]
        long = row[22]
        loc = get_loc(lat, long)
        state = loc[0:2]
        county = loc[2:5]
        tract = loc[5:11]
        block = loc[11]
        # url = 'http://api.census.gov/data/2013/acs5?get=NAME%2CB01001_001E&for=block+group:' + block + '&in=state:'+state+'+county:'+county+'+tract:'+tract+'&key=f584b1ef67466bf282be1268df5a899b2c114192'
        population_white_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME%2CB01001_001E&for=block+group:' + block + '&in=state:'+state+'+county:'+county+'+tract:'+tract+'&key=f584b1ef67466bf282be1268df5a899b2c114192')
        stemdegrees_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME,C15010_002E&for=block+group:' + block + '&in=state:' + state + '+county:'+ county + '+tract:' + tract + '&key=0e11756a48f5a8ec01c921ac7afbbf7bed1e84e6')
        disabilities_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME,C18108_001E&for=block+group:' + block + '&in=state:' + state + '+county:'+ county + '+tract:' + tract + '&key=0e11756a48f5a8ec01c921ac7afbbf7bed1e84e6')
        population_white = population_white_request.json()[1][1]
        stemdegrees = stemdegrees_request.json()[1][1]
        disabilities = disabilities_request.json()[1][1]

        pop_white_list.append(population_white)
        stemdegrees_list.append(stemdegrees)
        disabilities_list.append(disabilities)


    new_df = pd.concat([df, pd.DataFrame(columns=list('w'), data=pop_white_list, index=df.index)], axis=1)
    new_df2 = pd.concat([new_df, pd.DataFrame(columns=list('s'), data=stemdegrees_list, index=df.index)], axis=1)
    new_df3 = pd.concat([new_df2, pd.DataFrame(columns=list('d'), data=disabilities_list, index=df.index)], axis=1)



    return new_df3

