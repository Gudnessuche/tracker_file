import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from decimal import Decimal, getcontext
import csv

class BitcoinTracker:
    def __init__(self):
        self.purchases = []
        self.default_price = 60000
        self.satoshis_per_bitcoin = 100_000_000

    def import_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = pd.to_datetime(row['date'], dayfirst=True)
                quantity = float(row['quantity'])
                units = row.get('units', 'Satoshi')
                if units.lower() == 'btc':
                    quantity *= self.satoshis_per_bitcoin
                price = float(row['price'])
                self.purchases.append({"qty": quantity / self.satoshis_per_bitcoin, "price": price, "date": date})

    def add_purchase(self, qty_satoshis=None, price=None, csv_file=None):
        if csv_file:
            self.import_csv(csv_file)
        else:
            qty_bitcoin = qty_satoshis / self.satoshis_per_bitcoin
            if price is None:
                print("Fetching current Bitcoin price...")
                try:
                    price = yf.Ticker("BTC-USD").info["regularMarketPrice"]
                except Exception:
                    price = self.default_price
                date = pd.Timestamp.now()
            else:
                date = input("Enter date of purchase (dd-mm-yyyy): ")
                date = pd.to_datetime(date, dayfirst=True)
            
            self.purchases.append({"qty": qty_bitcoin, "price": price, "date": date})

    def calculate_stats(self):
        if not self.purchases:
            return "No purchases added yet."
        
        df = pd.DataFrame(self.purchases)
        df["total_satoshis_price"] = df["qty"] * self.satoshis_per_bitcoin * df["price"]
        total_bitcoin_purchased = sum(Decimal(purchase["qty"]) for purchase in self.purchases)
        total_price = sum(df["total_satoshis_price"])
        
        if len(df) == 1:
            getcontext().prec = 20
            total_price = round(float(total_price / self.satoshis_per_bitcoin), 2)
            total_bitcoin_purchased = round(float(total_bitcoin_purchased), 8)
            return {
                "avg_buy_price": df["price"].mean(),
                "total_price": total_price,
                "total_bitcoin_purchased": total_bitcoin_purchased,
                "yearly_averages": "Not enough data for yearly averages."
            }
        
        df.set_index("date", inplace=True)
        getcontext().prec = 20
        total_price = round(float(total_price / self.satoshis_per_bitcoin), 2)
        total_bitcoin_purchased = round(float(total_bitcoin_purchased), 8)
        return {
            "avg_buy_price": df["price"].mean(),
            "total_price": total_price,
            "total_bitcoin_purchased": total_bitcoin_purchased,
            "yearly_averages": df.resample("YE")["price"].mean(),
        }

    def plot_charts(self):
        if not self.purchases:
            return "No purchases added yet."
        
        df = pd.DataFrame(self.purchases)
        df["total"] = df["qty"] * df["price"]
        df.set_index("date", inplace=True)
        
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(df["price"])
        plt.title("Bitcoin Price Over Time")
        
        plt.subplot(1, 2, 2)
        plt.plot(df["total"])
        plt.title("Total Value Over Time")
        plt.show()

tracker = BitcoinTracker()

while True:
    print("\n1. Add Purchase")
    print("2. View Stats")
    print("3. View Charts")
    print("4. Exit")
    choice = input("Choose an option: ")
    
    if choice == "1":
        csv_file = input("Enter CSV file (optional): ")
        if csv_file:
            tracker.add_purchase(csv_file=csv_file)
        else:
            qty_satoshis = float(input("Enter quantity in Satoshis: "))
            price = input("Enter price (optional): ")
            if price:
                price = float(price)
            else:
                price = None
            tracker.add_purchase(qty_satoshis, price)
    elif choice == "2":
        stats = tracker.calculate_stats()
        print(stats)
    elif choice == "3":
        tracker.plot_charts()
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")
