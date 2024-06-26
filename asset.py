import yfinance as yf
import sys
import os

sys.path.append(os.getcwd() + "/source")

class Asset:

    
    def __init__(self, symbol, name, source=None):

        #--- Basic info
        self.symbol = symbol
        self.name = name


        self.set_source(source)#yf.Ticker(symbol) # TODO: Handle errors
        self.market_cap = None # Market capitalization or total value
        # self.asset_type = self.source.info['quoteType']
        self.short_name = name
        # self.long_name  = self.source.info['longName']

        
        # Creates a unique asset ID based on creation date
        from datetime import datetime as dt

        uniqueID = str(dt.today())
        for sym in [' ', '-', ':', '.']:
            uniqueID = uniqueID.replace(sym, '')
        self.ID = uniqueID

        

        #--- Transaction info
        self.buy_price  = None
        self.sell_price = None
        self.quantity   = None
        self.current_price = None

    def set_source(self, source=None):

        from sources import source_list
        print("Source is" + str(source))
        if source is None:
            return NotImplemented
        else:
            self.source = source_list[source]

        self.source.set_ticker(self.symbol)
    
    def set_market_cap(self):
        set_func = mkt_cap_funcs[self.source]

        self.market_cap = set_func()
        raise NotImplementedError

    def set_long_name(self):
        # Method to update general information about the asset
        raise NotImplementedError

    def set_asset_type(self):
        # Method to update general information about the asset
        raise NotImplementedError

    def update_info(self):
        # Method to update general information about the asset
        raise NotImplementedError("Subclasses must implement this method")

    def display_info(self):
        # Method to display general information about the asset
        print(f"Symbol: {self.symbol}")
        print(f"Name: {self.name}")
        print(f"Market Cap: {self.market_cap}")
