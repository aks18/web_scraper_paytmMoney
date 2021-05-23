import pandas as pd
import numpy as np
import pickle as pkl


pkl_loc = 'data/extracted_dict.pkl'


def get_stocks_dict(pklloc, dump=False):
    with open(pklloc, 'rb') as f:
        pkl_data = pkl.load(f)
        f.close()

    funds = list(pkl_data.keys())
    stocksdict = {}

    for idx in range(len(funds)):
        fund_companies_list = pkl_data[funds[idx]]['companies']['list']
        for idx_2 in range(len(fund_companies_list)):
            company_name = str(fund_companies_list[idx_2]['name'])
            if company_name in stocksdict:
                stocksdict[company_name]['holdings'] += fund_companies_list[idx_2]['value']
                stocksdict[company_name]['mfs'].append(funds[idx])
                stocksdict[company_name]['mfs_ranks'].append(pkl_data[funds[idx]]['rank'])
            else:
                stocksdict[company_name] = {'holdings': fund_companies_list[idx_2]['value'],
                                             'mfs': [funds[idx]],
                                             'mfs_ranks': [pkl_data[funds[idx]]['rank']]}
    if dump:
        with open('data/stocks_dict.pkl', 'wb') as f:
            pkl.dump(stocksdict, f)
            f.close()

    return stocksdict


def get_stocks_df(stocksdict, write=False):
    df = pd.DataFrame(columns=['stock_name', 'net_holdings', 'n_mfs', 'mfs', 'mfs_ranks'])
    stocks_list = list(stocksdict)
    for idx in range(len(stocks_list)):
        df.loc[df.shape[0]] = [stocks_list[idx], stocksdict[stocks_list[idx]]['holdings'],
                               len(stocksdict[stocks_list[idx]]['mfs']), str(stocksdict[stocks_list[idx]]['mfs'])[1:-1],
                               str(stocksdict[stocks_list[idx]]['mfs_ranks'])[1:-1]]
    if write:
        df.to_csv('data/stocks_summary.csv', index=False)
    return df


stocks_dict = get_stocks_dict(pkl_loc, dump=False)
df = get_stocks_df(stocks_dict, write=True)

print(df.shape)
