import pandas as pd
from datetime import datetime
import os

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, license_plate):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate


class TollBooth:
    def __init__(self, booth_id, location, toll_rates):
        self.booth_id = booth_id
        self.location = location
        self.toll_rates = toll_rates


class TollTransaction:
    def __init__(self, transaction_id, vehicle_id, booth_id, amount, timestamp):
        self.transaction_id = transaction_id
        self.vehicle_id = vehicle_id
        self.booth_id = booth_id
        self.amount = amount
        self.timestamp = timestamp


class TollManagementSystem:
    def __init__(self):
        self.vehicles = []
        self.toll_booths = []
        self.transactions = []
        self.load_data()

    def load_data(self):
        # Create Excel files if they don't exist
        if not os.path.exists("vehicles.xlsx"):
            self.create_excel("vehicles.xlsx", ["vehicle_id", "vehicle_type", "license_plate"])
        if not os.path.exists("toll_booths.xlsx"):
            self.create_excel("toll_booths.xlsx", ["booth_id", "location", "toll_rates"])
        if not os.path.exists("transactions.xlsx"):
            self.create_excel("transactions.xlsx", ["transaction_id", "vehicle_id", "booth_id", "amount", "timestamp"])

        # Load data from Excel files
        self.vehicles = pd.read_excel("vehicles.xlsx").to_dict(orient="records")
        self.toll_booths = pd.read_excel("toll_booths.xlsx").to_dict(orient="records")
        self.transactions = pd.read_excel("transactions.xlsx").to_dict(orient="records")
        print("Data loaded successfully.")

    def create_excel(self, filename, columns):
        df = pd.DataFrame(columns=columns)
        df.to_excel(filename, index=False)
        print(f"Created {filename} with columns {columns}")

    def save_data(self):
        pd.DataFrame(self.vehicles).to_excel("vehicles.xlsx", index=False)
        pd.DataFrame(self.toll_booths).to_excel("toll_booths.xlsx", index=False)
        pd.DataFrame(self.transactions).to_excel("transactions.xlsx", index=False)
        print("Data saved successfully.")

    def add_vehicle(self, vehicle_id, vehicle_type, license_plate):
        self.vehicles.append({"vehicle_id": vehicle_id, "vehicle_type": vehicle_type, "license_plate": license_plate})
        print("Vehicle added successfully.")

    def add_toll_booth(self, booth_id, location, toll_rates):
        self.toll_booths.append({"booth_id": booth_id, "location": location, "toll_rates": toll_rates})
        print("Toll booth added successfully.")

    def record_transaction(self, transaction_id, vehicle_id, booth_id):
        vehicle = next((v for v in self.vehicles if v["vehicle_id"] == vehicle_id), None)
        toll_booth = next((tb for tb in self.toll_booths if tb["booth_id"] == booth_id), None)

        if not vehicle or not toll_booth:
            print("Invalid vehicle ID or booth ID.")
            return

        toll_rate = toll_booth["toll_rates"].get(vehicle["vehicle_type"], 0)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "transaction_id": transaction_id,
            "vehicle_id": vehicle_id,
            "booth_id": booth_id,
            "amount": toll_rate,
            "timestamp": timestamp
        })
        print(f"Transaction recorded successfully! Toll Amount: ${toll_rate:.2f}")

    def view_transactions(self):
        if not self.transactions:
            print("No transactions to display.")
            return

        print("\nTransaction History:")
        for t in self.transactions:
            print(
                f"ID: {t['transaction_id']}, Vehicle ID: {t['vehicle_id']}, Booth ID: {t['booth_id']}, "
                f"Amount: ${t['amount']}, Timestamp: {t['timestamp']}"
            )


def menu():
    system = TollManagementSystem()

    while True:
        print("\n=== Toll Management System ===")
        print("1. Add Vehicle")
        print("2. Add Toll Booth")
        print("3. Record Transaction")
        print("4. View Transactions")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_id = input("Enter Vehicle ID: ")
            vehicle_type = input("Enter Vehicle Type (Car/Truck/Motorcycle): ")
            license_plate = input("Enter License Plate: ")
            system.add_vehicle(vehicle_id, vehicle_type, license_plate)

        elif choice == "2":
            booth_id = input("Enter Booth ID: ")
            location = input("Enter Location: ")
            toll_rates_input = input("Enter Toll Rates (e.g., {'Car': 5, 'Truck': 10, 'Motorcycle': 3}): ")
            toll_rates = eval(toll_rates_input)
            system.add_toll_booth(booth_id, location, toll_rates)

        elif choice == "3":
            transaction_id = input("Enter Transaction ID: ")
            vehicle_id = input("Enter Vehicle ID: ")
            booth_id = input("Enter Booth ID: ")
            system.record_transaction(transaction_id, vehicle_id, booth_id)

        elif choice == "4":
            system.view_transactions()

        elif choice == "5":
            system.save_data()
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
