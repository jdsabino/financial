from asset import Asset

class ETF(Asset):
    '''
    TODO

    '''

    def __init__(self, symbol, name):

        super().__init__(symbol, name)

        self.expense_ratio = None # self.source.info['ask']
        self.current_price = None
        self.fund_type = None
        self.ytd_return = self.source.set_ytd_return()


    def update_info(self):
        self.net_asset_value = self.source.set_ytd_return()
        # self.expense_ratio = expense_ratio

    def display_info(self):
        super().display_info()
        print(f"Fund Type: {self.fund_type}")
        print(f"Net Asset Value: {self.net_asset_value}")
        print(f"Expense Ratio: {self.expense_ratio}")
