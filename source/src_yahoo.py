from source import Source
import yfinance as yf

class Yahoo(Source):

    def __init__(self):

        super().__init__("Yahoo")
        self.source = None

        
        
    def set_ticker(self, ticker):

        self.source = yf.Ticker(ticker)

        try:
            self.source.info['shortName']
        except KeyError:
            print("Symbol not found!")
            return -1
        except:
            print("Didn't work.")
            return -1


    def set_sector(self):
        return self.source.info['sector']
    
    def set_market_cap(self):

        return NotImplemented

    def set_asset_type(self):
        return self.source.info['quoteType']

    def set_long_name(self):
        return self.source.info['longName']

    def set_sector(self):
        return NotImplementedError

    def set_industry(self):
        return self.source.info['industry']

    def set_country(self):
        return self.source.info['country']

    def set_current_price(self):
        return NotImplementedError

    def set_history(self):
        return NotImplementedError
    
    def set_dividend_yield(self):
        return self.source.info['dividendYield']

    def set_beta(self):
        return self.source.info['beta']

    def set_exDividend(self):
        import pandas as pd
        return pd.to_datetime( self.source.info['exDividendDate'], unit='s' )

    def set_ytd_return(self):
        return self.source.info['ytdReturn']

    def set_expense_ratio(self):
        return self.source.info['ask']
