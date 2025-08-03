import sqlite3

def initialize_database():
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    quantity INTEGER NOT NULL,
    unit TEXT,
    expiry_data TEXT
    )
    """)

    connection.commit()
    connection.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()




    for row in tree.get_children():
            tree.delete(row)
    load_inventory_data()

    def load_inventory_data():
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM food_items")
        rows=cursor.fetchall()
        connection.close()

        for row in rows: 
            tree.insert("", "end", values=row)
            remove_button = tk.Button(inventory_window, text="Remove", commad=lambda item_id=row[0]: remove_food_item(item_id))
            inventory_window.create_window(5, tree.bbox(row), window=remove_button)

    load_inventory_data()



    def check_low_stock():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT name, quantity, unit FROM food_items WHERE quantity < 5
    """)
    low_stock_items = cursor.fetchall()
    connection.close()

    if low_stock_items:
        alert_message = "Low Stock Items: \n"
        for item in low_stock_items:
            alert_message += f"- {item[0]}: {item[1]} {item[2]}\n"
        messagebox.showwarning("Low Stock Alert", alert_message)
    else:
        messagebox.showinfo("Low Stock Alert", "All items are sufficiently stocked!")


def remove_food_item():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select an item to remove.")
            return

        item_id = tree.item(selected_item)["values"][0]

        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("DELETE FROM food_items WHERE id = ?", (item_id,))
        connection.commit()
        connection.close()

        tree.delete(selected_item)
        messagebox.showinfo("Success", "Food item removed successfully!")
    
    remove_button = tk.Button(inventory_window, text="Remove Selected Item", command=remove_food_item)
    remove_button.pack(pady=10)