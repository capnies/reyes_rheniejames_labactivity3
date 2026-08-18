#DISCLAIMER:
#Some parts of this code is assisted using AI, specifically, the importing of the data from JSON file.
#The rest of the code, logic and data storing logic is done by me.
import json
import os

class InventoryItem:
    def __init__(self, item_id, name, price, quantity=0):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_stock(self, amount):
        if amount > 0:
            self.quantity += amount
            return True
        return False

    def remove_stock(self, amount):
        if 0 < amount <= self.quantity:
            self.quantity -= amount
            return True
        return False

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["item_id"], data["name"], data["price"], data["quantity"])

class InventoryManager:
    def __init__(self, data_file="inventory_data.json"):
        self.inventory = {}
        self.data_file = data_file
        self.load_data() # Automatically loads past data if the JSON exists

    def register_item(self, item):
        if item.item_id in self.inventory:
            print(f"[Error] Item ID {item.item_id} already exists.")
        else:
            self.inventory[item.item_id] = item
            self.save_data()
            print(f"[Success] Registered: {item.name}")

    def process_restock(self, item_id, amount):
        if item_id in self.inventory:
            if self.inventory[item_id].add_stock(amount):
                self.save_data()
                print(f"[Success] Restocked {amount} units of {self.inventory[item_id].name}. New Total: {self.inventory[item_id].quantity}")
            else:
                print("[Error] Invalid restock amount.")
        else:
            print(f"[Error] Item {item_id} not found.")

    def process_sale(self, item_id, amount):
        if item_id in self.inventory:
            if self.inventory[item_id].remove_stock(amount):
                self.save_data()
                print(f"[Success] Sold {amount} units of {self.inventory[item_id].name}. Remaining: {self.inventory[item_id].quantity}")
            else:
                print(f"[Error] Not enough stock for {self.inventory[item_id].name}. Current stock: {self.inventory[item_id].quantity}")
        else:
            print(f"[Error] Item {item_id} not found.")

    def save_data(self):
        with open(self.data_file, "w") as f:
            data_to_save = {item_id: item.to_dict() for item_id, item in self.inventory.items()}
            json.dump(data_to_save, f, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                try:
                    data = json.load(f)
                    self.inventory = {item_id: InventoryItem.from_dict(item_data) for item_id, item_data in data.items()}
                except json.JSONDecodeError:
                    self.inventory = {}

#Since we are now dealing with OOP concepts, we can instead do test cases automatically to save time.
def display_menu():
    print("\n===== STORE INVENTORY SYSTEM =====")
    print("1. Register New Item")
    print("2. Restock Item")
    print("3. Sell Item")
    print("4. View All Inventory")
    print("5. Exit")

def view_inventory(manager):
    if not manager.inventory:
        print("[Info] Inventory is empty.")
        return
    print("\n--- CURRENT INVENTORY ---")
    for item in manager.inventory.values():
        print(f"ID: {item.item_id} | Name: {item.name} | Price: ${item.price:.2f} | Qty: {item.quantity}")

if __name__ == "__main__":
    print("STARTING STORE INVENTORY SYSTEM")
    manager = InventoryManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            item_id = input("Enter Item ID: ").strip()
            name = input("Enter Item Name: ").strip()
            try:
                price = float(input("Enter Price: ").strip())
                quantity = int(input("Enter Initial Quantity: ").strip())
                new_item = InventoryItem(item_id, name, price, quantity)
                manager.register_item(new_item)
            except ValueError:
                print("[Error] Price and quantity must be valid numbers.")

        elif choice == "2":
            item_id = input("Enter Item ID to restock: ").strip()
            try:
                amount = int(input("Enter amount to add: ").strip())
                manager.process_restock(item_id, amount)
            except ValueError:
                print("[Error] Amount must be a valid number.")

        elif choice == "3":
            item_id = input("Enter Item ID to sell: ").strip()
            try:
                amount = int(input("Enter amount to sell: ").strip())
                manager.process_sale(item_id, amount)
            except ValueError:
                print("[Error] Amount must be a valid number.")

        elif choice == "4":
            view_inventory(manager)

        elif choice == "5":
            print("Exiting Store Inventory System. Goodbye!")
            break

        else:
            print("[Error] Invalid choice. Please select 1-5.")