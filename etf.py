from asset import Asset

class ETF(Asset):
    '''
    TODO

    '''

    def __init__(self, symbol, name):

        super().__init__(symbol, name)

        self.expense_ratio = self.source.info['ask']
        self.net_asset_value = None
        self.fund_type = None
        self.ytd_return = self.source.info['ytdReturn']


    def update_info(self, net_asset_value, expense_ratio):
        self.net_asset_value = net_asset_value
        self.expense_ratio = expense_ratio

    def display_info(self):
        super().display_info()
        print(f"Fund Type: {self.fund_type}")
        print(f"Net Asset Value: {self.net_asset_value}")
        print(f"Expense Ratio: {self.expense_ratio}")
