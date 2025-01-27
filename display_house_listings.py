import tkinter as tk
from tkinter import ttk
import pandas as pd

def display_house_listings(filename: str):
    """
    Display house listings from a CSV file in a GUI format.
    
    :param filename: Name of the CSV file containing house listings.
    """
    df = pd.read_csv(filename)

    # Ensure the correct columns are being used
    if 'pricing' not in df.columns or 'address' not in df.columns:
        raise ValueError("CSV file must contain 'pricing' and 'address' columns")

    # Create the main window
    root = tk.Tk()
    root.title("House Listings")
    root.geometry("900x600")  # Set the window size

    # Create a style
    style = ttk.Style()
    style.theme_use("clam")  # Use the 'clam' theme for a modern look
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="white")
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
    style.map('Treeview', background=[('selected', '#4CAF50')], foreground=[('selected', 'white')])

    # Create a frame for the treeview
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Create a treeview widget
    columns = ['pricing', 'address', 'size', 'bedrooms', 'bathrooms']  # Adjust column names
    tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode="browse")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Define the column headings
    tree.heading('pricing', text='Price', anchor=tk.W)
    tree.heading('address', text='Address', anchor=tk.W)
    tree.heading('size', text='Size (sqft)', anchor=tk.W)
    tree.heading('bedrooms', text='Bedrooms', anchor=tk.W)
    tree.heading('bathrooms', text='Bathrooms', anchor=tk.W)

    for col in columns:
        tree.column(col, anchor=tk.W, width=150)

    # Insert the data into the treeview
    for index, row in df.iterrows():
        values = [row['pricing'], row['address'], row['size'], row['bedrooms'], row['bathrooms']]
        tree.insert("", tk.END, values=values)

    # Add alternating row colors
    tree.tag_configure('oddrow', background='lightblue')
    tree.tag_configure('evenrow', background='white')

    for i, item in enumerate(tree.get_children()):
        if i % 2 == 0:
            tree.item(item, tags=('evenrow',))
        else:
            tree.item(item, tags=('oddrow',))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add a label for the title
    title_label = ttk.Label(root, text="House Listings", font=("Helvetica", 20, "bold"))
    title_label.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

def main():
    filename = 'house_listings_concord_nc.csv'
    display_house_listings(filename)

if __name__ == "__main__":
    main()
