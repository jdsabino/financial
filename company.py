import yfinance as yf
# from alpha_vantage.fundamentaldata import FundamentalData
# from alpha_vantage.timeseries import TimeSeries
# from alpha_vantage_functions import *
from yfinance_functions import *
from wacc_list import wacc
from asset import Asset

API_KEY = '888C8PL34SZMZSLP';

class Company(Asset):
    

    def __init__(self, symbol, name, source='YFinance'):

        super().__init__(symbol, name)
        
        self.asset_type = 'Stock'


        self.info_source = source
        
        #--- Dicionarios
        self.revenue_funcs = { 'YFinance': yf_get_income_statement_info} #, 'AlphaVantage': av_get_income_statement_info}
        
        self.cash_flow_funcs = { 'YFinance': yf_compute_free_cashflow} #, 'AlphaVantage': av_compute_free_cash_flow}
        
        self.net_income_funcs = {'YFinance': yf_get_cash_flow_info} #, 'AlphaVantage': av_get_cash_flow_info}

        self.overview_funcs = {'YFinance': yf_get_company_overview} #, 'AlphaVantage': av_get_company_overview}

        #--- Quantities of interest
        self.revenue = self.get_revenue(self.info_source)
        self.cash_flow = 0#self.get_cash_flow(self.info_source)
        self.net_income = self.get_net_income(self.info_source)        
        self.free_cash_flow = self.get_cash_flow(self.info_source)
        self.total_shares = -1 # TODO # int(self.get_overview(self.info_source, field='SharesOutstanding'))

        try:
            self.wacc = wacc[self.symbol]
        except:
            print("Couldn't find company in the WACC list. Assigning default value... (6%)")
            self.wacc = 0.06



    def get_overview(self, info_source, field='all'):
        
        overview = self.overview_funcs[info_source](self.symbol, field)

        return overview
        
    def get_revenue(self, info_source, n_years=4):

        info_label = gross_revenue
        revenues = self.revenue_funcs[info_source](self.symbol, info_label)

        return revenues

    def get_cash_flow(self, info_source, n_years=4):

        info_label = 'stuff'
        cashflow = self.cash_flow_funcs[info_source](self.symbol, info_label)

        return cashflow


    def get_net_income(self, info_source, n_years=4):

        info_label = 'netIncome'
        net_income = self.net_income_funcs[info_source](self.symbol, info_label)

        return net_income


    def intrisic_value(self, inf_growth=0.025, n_years=4):

        feeling_factor = 0.85 # Used to rescale the growth margins
        #--- Calculates growth estimative based on the last years available
        #    Note: index '0' holds the most recent value for Alpha Value
        rev_growth = np.mean( ( self.revenue[0:-1]/self.revenue[1:] - 1 ) )*feeling_factor
        ni_margin  = np.mean( ( self.net_income/self.revenue ) )*feeling_factor
        fcf_over_net_income  = np.mean( ( self.free_cash_flow/self.net_income ) )*feeling_factor
        
        #--- Arrays for future prices
        future_revenues       = np.zeros( n_years )
        future_net_income     = np.zeros( n_years )
        future_free_cash_flow = np.zeros( n_years )
        pv_future_cash_flow   = np.zeros( n_years )

        for ii in range( 0, n_years ):

            discount_factor = np.power( self.wacc + 1, ii + 1 )

            if ii == 0:
                future_revenues[ii] = ( 1 + rev_growth )*self.revenue[0]
            else:   
                future_revenues[ii] = ( 1 + rev_growth )*future_revenues[ii-1]

            future_net_income[ii] = future_revenues[ii]*ni_margin
            future_free_cash_flow[ii] = fcf_over_net_income*future_net_income[ii]
            pv_future_cash_flow[ii] = future_free_cash_flow[ii]/discount_factor
            
        terminal_value = future_free_cash_flow[-1]*( 1 + inf_growth )/( self.wacc - inf_growth )
        total_value_cf = np.sum(pv_future_cash_flow) + terminal_value/discount_factor

        int_value = total_value_cf/self.total_shares

        return int_value
 

    def dividend_income(self):
        return NotImplementedError





