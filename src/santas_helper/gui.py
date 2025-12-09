"""GUI interface for Santa's Helper using tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
from .models import Person, WishlistItem
from .storage import StorageManager
from .prisjakt import PrisjaktClient


class SantasHelperGUI:
    """GUI application for managing wishlists."""
    
    def __init__(self, root):
        """Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Santa's Helper - Wishlist Manager")
        self.root.geometry("800x600")
        
        self.storage = StorageManager()
        self.prisjakt = PrisjaktClient()
        
        self.setup_ui()
        self.refresh_people_list()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # People section
        ttk.Label(main_frame, text="People:", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # People listbox
        people_frame = ttk.Frame(main_frame)
        people_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.people_listbox = tk.Listbox(people_frame, height=10, width=25)
        self.people_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.people_listbox.bind('<<ListboxSelect>>', self.on_person_select)
        
        people_scrollbar = ttk.Scrollbar(people_frame, orient=tk.VERTICAL, command=self.people_listbox.yview)
        people_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.people_listbox.config(yscrollcommand=people_scrollbar.set)
        
        # People buttons
        people_btn_frame = ttk.Frame(main_frame)
        people_btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=(0, 10), pady=(5, 0))
        
        ttk.Button(people_btn_frame, text="Add Person", command=self.add_person_dialog).pack(
            fill=tk.X, pady=2
        )
        ttk.Button(people_btn_frame, text="Remove Person", command=self.remove_person).pack(
            fill=tk.X, pady=2
        )
        
        # Wishlist section
        wishlist_frame = ttk.Frame(main_frame)
        wishlist_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        wishlist_frame.columnconfigure(0, weight=1)
        wishlist_frame.rowconfigure(1, weight=1)
        
        ttk.Label(wishlist_frame, text="Wishlist:", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # Wishlist display
        self.wishlist_text = scrolledtext.ScrolledText(
            wishlist_frame, height=20, width=50, wrap=tk.WORD, state=tk.DISABLED
        )
        self.wishlist_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        # Wishlist buttons
        wishlist_btn_frame = ttk.Frame(wishlist_frame)
        wishlist_btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(wishlist_btn_frame, text="Add Item", command=self.add_item_dialog).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(wishlist_btn_frame, text="Remove Item", command=self.remove_item_dialog).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(wishlist_btn_frame, text="Find Prices", command=self.show_prices).pack(
            side=tk.LEFT, padx=2
        )
    
    def refresh_people_list(self):
        """Refresh the list of people."""
        self.people_listbox.delete(0, tk.END)
        people = self.storage.list_people()
        for person in people:
            self.people_listbox.insert(tk.END, person)
    
    def on_person_select(self, event):
        """Handle person selection."""
        selection = self.people_listbox.curselection()
        if not selection:
            return
        
        person_name = self.people_listbox.get(selection[0])
        self.display_wishlist(person_name)
    
    def display_wishlist(self, person_name: str):
        """Display a person's wishlist.
        
        Args:
            person_name: Name of the person
        """
        person = self.storage.load_person(person_name)
        if not person:
            return
        
        self.wishlist_text.config(state=tk.NORMAL)
        self.wishlist_text.delete(1.0, tk.END)
        
        if not person.wishlist:
            self.wishlist_text.insert(tk.END, f"{person_name} has no items in their wishlist yet.")
        else:
            self.wishlist_text.insert(tk.END, f"{person_name}'s Wishlist\n")
            self.wishlist_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for item in sorted(person.wishlist, key=lambda x: x.priority):
                self.wishlist_text.insert(tk.END, f"[Priority {item.priority}] {item.name}\n")
                if item.description:
                    self.wishlist_text.insert(tk.END, f"  Description: {item.description}\n")
                self.wishlist_text.insert(tk.END, "\n")
        
        self.wishlist_text.config(state=tk.DISABLED)
    
    def add_person_dialog(self):
        """Show dialog to add a new person."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Person")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Person's Name:").pack(pady=(10, 5))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid Input", "Please enter a name.")
                return
            
            if self.storage.load_person(name):
                messagebox.showwarning("Duplicate", f"Person '{name}' already exists!")
                return
            
            person = Person(name=name)
            self.storage.save_person(person)
            self.refresh_people_list()
            dialog.destroy()
            messagebox.showinfo("Success", f"Added person: {name}")
        
        ttk.Button(dialog, text="Add", command=save).pack(pady=10)
        
        dialog.bind('<Return>', lambda e: save())
    
    def remove_person(self):
        """Remove the selected person."""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person to remove.")
            return
        
        person_name = self.people_listbox.get(selection[0])
        
        if messagebox.askyesno("Confirm", f"Remove {person_name}'s wishlist?"):
            self.storage.delete_person(person_name)
            self.refresh_people_list()
            self.wishlist_text.config(state=tk.NORMAL)
            self.wishlist_text.delete(1.0, tk.END)
            self.wishlist_text.config(state=tk.DISABLED)
    
    def add_item_dialog(self):
        """Show dialog to add a new item."""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person first.")
            return
        
        person_name = self.people_listbox.get(selection[0])
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add Item to {person_name}'s Wishlist")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Item Name:").pack(pady=(10, 5))
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        ttk.Label(dialog, text="Description (optional):").pack(pady=(10, 5))
        desc_entry = ttk.Entry(dialog, width=40)
        desc_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Priority (1=highest):").pack(pady=(10, 5))
        priority_entry = ttk.Entry(dialog, width=10)
        priority_entry.insert(0, "1")
        priority_entry.pack(pady=5)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid Input", "Please enter an item name.")
                return
            
            description = desc_entry.get().strip()
            try:
                priority = int(priority_entry.get())
            except ValueError:
                messagebox.showwarning("Invalid Input", "Priority must be a number.")
                return
            
            person = self.storage.load_person(person_name)
            item = WishlistItem(name=name, description=description, priority=priority)
            person.add_item(item)
            self.storage.save_person(person)
            
            self.display_wishlist(person_name)
            dialog.destroy()
            messagebox.showinfo("Success", f"Added '{name}' to {person_name}'s wishlist")
        
        ttk.Button(dialog, text="Add Item", command=save).pack(pady=10)
        
        dialog.bind('<Return>', lambda e: save())
    
    def remove_item_dialog(self):
        """Show dialog to remove an item."""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person first.")
            return
        
        person_name = self.people_listbox.get(selection[0])
        person = self.storage.load_person(person_name)
        
        if not person.wishlist:
            messagebox.showinfo("Empty List", f"{person_name} has no items to remove.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Remove Item from {person_name}'s Wishlist")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select item to remove:").pack(pady=(10, 5))
        
        items_listbox = tk.Listbox(dialog, height=10)
        items_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for item in person.wishlist:
            items_listbox.insert(tk.END, item.name)
        
        def remove():
            item_selection = items_listbox.curselection()
            if not item_selection:
                messagebox.showwarning("No Selection", "Please select an item to remove.")
                return
            
            item_name = items_listbox.get(item_selection[0])
            person.remove_item(item_name)
            self.storage.save_person(person)
            
            self.display_wishlist(person_name)
            dialog.destroy()
            messagebox.showinfo("Success", f"Removed '{item_name}' from {person_name}'s wishlist")
        
        ttk.Button(dialog, text="Remove", command=remove).pack(pady=5)
    
    def show_prices(self):
        """Show Prisjakt links for the selected person's wishlist."""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person first.")
            return
        
        person_name = self.people_listbox.get(selection[0])
        person = self.storage.load_person(person_name)
        
        if not person.wishlist:
            messagebox.showinfo("Empty List", f"{person_name} has no items in their wishlist.")
            return
        
        # Create a new window to show prices
        prices_window = tk.Toplevel(self.root)
        prices_window.title(f"Prisjakt Links for {person_name}")
        prices_window.geometry("600x400")
        prices_window.transient(self.root)
        
        # Create scrolled text widget
        text_widget = scrolledtext.ScrolledText(prices_window, wrap=tk.WORD, width=70, height=20)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget.insert(tk.END, f"Prisjakt Links for {person_name}'s Wishlist\n")
        text_widget.insert(tk.END, "=" * 70 + "\n\n")
        
        # Add clickable links
        for item in sorted(person.wishlist, key=lambda x: x.priority):
            link_info = self.prisjakt.get_product_link(item.name)
            
            text_widget.insert(tk.END, f"[Priority {item.priority}] {item.name}\n")
            if item.description:
                text_widget.insert(tk.END, f"  Description: {item.description}\n")
            
            # Insert link
            start_idx = text_widget.index(tk.INSERT)
            text_widget.insert(tk.END, f"  {link_info['url']}\n")
            end_idx = text_widget.index(tk.INSERT)
            
            # Make link clickable
            tag_name = f"link_{id(item)}"
            text_widget.tag_add(tag_name, f"{start_idx}", f"{end_idx} - 1c")
            text_widget.tag_config(tag_name, foreground="blue", underline=True)
            text_widget.tag_bind(tag_name, "<Button-1>", 
                                lambda e, url=link_info['url']: webbrowser.open(url))
            text_widget.tag_bind(tag_name, "<Enter>", 
                                lambda e, tag=tag_name: text_widget.config(cursor="hand2"))
            text_widget.tag_bind(tag_name, "<Leave>", 
                                lambda e: text_widget.config(cursor=""))
            
            text_widget.insert(tk.END, "\n")
        
        text_widget.config(state=tk.DISABLED)
        
        # Add button to open all links
        def open_all_links():
            for item in person.wishlist:
                link_info = self.prisjakt.get_product_link(item.name)
                webbrowser.open(link_info['url'])
        
        button_frame = ttk.Frame(prices_window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="Open All Links in Browser", 
                  command=open_all_links).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", 
                  command=prices_window.destroy).pack(side=tk.RIGHT, padx=5)


def main():
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = SantasHelperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
