class Asset:

    def __init__(self, symbol):



        #--- Basic info
        self.symbol = symbol
        self.name = ''
        self.market_cap = None # Market capitalization or total value
        self.asset_type = ''

        # Creates a unique asset ID based on creation date
        import datetime.datetime as dt

        uniqueID = str(dt.today())
        for sym in [' ', '-', ':', '.']:
            uniqueID = uniqueID.replace(sym, '')
        self.ID = uniqueID

        

        #--- Transaction info
        self.buy_price  = None
        self.sell_price = None
        self.quantity   = None
        self.current_price = None

    def update_info(self):
        # Method to update general information about the asset
        raise NotImplementedError("Subclasses must implement this method")

    def display_info(self):
        # Method to display general information about the asset
        print(f"Symbol: {self.symbol}")
        print(f"Name: {self.name}")
        print(f"Market Cap: {self.market_cap}")
