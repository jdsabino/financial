from source import Source
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries


class AlphaVantage(Source):

    def __init__(self, api_key = ''):

        super().__init__("Alpha Vantage")

        if api_key == '':
            print("Can't do anything without a valid API key!")

        self.api_key = api_key

        try:
            self.fd = FundamentalData(self.api_key)
            self.ts = TimeSeries(self.api_key)
        except Exception as ee:
            print(ee)


    def set_source(api_key):
        self.fd = FundamentalData(self.api_key)
        self.ts = TimeSeries(self.api_key)

    
        
        
