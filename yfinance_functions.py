import yfinance as yf
import numpy as np



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


def yf_get_income_statement_info(ticker, field):
    return NotImplementedError

def yf_get_cash_flow_info(ticker, field):
    return NotImplementedError

def yf_get_company_overview(ticker, field):
    return NotImplementedError

def yf_compute_free_cashflow(ticker, field):
    return NotImplementedError

