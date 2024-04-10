

class Source:

    
    
    def __init__(self, name):
        self.available_sources = ["Yahoo"]
        self.print_sources()
        self.name = name
        self.source = None
        self.api_key = ''
    
        
    def print_sources(self):

        print("Available sources:")

        for src in self.available_sources:
            print('-' + src)
    
        return 0

    def set_ticker(ticker):
        return NotImplemented
    
    def set_market_cap(self):

        return NotImplemented

    def set_asset_type(self):
        return NotImplemented

    def set_long_name(self):
        return NotImplemented

    def set_sector(self):
        return NotImplementedError

    def set_industry(self):
        return NotImplementedError

    def set_country(self):
        return NotImplementedError

    def set_current_price(self):
        return NotImplementedError

    def set_history(self):
        return NotImplementedError
    
    def set_dividend_yield(self):
        return NotImplementedError

    def set_beta(self):
        return NotImplementedError

    def set_exDividend(self):
        return NotImplementedError

    def set_ytd_return(self):
        return NotImplementedError

    def set_expense_ratio(self):
        return NotImplementedError

    
