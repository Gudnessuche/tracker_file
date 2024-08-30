import csv
from datetime import datetime
from forex_python.converter import CurrencyRates

class BitcoinTracker:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.price(c_p)
        self.purchases = []
        self.load_purchases()
        self.currency_rates = CurrencyRates()

    def price(self):
        price = price = self.price()
        if not price

    def load_purchases(self):
        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['quantity'] = float(row['quantity'])
                    row['price'] = float(row['price'])
                    row['date'] = datetime.strptime(row['date'], '%Y-%m-%d' )
                    self.purchases.append(row)
        except FileNotFoundError:
            pass

    def add_purchase(self, quantity, price, date):
        purchase = {'quantity': quantity, 'price': price, 'date': datetime.strptime(date, '%Y-%m-%d')}
        self.purchases.append(purchase)
        self.save_purchases()

    def save_purchases(self):
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['quantity', 'price', 'date'])
            writer.writeheader()
            for purchase in self.purchases:
                writer.writerow({'quantity': purchase['quantity'], 'price': purchase['price'], 'date': purchase['date'].strftime('%Y-%m-%d``')})

    def total_bitcoin_purchased(self):
        return sum(purchase['quantity'] for purchase in self.purchases)

    def total_price_spent(self):
        return sum(purchase['quantity'] * purchase['price'] for purchase in self.purchases)

    def average_buy_price(self):
        total_quantity = self.total_bitcoin_purchased()
        if total_quantity == 0:
            return 0
        return self.total_price_spent() / total_quantity

    def yearly_averages(self):
        yearly_data = {}
        for purchase in self.purchases:
            year = purchase['date'].year
            if year not in yearly_data:
                yearly_data[year] = {'quantity': 0, 'total_spent': 0}
            yearly_data[year]['quantity'] += purchase['quantity']
            yearly_data[year]['total_spent'] += purchase['quantity'] * purchase['price']
        return {year: data['total_spent'] / data['quantity'] for year, data in yearly_data.items()}

    def specific_returns(self, current_price):
        total_spent = self.total_price_spent()
        total_value = self.total_bitcoin_purchased() * current_price
        return total_value - total_spent

    def convert_currency(self, amount, from_currency, to_currency):
        return self.currency_rates.convert(from_currency, to_currency, amount)

    def btc_price_in_currency(self, btc_price, currency):
        return self.convert_currency(btc_price, 'USD', currency)

# Example usage
tracker = BitcoinTracker('bitcoin_purchases.csv')
tracker.add_purchase(0.1, 30000, '2023-01-01')
tracker.add_purchase(0.2, 35000, '2023-06-01')

print("Total Bitcoin Purchased:", tracker.total_bitcoin_purchased())
print("Total Price Spent:", tracker.total_price_spent())
print("Average Buy Price:", tracker.average_buy_price())
print("Yearly Averages:", tracker.yearly_averages())
print("Specific Returns (current price $40000):", tracker.specific_returns(40000))
print("BTC Price in NGN:", tracker.btc_price_in_currency(40000, 'NGN'))
