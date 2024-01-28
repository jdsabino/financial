class Portfolio:
    
    def __init__(self, name="My Portfolio"):
        self.name = name
        self.raw_assets = []  # Raw list of assets to keep track of transactions
        self.assets = {} # Dictionary to store assets with their symbols as keys and quantities as values
        self.owners = []  # List of owners : Still to decide if ths will only be names or a prper class

    def add_asset(self, asset, quantity):
        #--- Add a new asset to the portfolio
        # First raw list
        if asset.ID not in self.assets:
            self.assets[asset.symbol] = {"asset": asset, "quantity": quantity}

        # Then the clean list
        if asset.symbol not in self.assets:
            self.assets[asset.symbol] = {"asset": asset, "quantity": quantity}
        else:
            self.assets[asset.symbol]["quantity"] += quantity

    def remove_asset(self, symbol, quantity):
        # Remove a certain quantity of an asset from the portfolio
        if symbol in self.assets:
            if self.assets[symbol]["quantity"] >= quantity:
                self.assets[symbol]["quantity"] -= quantity
                if self.assets[symbol]["quantity"] == 0:
                    del self.assets[symbol]
            else:
                print(f"Error: Attempting to sell more {symbol} than available in the portfolio.")
        else:
            print(f"Error: {symbol} not found in the portfolio.")


    def add_owner(self, owner):
        if owner not in self.owners:
            self.owners.append(owner)
        else:
            print("Owner on the list already!")

    def remove_owner(self, owner):

        if owner in self.owners:
            self.owners.remove(owner)
        else:
            print("Owner not found int owners list!")

    def calculate_portfolio_value(self):
        # Calculate the total value of the portfolio
        total_value = 0
        for asset_data in self.assets.values():
            asset = asset_data["asset"]
            quantity = asset_data["quantity"]
            total_value += asset.current_price * quantity
        return total_value

    def calculate_asset_allocation(self):
        # Calculate the percentage allocation of each asset in the portfolio
        total_value = self.calculate_portfolio_value()
        allocation = {}
        for symbol, asset_data in self.assets.items():
            asset = asset_data["asset"]
            quantity = asset_data["quantity"]
            asset_value = asset.current_price * quantity
            percentage_allocation = (asset_value / total_value) * 100
            allocation[symbol] = {"asset": asset, "percentage_allocation": percentage_allocation}
        return allocation

    def display_portfolio_summary(self):
        # Display a summary of the portfolio, including total value and asset allocation
        print(f"Portfolio: {self.name}")
        print(f"Total Portfolio Value: ${self.calculate_portfolio_value():,.2f}")
        print("\nAsset Allocation:")
        allocation = self.calculate_asset_allocation()
        for symbol, data in allocation.items():
            print(f"{symbol}: {data['percentage_allocation']:.2f}%")

    def update_asset_prices(self):
        # Update the prices of all assets in the portfolio
        for asset_data in self.assets.values():
            asset = asset_data["asset"]
            asset.update_info()  # Assuming there's an update_info method in the Asset class


    
