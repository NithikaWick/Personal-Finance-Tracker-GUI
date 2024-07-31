import tkinter as tk
from tkinter import ttk, messagebox
import json


class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry('810x520')
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions("transactions.json")

    def create_widgets(self):
        # Frame for table and scrollbar
        page_Label = tk.Label(self.root, text="PERSONAL FINANCIAL TRACKER.", font=('Aptos Display', 25, 'bold'))
        page_Label.pack(padx=0, pady=10)


        # Search bar and button
        # Search button
        search_frame = ttk.Frame(self.root, border=1)
        search_frame.pack(side="top", pady=10, padx=10, anchor="w")  # Align to the left corner
        # Search bar
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.grid(row=0, column=0, padx=5)
        # Search button
        search_button = tk.Button(search_frame, text="Search",font=('Calibre', 10), command=self.search_transactions)
        search_button.grid(row=0, column=1)

        # Table frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)


        # Treeview for displaying transactions
        self.table = ttk.Treeview(self.table_frame, columns = ('no.',"Category", "Amount", "Date"), show='headings')

        self.table.column('no.', width=5, minwidth=3 )
        self.table.heading('no.', text='No.')
        self.table.heading('Category', text='Category')
        self.table.heading('Amount', text='Amount (Rs.)')
        self.table.heading('Date', text='Transaction Date')
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=7, pady=9)

        #Add some styles
        self.styles = ttk.Style()
        self.styles.configure('Treeview', rowheight=21, font=('Calibre', 9))
        self.styles.configure('Treeviwe.Heading', font='bold',background="lightgrey")
        self.table.tag_configure('oddrow',background='white')
        self.table.tag_configure('evenrow', background='lightblue')
        # self.styles.configure(self.root, background='lightgreen')

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=scrollbar.set)

        # Sorting dropdown menu
        sort_frame = tk.Frame(self.root)
        sort_frame.pack(side="bottom", pady=10, padx=10, anchor="e")
        ttk.Label(sort_frame, text="Sort by:", font=("Helvetica", 10)).grid(row=0, column=0)
        self.sort_var = tk.StringVar()
        sort_options = ttk.Combobox(sort_frame, textvariable=self.sort_var, values=["Category", "Date", "Amount"])
        sort_options.grid(row=0, column=1)
        sort_options.current(0)  # Set the default sorting option
        sort_button = ttk.Button(sort_frame, text="Sort", command=self.sort_transactions)
        sort_button.grid(row=0, column=2)


        # Close message
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        # self.root.mainloop()
    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            transactions = []
            for category, category_transactions in data.items():
                for transaction in category_transactions:
                    transactions.append({
                        "Category": category,
                        "Date": transaction["date"],
                        "Amount": transaction["amount"]
                    })
            return transactions
        except FileNotFoundError:
            return []

    def display_transactions(self, transactions):
        # Remove existing entries
        for row in self.table.get_children():
            self.table.delete(row)

        # Add transactions to the treeview
        count = 1
        for transaction in transactions:
            if count % 2 == 0:
                self.table.insert("", "end", values=(
                    (count),
                    transaction["Category"],
                    transaction["Amount"],
                    transaction["Date"]), tags=('evenrow'))
            else:
                self.table.insert("", "end", values=(
                    (count),
                    transaction["Category"],
                    transaction["Amount"],
                    transaction["Date"]), tags=('oddrow'))
            count += 1
    def search_transactions(self):
        search_item = self.search_var.get().lower()
        if not search_item:
            self.display_transactions(self.transactions)
            return

        filtered_transactions = [t for t in self.transactions if search_item in str(t).lower()]
        self.display_transactions(filtered_transactions)

    def sort_transactions(self):
        sort_column = self.sort_var.get()
        if sort_column:
            self.sort_by_column(sort_column)

    def sort_by_column(self, col):
        items = [(self.table.set(child, col), child) for child in self.table.get_children('')]
        items.sort(reverse=False)
        for index, (val, child) in enumerate(items):
            self.table.move(child, '', index)

    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()


if __name__ == "__main__":
    main()
