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
if __name__ == "__main__":
    print("STARTING STORE INVENTORY SYSTEM")
    manager = InventoryManager()

    print("\n--- TEST CASE 1: Adding New Items ---")
    item1 = InventoryItem("ITM001", "Mechanical Keyboard", 120.00, 10)
    item2 = InventoryItem("ITM002", "Wireless Mouse", 45.00, 25)
    manager.register_item(item1)
    manager.register_item(item2)

    print("\n--- TEST CASE 2: Modifying Stock ---")
    manager.process_restock("ITM001", 5)
    manager.process_sale("ITM002", 2)

    print("\n--- TEST CASE 3: Error Handling & Validation ---")
    manager.process_sale("ITM001", 50)
    manager.register_item(item1)