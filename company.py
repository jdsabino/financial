import yfinance as yf
# from alpha_vantage.fundamentaldata import FundamentalData
# from alpha_vantage.timeseries import TimeSeries
# from alpha_vantage_functions import *
from yfinance_functions import *
from wacc_list import wacc
from asset import Asset
import yfinance as yf
import datetime as dt
import pandas as pd

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
        self.dividend_yield = self.source.info['dividendYield']
        self.beta = self.source.info['beta']
        self.exDividend = pd.to_datetime( self.source.info['exDividendDate'], unit='s' )

        



    def get_overview(self):
        
        overview = self.overview_funcs[info_source](self.symbol, field)

        return overview
        
    def get_revenue(self, n_years=4):

        info_label = gross_revenue
        revenues = self.revenue_funcs[info_source](self.symbol, info_label)

        return revenues

    def get_free_cash_flows(self, n_years=4):
        '''
        Retrieves the Free Cash Flows of the last n_years years.
        n_years is set to 4 because yfinance only returns that many years back.

        TODO: Get a data source that provides more FCF history.

        Parameters
        ----------
        n_years: integer
            number of years (counting backwords from the present one) going backwards
        to retreieve free cash flows

        Returns
        ----------
        prices: pandas.core.series.Series
            The list of free cashflows
        
        '''

        fcf_idx = 0 # Works for yfinance

        fcf = self.source.get_cash_flow()
        fcf = fcf.iloc[fcf_idx]

        return fcf


    def get_net_income(self, n_years=4):

        info_label = 'netIncome'
        net_income = self.net_income_funcs[info_source](self.symbol, info_label)

        return net_income


    # The next three functions implement models that help
    # computing a stock's intrinsic value. 
    # These methods will be called by the 'intrinsic_value' method.
    # Consider creating a file with modules and its implementations.
    def dividend_discount(self):
        return NotImplementedError
    
    def residual_income(self):
        return NotImplementedError
    
    def discounted_cash_flows(self, ):
        return NotImplementedError
        

    def intrinsic_value(self, model='DCF'):

        if model == 'DCF':

            from model_functions import discounted_cash_flows_model

            nyears = 4
            discount_rate = 0.06*np.ones(nyears)
            ft_fcf = self.predict_fcf(nyears)

            int_value = discounted_cash_flows_model(ft_fcf,
                                                    discount_rate, nperiods=nyears)

            return int_value
        
        else:
            print("Model not found!")
            return -1
        
 

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

    def predict_fcf(self, nfcfs, method='LinReg'):
        '''
        Predicts the evolution of Free Cash Flows.
        It uses a specific method (by default Linear regression)
        to extrapolate future values of FCFs based on their past vales.
        
        Parameters
        ----------
        nfcfs: integer
            The number of free cash flows to predict
        method: String
            The method to predict future FCFs

        Returns
        ----------
        future_fcf: numpy.array 
            An array with the predicted values of the FCFs
        '''



        #--- LinReg method
        if method == "LinReg":
            fcf = self.get_free_cash_flows()
            fcf = fcf[::-1]
            
            tt = np.arange(fcf.size)
            
            from sklearn import linear_model
            linReg = linear_model.LinearRegression()
            linReg.fit( tt.reshape(-1, 1), fcf.values.reshape(-1,1))
            
            tt_future = np.arange(fcf.size, fcf.size + nfcfs)
            
            fcf_future = linReg.predict(tt_future.reshape(-1, 1))
            
            return fcf_future.squeeze()
        elif method == "ExpectedGrowth":
            return NotImplementedError
        else:
            return -1
    

    def update_info(self):

        self.current_price = self.stock_price()


