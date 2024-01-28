from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
import numpy as np

API_KEY = '888C8PL34SZMZSLP';

ts = TimeSeries(API_KEY)
fd = FundamentalData(API_KEY)

#---- Fields for requests

# Indicators
gross_revenue = 'totalRevenue'
net_income    = 'netIncome'
ebit          = 'ebit' 
ebitda        = 'ebitda'
dividend_payout = 'dividendPayout'

# Relevant dates
fiscal_data   = 'fiscalDateEnding'
ex_dividend   = 'ExDividendDate'
dividend_date = 'DividendDate'

# Others
total_shares = 'SharesOutstanding'

def av_get_income_statement_info(ticker, field):

    try:
        data_raw, meta_data = fd.get_income_statement_annual(ticker)
        data = np.array(data_raw[field], dtype=float)
        
        return data
    
    except Exception as e:
        print('ERROR' + str(e))
        print('Problem with request. Check company ticker or field spelling.')

    
def av_get_cash_flow_info(ticker, field):

    try:
        data_raw, meta_data = fd.get_cash_flow_annual(ticker)
        data = np.array(data_raw[field], dtype=float)
        
        return data
    
    except Exception as e:
        print('ERROR' + str(e))
        print('Problem with request. Check company ticker or field spelling.')    


def av_get_company_overview(ticker, field='all'):

    try:
        data_raw, meta_data = fd.get_company_overview(ticker)
        #data = np.array(data_raw[field], dtype=float)
        
    except Exception as e:
        print('ERROR' + str(e))
        print('Problem with request. Check company ticker or field spelling.')

    if field == 'all':
        return data_raw
    else:
        data = np.array(data_raw[field], dtype=float)
        return data
    

def av_compute_free_cash_flow(ticker, field='bullshit'):

    op_cash_flow = np.array(av_get_cash_flow_info(ticker, 'operatingCashflow'), dtype = float)
    capex = np.array(av_get_cash_flow_info(ticker, 'capitalExpenditures'), dtype = float)

    fcf = op_cash_flow - capex

    return fcf





