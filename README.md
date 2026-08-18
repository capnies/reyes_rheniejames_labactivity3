# Store Inventory Tracker - Lab Activity 3

##### DEVELOPED BY: Reyes, Rhenie James C.
**DISCLAIMER:** Some parts of this code and README.md were assisted by AI, specifically the parsing and loading of data from the JSON file, and the technical vocabolary. The core OOP logic and data structure, and flow of the README.md were designed and proposed by me.

## System Logic
This program uses Object-Oriented Programming (OOP) principles to manage store inventory through two main classes:
* **`InventoryItem`**: Represents an individual product. It stores details like ID, name, price, and quantity, and contains methods to safely add or remove stock.
* **`InventoryManager`**: Acts as the central database and controller. It registers new items, processes transactions (sales and restocks), and automatically saves or loads the data from a local `inventory_data.json` file so records aren't lost when the program closes.

## How to Run
1. Ensure Python is installed in your environment.
2. Open your terminal and navigate to the folder containing the script.
3. Execute the program by running:
   ```bash
   python reyes_rhenie_labactivity3.py
   ```
4. The terminal will automatically run three predefined test cases demonstrating the system's capabilities (instantiation, stock modification, and error validation).
5. A file named `inventory_data.json` will be automatically generated in the same folder to store the inventory records.