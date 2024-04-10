from source import Source
import justetf_scraping as js

class justETF(Source):

    def __init__(self, ticker=None):

        super().__init__("justETF")

        if ticker == None:
            print("Ticker is None. Source will not be set!")
            self.ticker = ''
        else:

            self.ticker = ticker
            
            try:
                self.chart = js.load_chart(self.ticker)
            except Exception as ee:
                print("Something went wrong with the chart!")
                print(ee)

        
            # try:
            #     self.overview = js.load_overview(self.ticker)
            # except Exception as ee:
            #     print("Something went wrong with the overview!")
            #     print(ee)                
                
        

        
    def set_ticker(self, ticker):

        self.ticker = ticker


    def set_source(self):
        try:
            self.chart = js.load_chart(self.ticker)
        except Exception as ee:
            print("Something went wrong with the chart!")
            print(ee)
            
    def set_current_price(self):
        return self.chart.iloc[]
        # try:
        #     self.overview = js.load_overview(self.ticker)
        # except Exception as ee:
        #     print("Something went wrong with the overview!")
        #     print(ee)
                
        

        
