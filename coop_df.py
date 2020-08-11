import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint
from mums_little_helper import *
from reconcile import *


def coop_df(file_name, datetime_obj):
    '''
    Intermediary funct btw reconcile.py and mums_little_helper.py

    Takes file_name & date as datetime object from reconcile_month
    Runs all other functions.

    Returns dataframe to reconcile.py. Dataframe returned represents one paycheck week,
    unless it detects a week that straddles two months, in which case the dataframe
    returned will represent two paycheck weeks.

    '''

    # Parse datetime_obj into year, month, day
    y = datetime_obj.year
    m = datetime_obj.month
    d = datetime_obj.day

    #ps_a, ps_b, dr_a, dr_b = slice_the_cack('datasets/Test file MMG2.CSV', 2019, 10, 10)
    ps_a, dr_a = slice_the_cack(file_name, y, m, d)
    depts = get_employees_by_dept(ps_a, dr_a)
    account_sums = get_sums(ps_a, dr_a, depts)
    piece_dict = pieces_of_me(account_sums, depts)
    dfs = sum_and_separate_by_dept(piece_dict)
    dfs_x = merge_dfs(dfs)

    # Check number of months present in initial dfs_x here
    if dfs_x['Month'].nunique() > 1:
        # if > 1, find previous week
        prev_dt = datetime_obj - timedelta(weeks = 1)
        # if previous week's month == initial week's month, run second time with previous week
        if prev_dt.month == m:
            dfs_pw = coop_df(file_name, prev_dt)
            dfs_pw['Week'] = dfs_pw['Wages'].apply(lambda x: 'A')
            dfs_x['Week'] = dfs_x['Wages'].apply(lambda x: 'B')
            dfs_x = pd.concat([dfs_pw, dfs_x])
            print(f'This is concat with PW:\n {dfs_x}')
            return dfs_x
            #print(f'prev_dt loop: {prev_dt, list_of_dfs_x}')
        else:
            print(f'This found PW was out of month:\n {dfs_x}')
            return dfs_x
    else:
        print(f'This is returning only one initial week:\n {dfs_x}')
        return dfs_x
