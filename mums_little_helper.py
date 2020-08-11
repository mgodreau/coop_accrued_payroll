import pandas as pd
from pprint import pprint

def slice_the_cack(file_name, year, month, day,):
    '''
    Takes a Timestamp.

    Returns a dictionary of the Saturday through Sunday
    daterange before the previous Thursday where the keys
    are the int month numbers and the values
    are the percentage of days in each month
    of the total days returned in all months.

    '''

    pr = pd.read_csv(file_name, encoding='unicode_escape')
    pr['Date'] = pd.to_datetime(pr['Date'])
    pr.dropna(subset=['Date'], inplace=True)
    pr['Year'] = pr.copy()['Date'].dt.year
    pr['Month'] = pr.copy()['Date'].dt.month

    paydate_entered = pd.Timestamp(year=year, month=month, day=day, freq='D')

    #Based on paydate_entered, assign either week-immediately-before or week-of to dr_a
    if paydate_entered.weekday() <= 2:
        su = paydate_entered - ((paydate_entered.weekday() + 8) * paydate_entered.freq)
        sa = paydate_entered - ((paydate_entered.weekday() + 2) * paydate_entered.freq)
    else:
        su = paydate_entered - ((paydate_entered.weekday() + 1) * paydate_entered.freq)
        sa = su + 6 * paydate_entered.freq
    #
    # if paydate_entered.weekday() <= 2:
    #     su = paydate_entered - ((paydate_entered.weekday() + 15) * paydate_entered.freq)
    #     sa = paydate_entered - ((paydate_entered.weekday() + 9) * paydate_entered.freq)
    # else:
    #     su = paydate_entered - ((paydate_entered.weekday() + 8) * paydate_entered.freq)
    #     sa = paydate_entered - ((paydate_entered.weekday() + 2) * paydate_entered.freq)


    #EX. for 10-3, we assign dr_a the week-of 9-29 thru 10-5
    dr_a = pd.date_range(start=su, end=sa, freq='D')
    su = dr_a[0]

    #paycheck_span = first arg of get_sums AND a df displaying the sat to sun of dr_a
    ps_a = pr[ (pr['Date'] >= dr_a[0]) & (pr['Date'] <= dr_a[-1]) ]

    # # dr_b as week following dr_a
    # nexsu = dr_a[-1]+1*dr_a.freq
    # nexsa = dr_a[-1]+7*dr_a.freq
    # dr_b = pd.date_range(start=nexsu, end=nexsa, freq='D')
    # ps_b = pr[ (pr['Date'] >= dr_b[0]) & (pr['Date'] <= dr_b[-1]) ]

    return ps_a, dr_a


def get_sums(paycheck_span, dr, depts):

    '''
    Takes a df and a pd.date_range
    Returns
    {'fractmo': {9: 1.0},
     'txs_by_emp': {'Adams, L': 46.32,
                'Avery, B': 25.77,
                'Bingo, Nolan': 39.650000000000006,
                'Conde, Barb': 23.59,
                'Clyde-Owens, L': 48.42,
                'Chorse, MD': 33.42,
                'Fray-Chase, Jay': 27.94,
                'Gunn, Jim': 46.88,
                'Graybranch, Linne': 57.209999999999994,
                'Hedrovin, Zed': 15.509999999999998,
                'Heart, Ray': 48.14,
                'LaRay, Jane': 43.42,
                'Lentifold, Eddie': 22.65,
                'Mattison, Ronnie G.': 38.1,
                'Peace, Jesse B.'': 31.34,
                'Peet, Angela L': 61.23,
                'Pino, Kola': 29.37,
                'Picken, James': 42.79,
                'Rich, Chiccie SR.': 35.74,
                'Ryan, Noam': 31.37,
                'Stark, Nancy B': 3.35,
                'Teddy, Aimee': 31.02,
                'Van Wilson, Len P.': 61.56,
                'Wavering, Lindsay': 41.96},
     'wgs': {'61101 · Salary & Wages-Packaging': 444.38,
         '61104 · Salary & Wages-Bakery': 2602.4799999999996,
         '61107 · Salary & Wages-Deli': 774.28,
         '61109 · Salary & Wages-Produce': 643.31,
         '61141 · Salary & Wages-Admin': 4110.31,
         '61142 · Salary & Wages-Store': 2804.06}}

    '''

    fractmo_dict = {}
    #print(f'paycheck_span: {paycheck_span}')

    #Finds the week before dr passed originally
    #This daterange represents the days that were actually worked
    #Allows fractmo_dict to iterate over appropriate week
    prevsun = dr[0] - 7 * dr.freq
    prevsat = dr[0] - 1 * dr.freq
    dr = pd.date_range(start=prevsun, end=prevsat, freq='D')

    for d in dr:
        try:
            fractmo_dict[d.month] = fractmo_dict[d.month] + 1
        except:
            fractmo_dict[d.month] = 1

    #divide each value by the sum
    total = sum(fractmo_dict.values(), 0.0)
    for key in fractmo_dict:
        fractmo_dict[key] = fractmo_dict[key] / total
        #print(f'get_sums: {fractmo_dict[key]}')

    paycheck_span = paycheck_span[ (paycheck_span['Num'] != 'Accrued Pay')]

    #Group paycheck_span by summed amount in each account for the week
    wnt = paycheck_span.groupby(['Account'], as_index=False)['Amount'].sum()

    #Dict of taxes sums per week by employee name
    vnt = paycheck_span.groupby(['Account', 'Name'], as_index=False)['Amount'].sum()
    #print(f'vnt: {vnt}')
    emp_txs = vnt[ (vnt['Account'] == '61210 · FICA Expense') | (vnt['Account'] == '61230 · NYUI Expense') ]
    #print(f'emp_txs: {emp_txs}')
    txs_by_emp = emp_txs.groupby(['Name'])['Amount'].sum().to_dict()

    #Dict of taxes sums per week, by department, according to emp-dept assignments

    # hold_tbe = {}
    # for n, t in txs_by_emp.items():
    #
    #     hold_tbe[n] = t

    dept_taxes = {}
    for d, l in depts.items():
        dept_taxes[d] = 0

        for n in l:
            dept_taxes[d] += txs_by_emp[n]

    # print(f'hold_tbe: {hold_tbe}')
    # print(f'dept_taxes: {dept_taxes}')

    txs_for_depts_emps = dept_taxes

    #Dict of only salary & wages accounts' sums
    wgs = wnt[ (wnt['Account'] != '61210 · FICA Expense') & (wnt['Account'] != '61230 · NYUI Expense') ]
    wgs_sums_dict = wgs.groupby(['Account'])['Amount'].sum().iloc[:].to_dict()

    return {'txs_for_depts_emps': txs_for_depts_emps, 'txs_by_emp': txs_by_emp, 'wgs': wgs_sums_dict, 'fractmo': fractmo_dict}


def get_tax_dept(ps):
    '''
    Returns the department and amount for the employee
    where the employee made the highest total amount for
    that month.

    file_name (str): path to csv file
    year (int): year over which to look for dept
    month (int): month over which to look for dept
    employee_name (str): name of employee to look up
    '''

    #concatenate your two paycheck_spans
    #frames = [ps, pst]
    #print(pr['Date'])

    #pr = pd.read_csv(pr, encoding='unicode_escape')
    #pr['Date'] = pd.to_datetime(pr['Date'])
    # drop null dates (just the last row)
    # drop that weird first column, the useless Clr and Balance cols too
    #pr.drop(columns=['Unnamed: 0', 'Clr', 'Balance'], inplace=True)

#     # Remove FUPAs
#     pr = pr[ (pr['Account'] != '61210 · FICA Expense') & \
#          (pr['Account'] != '61220 · FUTA Expense') & \
#          (pr['Account'] != '61230 · NYUI Expense') ]

    # create month and year cols
    #pr['Year'] = pr.copy()['Date'].dt.year
    #pr['Month'] = pr.copy()['Date'].dt.month

    # get sum totals per employee by y/m/name/dept
    ps = ps.groupby(['Name', 'Account']).sum().reset_index()

    # Sort the df based on Year, Month, Name, Account, then Amount
    # We need this for the next rank step, and will then join
    # the two results together.
    ps.sort_values(['Name', 'Amount'], inplace=True, ascending=False)

    # create the ranks for each month/name combination. Record number
    # 1 should (but isn't) the department where the employee made the
    # most money that month
    ranks = ps.groupby(by=['Name'])['Amount'].rank(method='first')
    ranks = ranks.astype('int32')
    ranks.name = 'Rank'
    #print(ranks.head(20))

    # Join the pr dataframe and the ranks dataframe back together
    wbd = pd.merge(ps, ranks, left_index=True, right_index=True)

    # create a composite join key for wbd
    wbd['cjk'] = wbd['Name'] + wbd['Rank'].astype('str')

    # the rank that corresponds to the employee's highest earning department for that month
    max_ranks = wbd.groupby(['Name'])['Rank'].max().reset_index()
    # create a composite join key for max_ranks
    max_ranks['cjk'] = max_ranks['Name'] + \
        max_ranks['Rank'].astype('str')

    # join the wbd and max_ranks table on their composite keys
    res = pd.merge(
        max_ranks,
        wbd,
        how='left',
        on='cjk',
        suffixes=('_mr', '')
    )[['Name', 'Account']]
    #print(res)
    res = res.set_index('Name')
    # fetch the user requested information from the res dataframe
    #vals =  res[ (res['Year'] == year) & (res['Month'] == month) & (res['Name'] == employees) ].values

#     out_dict = {}

#     for i, j in zip(vals[0], ['year', 'month', 'name', 'dept', 'amount']):
#         out_dict[j] = i

#     out_df = pd.DataFrame(out_dict, index=[1])

    #res_dict = res.set_index('Name').to_dict()
    return res

def get_employees_by_dept(ps, dr):

    depts = get_tax_dept(ps)
    depts = depts.reset_index()
    depts = depts.groupby(['Account'])['Name']

    ebd = {}

    for d, n in depts:
        ebd[d] = []
        #print(f'd: {d}\ntype of d: {type(d)}\n')
        #print(f'n: {n}\ntype of n: {type(n)}')

        for v in n:
            ebd[d].append(v)

    return ebd

def pieces_of_me(account_sums, depts):
    '''
    Takes dict that looks like dis.
    ratio of days in months within our one week paycheck range,
    sum of taxes by account,
    sum of salary and wages by dept.

    {'fractmo': {9: 1.0},
     'txs_by_emp': {'Adams, L': 46.32,
                'Avery, B': 25.77,
                'Bingo, Nolan': 39.650000000000006,
                'Conde, Barb': 23.59,
                'Clyde-Owens, L': 48.42,
                'Chorse, MD': 33.42,
                'Fray-Chase, Jay': 27.94,
                'Gunn, Jim': 46.88,
                'Graybranch, Linne': 57.209999999999994,
                'Hedrovin, Zed': 15.509999999999998,
                'Heart, Ray': 48.14,
                'LaRay, Jane': 43.42,
                'Lentifold, Eddie': 22.65,
                'Mattison, Ronnie G.': 38.1,
                'Peace, Jesse B.': 31.34,
                'Peet, Angela L': 61.23,
                'Pino, Kola': 29.37,
                'Picken, James': 42.79,
                'Rich, Chiccie SR.': 35.74,
                'Ryan, Noam': 31.37,
                'Stark, Nancy B': 3.35,
                'Teddy, Aimee': 31.02,
                'Van Wilson, Len P.': 61.56,
                'Wavering, Lindsay': 41.96},
     'wgs': {'61101 · Salary & Wages-Packaging': 444.38,
         '61104 · Salary & Wages-Bakery': 2602.4799999999996,
         '61107 · Salary & Wages-Deli': 774.28,
         '61109 · Salary & Wages-Produce': 643.31,
         '61141 · Salary & Wages-Admin': 4110.31,
         '61142 · Salary & Wages-Store': 2804.06}}

    Returns dict that looks like dis
    {9: {'txs_by_emp': {'Adams, L': 46.32,
                    'Avery, B': 25.77,
                    'Bingo, Nolan': 39.650000000000006,
                    'Conde, Barb': 23.59,
                    'Clyde-Owens, L': 48.42,
                    'Chorse, MD': 33.42,
                    'Fray-Chase, Jay': 27.94,
                    'Gunn, Jim': 46.88,
                    'Graybranch, Linne': 57.209999999999994,
                    'Hedrovin, Zed': 15.509999999999998,
                    'Heart, Ray': 48.14,
                    'LaRay, Jane': 43.42,
                    'Lentifold, Eddie': 2222.65,
                    'Mattison, Ronnie G.': 38.1,
                    'Peace, Jesse B.': 31.34,
                    'Peet, Angela L': 61.23,
                    'Pino, Kola': 29.37,
                    'Picken, James': 42.79,
                    'Rich, Chiccie SR.': 35.74,
                    'Ryan, Noam': 31.37,
                    'Stark, Nancy B': 3.35,
                    'Teddy, Aimee': 31.02,
                    'Van Wilson, Len P.': 61.56,
                    'Wavering, Lindsay': 41.96},
     'wgs': {'61101 · Salary & Wages-Packaging': 444.38,
             '61104 · Salary & Wages-Bakery': 2602.4799999999996,
             '61107 · Salary & Wages-Deli': 774.28,
             '61109 · Salary & Wages-Produce': 643.31,
             '61141 · Salary & Wages-Admin': 4110.31,
             '61142 · Salary & Wages-Store': 2804.06}}}
    '''


    #iterate thru each of the account dicts
    #mult'ing by the ratio of days in first month (from fractmo_dict)
    #populate a dcit or df with
#     {key = month:
#         {key = account: value = sum as ratio of number of days within key month}.
#     {key = month:
#         {key = account: value = sum as ratio of number of days within key month}.


    piece_dict = {}

    for k, v in account_sums['fractmo'].items():
        piece_dict[k] = {}

        piece_dict[k]['wgs'] = {}
        for i, j in account_sums['wgs'].items():
            # This is how we get weekly fractional wages
            piece_dict[k]['wgs'][i] = j * v

        piece_dict[k]['txs_for_depts_emps'] = {}
        for m, n in account_sums['txs_for_depts_emps'].items():
            # This is how we get weekly sums of taxes according to depts emps are assigned
            piece_dict[k]['txs_for_depts_emps'][m] = n * v

        # tbe = {}
        # for m, n in account_sums['txs_by_emp'].items():
        #     # This is how we get weekly fractional taxes by employee
        #     tbe[m] = n * v

        # This adds emps listed by dept to piece_dict for later use in sum_and_separate_by_dept
        #piece_dict[k]['depts'] = depts

        tbebd = {}
        for d, l in depts.items():
            tbebd[d] = {}
            for n in l:
                tbebd[d][n] = round(account_sums['txs_by_emp'][n] * v, 2)

        piece_dict[k]['depts'] = tbebd

        # print(f'tbebd')
        # pprint(tbebd)
        cn = {}
        for d, t in account_sums['txs_for_depts_emps'].items():
            cn[d] = (t + account_sums['wgs'][d]) * v

        piece_dict[k]['cn'] = cn

        #one col be the dept names --- one col be wages plus txs_for_depts_emps



    return piece_dict

def make_lists_for_laterframes(generic_dict):

    '''

    Returns mini dfs out of series fed
    'wages','taxes','employees' indexed by dept

    '''

#    print(f'generic_dict')
#    pprint(generic_dict)

    list_of_depts = []
    list_of_things = []

    for d, t in generic_dict.items():
        list_of_depts.append(d)
        list_of_things.append(t)

    return list_of_depts, list_of_things

def sum_and_separate_by_dept(piece_dict):
    '''
    Takes a dict that looks like dis
    {9: {'txs_by_emp': {'Adams, L': 46.32,
                    'Avery, B': 25.77,
                    'Bingo, Nolan': 39.650000000000006,
                    'Conde, Barb': 23.59,
                    'Clyde-Owens, L': 48.42,
                    'Chorse, MD': 33.42,
                    'Fray-Chase, Jay': 27.94,
                    'Gunn, Jim': 46.88,
                    'Graybranch, Linne': 57.209999999999994,
                    'Hedrovin, Zed': 15.509999999999998,
                    'Heart, Ray': 48.14,
                    'LaRay, Jane': 43.42,
                    'Lentifold, Eddie': 2222.65,
                    'Mattison, Ronnie G.': 38.1,
                    'Peace, Jesse B.': 31.34,
                    'Peet, Angela L': 61.23,
                    'Pino, Kola': 29.37,
                    'Picken, James': 42.79,
                    'Rich, Chiccie SR.': 35.74,
                    'Ryan, Noam': 31.37,
                    'Stark, Nancy B': 3.35,
                    'Teddy, Aimee': 31.02,
                    'Van Wilson, Len P.': 61.56,
                    'Wavering, Lindsay': 41.96},
     'wgs': {'61101 · Salary & Wages-Packaging': 444.38,
             '61104 · Salary & Wages-Bakery': 2602.4799999999996,
             '61107 · Salary & Wages-Deli': 774.28,
             '61109 · Salary & Wages-Produce': 643.31,
             '61141 · Salary & Wages-Admin': 4110.31,
             '61142 · Salary & Wages-Store': 2804.06}}}

    Returns a list of dicts that looks like dis
        list_of_wgs_by_dept
    [{'61101 · Salary & Wages-Packaging': 89.43714285714285,
      '61104 · Salary & Wages-Bakery': 632.0857142857143,
      '61107 · Salary & Wages-Deli': 239.61714285714282,
      '61109 · Salary & Wages-Produce': 178.0971428571428,
      '61141 · Salary & Wages-Admin': 1342.802857142857,
      '61142 · Salary & Wages-Store': 566.3571428571428}]
    list_of_wgs_by_dept
    [{'61101 · Salary & Wages-Packaging': 89.43714285714285,
      '61104 · Salary & Wages-Bakery': 632.0857142857143,
      '61107 · Salary & Wages-Deli': 239.61714285714282,
      '61109 · Salary & Wages-Produce': 178.0971428571428,
      '61141 · Salary & Wages-Admin': 1342.802857142857,
      '61142 · Salary & Wages-Store': 566.3571428571428},
     {'61101 · Salary & Wages-Packaging': 223.59285714285713,
      '61104 · Salary & Wages-Bakery': 1580.2142857142858,
      '61107 · Salary & Wages-Deli': 599.0428571428571,
      '61109 · Salary & Wages-Produce': 445.2428571428571,
      '61141 · Salary & Wages-Admin': 3357.0071428571428,
      '61142 · Salary & Wages-Store': 1415.892857142857}]
    '''
    # print(f'piece_dict')
    # pprint(piece_dict)

    dfs = []

    for m in piece_dict:

        # Create wage dataframe
        depts, wages = make_lists_for_laterframes(piece_dict[m]['wgs'])
        df = pd.DataFrame(([0] * len(depts)), columns=['Wages'], index=[depts])
        df['Wages'] = wages
        df['Month'] = [m] * df.shape[0]
        dfs.append(df)

        # Create tax dataframe
        depts, taxes = make_lists_for_laterframes(piece_dict[m]['txs_for_depts_emps'])
        tax_df = pd.DataFrame(([0] * len(depts)), columns=['Taxes'], index=[depts])
        tax_df.columns = ['Taxes']
        tax_df['Taxes'] = taxes
        dfs.append(tax_df)

        # Create employee dataframe
        depts, emps = make_lists_for_laterframes(piece_dict[m]['depts'])
        emp_df = pd.DataFrame(([0] * len(depts)), columns=['Employees'], index=[depts])
        emp_df['Employees'] = emps
        dfs.append(emp_df)

        depts, credit_new = make_lists_for_laterframes(piece_dict[m]['cn'])
        cn_df = pd.DataFrame(([0] * len(depts)), columns=['Totals_WnT'], index=[depts])
        cn_df['Totals_WnT'] = credit_new
        dfs.append(cn_df)

    return dfs

def merge_dfs(dfs):

    # This is a trial way to loop through dfs indices and build dfs_x dataframe
    # group_df = []
    # x = []
    # for i, df in enumerate(dfs):
    #     print(i)
    #     if i % 2 == 0 and i != 0:
    #         x.append(df)
    #         print(x)
    #         group_df.append(x)
    #         x = []
    #     else:
    #         x.append(df)

    dfs_x = []

    dfs_a = dfs[0].merge(dfs[1], left_index=True, right_index=True)\
        .merge(dfs[2], left_index=True, right_index=True)\
        .merge(dfs[3], left_index=True, right_index=True)

    dfs_x.append(dfs_a)
    if len(dfs) > 4:
        dfs_b = dfs[4].merge(dfs[5], left_index=True, right_index=True)\
            .merge(dfs[6], left_index=True, right_index=True)\
            .merge(dfs[7], left_index=True, right_index=True)

        dfs_x.append(dfs_b)

    #dfs_x = pd.concat([dfs_a, dfs_b])
    dfs_x = pd.concat(dfs_x)

    return dfs_x
