import yfinance as yf
# from alpha_vantage.fundamentaldata import FundamentalData
# from alpha_vantage.timeseries import TimeSeries
# from alpha_vantage_functions import *
from yfinance_functions import *
from wacc_list import wacc
from asset import Asset
import yfinance as yf

API_KEY = '888C8PL34SZMZSLP';

class Company(Asset):
    

    def __init__(self, symbol, name, source='YFinance'):

        super().__init__(symbol, name)
        
        self.asset_type = 'Stock'
        

        self.sector = self.source.info['sector']
        self.industry = self.source.info['industry']
        self.country =  self.source.info['country']
        self.current_price = self.source.fast_info['lastPrice']
        self.earnings_per_share = None
        self.dividend_yield = None
        self.beta = None
        
        # #--- Quantities of interest
        # self.revenue = self.get_revenue(self.info_source)
        # self.cash_flow = 0#self.get_cash_flow(self.info_source)
        # self.net_income = self.get_net_income(self.info_source)        
        # self.free_cash_flow = self.get_cash_flow(self.info_source)
        # self.total_shares = -1 # TODO # int(self.get_overview(self.info_source, field='SharesOutstanding'))

        # try:
        #     self.wacc = wacc[self.symbol]
        # except:
        #     print("Couldn't find company in the WACC list. Assigning default value... (6%)")
        #     self.wacc = 0.06



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

    def stock_price(self, start=None, end=None):
        """
        Returns the stock information (Open, High, Low, Close)
        between start to end date.

        When start and end are both None, returns the most recent stock value.
        When only end is None, returns the stock price for start date (if available).
        When only start is None, returns the stock price since data is available until 'end' date.
        

        Parameters
        ----------
        start: String
            start date in the format 'yyyy-mm-dd'
        end: String
            end date in the format 'yyyy-mm-dd'

        Returns
        ----------
        prices: pandas.core.series.Series
            The list of stock information in time   
        """        


        if start == None and end == None:
            print('Returning last price')
            hist = self.source.history()
            price = hist['Close'].iloc[-1]
            return price

        if start == None and end != None:
            prices = self.source.history(start='1900-01-01', end = end)
            return prices


        if end == None:
            import datetime as dt
            
            date_start = dt.datetime.strptime(start, '%Y-%m-%d')
            date_end   = date_start + dt.timedelta(days=1) # Add one day to the start date

            date_start = dt.datetime.strftime(date_start, '%Y-%m-%d') # Convert to string
            date_end   = dt.datetime.strftime(date_end, '%Y-%m-%d')
            
            prices = self.source.history(start = date_start, end = date_end)

            return prices['Close']
        else:
            prices = self.source.history(start = start, end = end)

            return prices





