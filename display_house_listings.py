import pandas as pd
import tkinter as tk
from tkinter import ttk

def display_house_listings(filename: str):
    """
    Display house listings from a CSV file in a GUI format.
    
    :param filename: Name of the CSV file containing house listings.
    """
    df = pd.read_csv(filename)

    # Create the main window
    root = tk.Tk()
    root.title("House Listings")
    root.geometry("800x600")  # Set the window size

    # Create a style
    style = ttk.Style()
    style.theme_use("clam")  # Use the 'clam' theme for a modern look
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="white")
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

    # Create a frame for the treeview
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a treeview widget
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings', selectmode="browse")
    tree.pack(fill=tk.BOTH, expand=True)

    # Define the column headings
    for col in df.columns:
        tree.heading(col, text=col, anchor=tk.W)
        tree.column(col, anchor=tk.W, width=100)

    # Insert the data into the treeview
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add a label for the title
    title_label = ttk.Label(root, text="House Listings", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

def main():
    filename = 'house_listings_zillow.csv'
    display_house_listings(filename)

if __name__ == "__main__":
    main()