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
    '''
    Turns a datetime object into an integer.

    Inputs:
            dt_time, a datetime object
    Outputs:
            int
    '''

    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day

def truncate_df(df, date_column_name, date_column_no, months, latest_date):
    '''
    Truncates a given dataframe to only include data from dates in a given timeframe.

    Inputs:
            df: the dataframe
            date_column_name: the name of the column in the dataframe that holds the dates
            date_column_no: the number of the column in the dataframe that holds the dates
            months: how many months back from the starting date the new df should include
            latest_date: starting date to calculate months back

    Outputs: dataframe
    '''

    df.sort(date_column_name, ascending=False)
    new_df = []
    for row in df.itertuples():
        date_int = to_integer(row[date_column_no])
        time_frame = latest_date - (months * 100)
        if date_int > time_frame:
            new_df.append(row[0])
    length = len(new_df)
    return df[-length:-1]

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
        # fail on error
        r = None

    return r

def get_loc(lat, long):
    '''
    Retrieves a FIPS location object for a given latitude and longitude.

    Inputs:
            lat: latitude
            long: longitude

    Outputs: string of numbers

    '''

    FIPS_url = 'http://data.fcc.gov/api/block/find?format=json&latitude={}&longitude={}&showall=true'.format(lat,long)
    response = urlopen(FIPS_url)
    FIPS = response.read().decode("utf-8")
    FIPS = json.loads(FIPS)
    return FIPS['Block']['FIPS']

def get_locs_for_df(df):
    '''
    Breaks down the FIPS location into state, county, tract, and block, and uses these to make specific API calls.
    Gather data from API calls.
    Appends new data in new columns on the original dataframe.

    Inputs:
            df: original dataframe

    Outputs:
            augmented dataframe

    '''

    # initialize lists
    pop_white_list = []
    stemdegrees_list = []
    disabilities_list = []

    count = 0

    # iterate through dataframe to get FIPS info and break it down
    for row in df.itertuples():
        lat = row[21]
        long = row[22]
        loc = get_loc(lat, long)
        state = loc[0:2]
        county = loc[2:5]
        tract = loc[5:11]
        block = loc[11]

    #make API calls
        population_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME,B02001_001E&for=block+group:' + block + '&in=state:' + state + '+county:' + county + '+tract:' + tract + '&key=f584b1ef67466bf282be1268df5a899b2c114192')
        population_white_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME,B02001_002E&for=block+group:' + block + '&in=state:'+state+'+county:'+county+'+tract:'+tract+'&key=f584b1ef67466bf282be1268df5a899b2c114192')
        stemdegrees_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME,C15010_002E&for=block+group:' + block + '&in=state:' + state + '+county:'+ county + '+tract:' + tract + '&key=f584b1ef67466bf282be1268df5a899b2c114192')
        disabilities_request = get_request('http://api.census.gov/data/2013/acs5?get=NAME,C18108_001E&for=block+group:' + block + '&in=state:' + state + '+county:'+ county + '+tract:' + tract + '&key=f584b1ef67466bf282be1268df5a899b2c114192')
        population_white = population_white_request.json()[1][1]
        stemdegrees = stemdegrees_request.json()[1][1]
        disabilities = disabilities_request.json()[1][1]
        total_pop = population_request.json()[1][1]

        pop_white = int(population_white)
        pop_stem = int(stemdegrees)
        pop_tot = int(total_pop)

        if pop_tot != 0:
            pop_white_list.append(pop_white/pop_tot)
            stemdegrees_list.append(pop_stem/pop_tot)
        else:
            pop_white_list.append(0)
            stemdegrees_list.append(0)

        disabilities_list.append(disabilities)
        count += 1
        print(count)

    new_df = pd.concat([df, pd.DataFrame(columns=list('w'), data=pop_white_list, index=df.index)], axis=1)
    new_df2 = pd.concat([new_df, pd.DataFrame(columns=list('s'), data=stemdegrees_list, index=df.index)], axis=1)
    new_df3 = pd.concat([new_df2, pd.DataFrame(columns=list('d'), data=disabilities_list, index=df.index)], axis=1)

    return new_df3

