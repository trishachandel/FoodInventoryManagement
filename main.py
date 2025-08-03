import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def create_table():
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS food_items")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    quantity INTEGER,
    unit TEXT,
    expiry_date TEXT,
    threshold REAL
    );
    """)

    connection.commit()
    connection.close()

create_table()

def add_food_item_window():
    add_window = tk.Toplevel()
    add_window.title("Add Food Item")
    add_window.geometry("400x500")

    tk.Label(add_window, text="Food Name: ").pack(pady=10)
    name_entry=tk.Entry(add_window)
    name_entry.pack(pady=5)

    tk.Label(add_window, text="Category: ").pack(pady=10)
    category_entry = tk.Entry(add_window)
    category_entry.pack(pady=5)

    tk.Label(add_window, text="Quantity: ").pack(pady=10)
    quantity_entry = tk.Entry(add_window)
    quantity_entry.pack(pady=5)

    tk.Label(add_window, text="Unit: ").pack(pady=10)
    unit_entry = tk.Entry(add_window)
    unit_entry.pack(pady=5)

    tk.Label(add_window, text="Expiry Date (YYYY-MM-DD): ").pack(pady=10)
    expiry_date_entry = tk.Entry(add_window)
    expiry_date_entry.pack(pady=5)

    tk.Label(add_window, text="Threshold: ").pack(pady=10)
    threshold_entry = tk.Entry(add_window)
    threshold_entry.pack(pady=5)

    def save_food_item():
        name=name_entry.get()
        category=category_entry.get()
        quantity= int(quantity_entry.get())
        unit=unit_entry.get()
        expiry_date=expiry_date_entry.get()
        threshold =threshold_entry.get()

        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("""
        INSERT INTO food_items (name, category, quantity, unit, expiry_date, threshold)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, quantity, unit, expiry_date, threshold))

        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Food item added successfully!")
        add_window.destroy()

    save_button=tk.Button(add_window, text="Save", command=save_food_item)
    save_button.pack(pady=20)


def view_inventory_window():
    inventory_window = tk.Toplevel()
    inventory_window.title("View Inventory")
    inventory_window.geometry("800x400")
    
    style= ttk.Style()
    style.configure("Treeview", background="#D3D3D3", foreground= "black", rowheight=25, fieldbackground="D3D3D3")
    style.map("Treeview", background=[("selected", "#B0E0E6")])

    tree = ttk.Treeview(inventory_window, columns=("ID","Name", "Category", "Quantity", "Unit", "Expiry Date","Threshold"), show="headings", height=15)
    for col in tree["columns"]:
        tree.heading(col, text=col, anchor=tk.W)
        tree.column(col, width=100, anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree.heading("ID", text="ID", anchor=tk.W)
    tree.heading("Name", text="Name", anchor=tk.W)
    tree.heading("Category", text="Category", anchor=tk.W)
    tree.heading("Quantity", text="Quantity", anchor=tk.W )
    tree.heading("Unit", text="Unit", anchor=tk.W)
    tree.heading("Expiry Date", text="Expiry Date", anchor=tk.W)
    tree.heading("Threshold", text="Threshold", anchor=tk.W)

    tree.column("ID", width=50, anchor=tk.W)
    tree.column("Name", width=150, anchor=tk.W)
    tree.column("Category", width=100, anchor=tk.W)
    tree.column("Quantity", width=100, anchor=tk.W)
    tree.column("Unit", width=100, anchor=tk.W)
    tree.column("Expiry Date", width=150, anchor=tk.W)
    tree.column("Threshold", width=100, anchor=tk.W)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM food_items")
    rows=cursor.fetchall()
    connection.close()
 
    for item in rows:
        tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))

    def remove_food_item():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select an item to remove.")
            return

        item_id = tree.item(selected_item[0], "values")[0]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM food_items WHERE id = ?", (item_id,))
        connection.commit()
        connection.close()

        tree.delete(selected_item[0])
        messagebox.showinfo("Success", "Food item removed successfully!")

    button_frame=tk.Frame(inventory_window)
    button_frame.pack(fill=tk.X, pady=10)

    remove_button = tk.Button(inventory_window, text="Remove Selected Item", command=remove_food_item)
    remove_button.pack(pady=10)


def show_alerts():
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()

    cursor.execute("""
    SELECT name, expiry_date FROM food_items 
    WHERE DATE(expiry_date) <= DATE('now', '+3 days')
    """)
    expiring_items = cursor.fetchall()

    cursor.execute("""
    SELECT name, quantity, threshold FROM food_items 
    WHERE quantity < threshold
    """)
    low_stock_items = cursor.fetchall()

    connection.close()

    alerts_message = ""

    if expiring_items:
        alerts_message += "⚠️ Expiring Soon:\n "
        for item in expiring_items:
            alerts_message += f"- {item[0]} (Expiry: {item[1]}\n)"
        alerts_message += "\n"
    
    if low_stock_items:
        alerts_message += "⚠️ Low Stock:\n"
        for item in low_stock_items:
            alerts_message += f"-{item[0]}: {item[1]} (Threshold: {item[2]})\n"
        
    if not alerts_message:
        alerts_message = "✅ All items are in good condition!"
    
    messagebox.showinfo("Alerts", alerts_message)

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


def main():
    create_table()
    root=tk.Tk()
    root.title("Food Inventory Management System ")
    root.geometry("800x600")

    tk.Label(root, text="Food Inventory Management", font=("Arial", 16)).pack(pady=20)

    style= ttk.Style()
    style.theme_use('classic')
    style.configure("TButton", font=("Arial", 12), padding=5)

    button_frame=tk.Frame(root)
    button_frame.pack(pady=20)

    btn_add_item = ttk.Button(button_frame, text="Add Food Item", width=20, compound=tk.LEFT, command=add_food_item_window)
    btn_view_inventory=ttk.Button(button_frame, text="View Inventory",width=20, command=view_inventory_window)
    btn_low_stock_alert = ttk.Button(button_frame, text="Low Stock Alerts",width=20, command=check_low_stock)
    btn_alerts = ttk.Button(button_frame, text="Alerts",width=20, command=show_alerts)

     
    btn_add_item.grid(row=0, column=0, padx=10, pady=5)
    btn_view_inventory.grid(row=0, column=1, padx=10, pady=5)
    btn_low_stock_alert.grid(row=1, column=0, padx=10, pady=5)
    btn_alerts.grid(row=1, column=1, padx=10, pady=5)


    root.mainloop()

if __name__ == "__main__":
    main()