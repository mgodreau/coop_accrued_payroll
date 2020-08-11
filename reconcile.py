import sys, os
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint
from os import path, listdir
from mums_little_helper import *
from coop_df import *

pd.set_option('max_colwidth', 400)

def reconcile_month(file_name, paydate):
    '''
    Takes two strings as args. file_name, paydate 'M-D-YYYY' or 'MM-DD-YYYY'
    Returns final dataframe dfs_x
    '''
    # Find path to file, assign file_name, and print name of file we're running
    path = os.getcwd()
    file_name = os.path.join(path, file_name)
    print(f'file_name: {file_name}')

    # Create datetime object YYYY-MM-DD from user input
    our_dt = datetime.strptime(paydate, '%m-%d-%Y').date()

    # FUNCTION CALL to all other functs via coop_df
    # Return compiled dataframe at html
    final_df = coop_df(file_name, our_dt)
    try:
        final_df.to_html(
            'file.html',
            columns=['Month', 'Week', 'Totals_WnT', 'Wages', 'Taxes', 'Employees'],
            justify='left',
            float_format='$%.2f')
    except KeyError:
        final_df.to_html(
            'file.html',
            columns=['Month', 'Totals_WnT', 'Wages', 'Taxes', 'Employees'],
            justify='left',
            float_format='$%.2f')

    print(f'final_df output: {final_df}')

if __name__ == '__main__':
    reconcile_month(sys.argv[1], sys.argv[2])
