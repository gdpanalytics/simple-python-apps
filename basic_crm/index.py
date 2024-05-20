import sqlite3

def setup_db():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            title TEXT,
            company TEXT,
            nation TEXT,
            city TEXT,
            address TEXT,
            zip_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_db()


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class CRMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic CRM")

        # grid layout
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # sidebar
        self.sidebar_frame = tk.Frame(root, bg="gray")
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        # main frame
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # buttons
        self.create_contact_button = tk.Button(self.sidebar_frame, text="Create Contact", command=self.show_create_contact)
        self.create_contact_button.pack(fill="x")
        self.view_contacts_button = tk.Button(self.sidebar_frame, text="View Contacts", command=self.show_view_contacts)
        self.view_contacts_button.pack(fill="x")

        # initialize pages
        self.create_contact_page = self.create_create_contact_page()
        self.view_contacts_page = self.create_view_contacts_page()

        self.show_create_contact()

    def create_create_contact_page(self):
        frame = tk.Frame(self.main_frame, bg="white")

        labels = ["Name", "Email", "Phone", "Title", "Company", "Nation", "City", "Address", "Zip Code"]
        self.entries = {}

        for idx, label in enumerate(labels):
            row, col = divmod(idx, 3)
            lbl = tk.Label(frame, text=label, bg="white")
            lbl.grid(row=row, column=col*2, padx=10, pady=5, sticky="e")
            entry = tk.Entry(frame)
            entry.grid(row=row, column=col*2+1, padx=10, pady=5, sticky="w")
            self.entries[label.lower()] = entry

        self.add_button = tk.Button(frame, text="Add Customer", command=self.add_customer)
        self.add_button.grid(row=(len(labels) + 2) // 3, column=0, columnspan=6, pady=10)

        return frame

    def create_view_contacts_page(self):
        frame = tk.Frame(self.main_frame, bg="white")

        self.contacts_tree = ttk.Treeview(frame, columns=("ID", "Name", "Email", "Phone", "Title", "Company", "Nation", "City", "Address", "Zip Code"), show="headings")
        for col in self.contacts_tree["columns"]:
            self.contacts_tree.heading(col, text=col)
            self.contacts_tree.column(col, width=100, minwidth=100)  

        # scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.contacts_tree.xview)
        self.contacts_tree.configure(xscrollcommand=hsb.set)
        hsb.pack(side='bottom', fill='x')

        self.contacts_tree.pack(fill="both", expand=True)

        # buttons for update and delete
        self.update_button = tk.Button(frame, text="Update Selected", command=self.update_contact)
        self.update_button.pack(side='left', padx=10, pady=10)
        self.delete_button = tk.Button(frame, text="Delete Selected", command=self.delete_contact)
        self.delete_button.pack(side='left', padx=10, pady=10)

        return frame

    def show_create_contact(self):
        self.view_contacts_page.pack_forget()
        self.create_contact_page.pack(fill="both", expand=True)

    def show_view_contacts(self):
        self.create_contact_page.pack_forget()
        self.view_contacts_page.pack(fill="both", expand=True)
        self.load_contacts()

    def add_customer(self):
        customer_data = {field: entry.get() for field, entry in self.entries.items()}
        
        if customer_data["name"]:
            conn = sqlite3.connect('crm.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO customers (name, email, phone, title, company, nation, city, address, zip_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(customer_data.values()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer added successfully")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Name is required")

    def load_contacts(self):
        for i in self.contacts_tree.get_children():
            self.contacts_tree.delete(i)
        
        conn = sqlite3.connect('crm.db')
        c = conn.cursor()
        c.execute("SELECT * FROM customers")
        records = c.fetchall()
        conn.close()

        for record in records:
            self.contacts_tree.insert('', 'end', values=record)

    def update_contact(self):
        selected_item = self.contacts_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No contact selected")
            return
        
        item = self.contacts_tree.item(selected_item)
        contact_id = item["values"][0]

        update_window = tk.Toplevel(self.root)
        update_window.title("Update Contact")

        labels = ["Name", "Email", "Phone", "Title", "Company", "Nation", "City", "Address", "Zip Code"]
        entries = {}

        for idx, label in enumerate(labels):
            row, col = divmod(idx, 3)
            lbl = tk.Label(update_window, text=label)
            lbl.grid(row=row, column=col*2, padx=10, pady=5, sticky="e")
            entry = tk.Entry(update_window)
            entry.grid(row=row, column=col*2+1, padx=10, pady=5, sticky="w")
            entry.insert(0, item["values"][idx+1])
            entries[label.lower()] = entry

        def save_update():
            updated_data = {field: entry.get() for field, entry in entries.items()}
            
            if updated_data["name"]:
                conn = sqlite3.connect('crm.db')
                c = conn.cursor()
                c.execute('''
                    UPDATE customers
                    SET name=?, email=?, phone=?, title=?, company=?, nation=?, city=?, address=?, zip_code=?
                    WHERE id=?
                ''', (*updated_data.values(), contact_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Customer updated successfully")
                update_window.destroy()
                self.load_contacts()
            else:
                messagebox.showerror("Error", "Name is required")

        save_button = tk.Button(update_window, text="Save", command=save_update)
        save_button.grid(row=(len(labels) + 2) // 3, column=0, columnspan=6, pady=10)

    def delete_contact(self):
        selected_item = self.contacts_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No contact selected")
            return

        item = self.contacts_tree.item(selected_item)
        contact_id = item["values"][0]

        conn = sqlite3.connect('crm.db')
        c = conn.cursor()
        c.execute('DELETE FROM customers WHERE id=?', (contact_id,))
        conn.commit()
        conn.close()

        self.contacts_tree.delete(selected_item)
        messagebox.showinfo("Success", "Customer deleted successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRMApp(root)
    root.mainloop()

