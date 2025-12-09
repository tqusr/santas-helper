"""Command-line interface for Santa's Helper."""

import sys
from typing import Optional
from .models import Person, WishlistItem
from .storage import StorageManager
from .prisjakt import PrisjaktClient


class CLI:
    """Command-line interface for managing wishlists."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.storage = StorageManager()
        self.prisjakt = PrisjaktClient()
    
    def print_help(self):
        """Print help information."""
        help_text = """
Santa's Helper - Wishlist Management Tool

Commands:
  add-person <name>                    Add a new person
  list-people                          List all people with wishlists
  remove-person <name>                 Remove a person's wishlist
  
  add-item <person> <item> [desc] [priority]   Add item to person's wishlist
  remove-item <person> <item>          Remove item from person's wishlist
  list-items <person>                  List all items for a person
  
  find-prices <person>                 Get Prisjakt links for all items
  
  help                                 Show this help message
  
Examples:
  python cli.py add-person "John Doe"
  python cli.py add-item "John Doe" "Gaming Mouse" "Wireless gaming mouse" 1
  python cli.py find-prices "John Doe"
"""
        print(help_text)
    
    def add_person(self, name: str):
        """Add a new person."""
        person = self.storage.load_person(name)
        if person:
            print(f"Person '{name}' already exists!")
            return
        
        person = Person(name=name)
        self.storage.save_person(person)
        print(f"Added person: {name}")
    
    def list_people(self):
        """List all people."""
        people = self.storage.list_people()
        if not people:
            print("No people found.")
            return
        
        print("People with wishlists:")
        for person_name in people:
            print(f"  - {person_name}")
    
    def remove_person(self, name: str):
        """Remove a person."""
        if self.storage.delete_person(name):
            print(f"Removed person: {name}")
        else:
            print(f"Person '{name}' not found.")
    
    def add_item(self, person_name: str, item_name: str, description: str = "", priority: int = 1):
        """Add an item to a person's wishlist."""
        person = self.storage.load_person(person_name)
        if not person:
            print(f"Person '{person_name}' not found. Create them first with 'add-person'.")
            return
        
        item = WishlistItem(name=item_name, description=description, priority=priority)
        person.add_item(item)
        self.storage.save_person(person)
        print(f"Added item '{item_name}' to {person_name}'s wishlist")
    
    def remove_item(self, person_name: str, item_name: str):
        """Remove an item from a person's wishlist."""
        person = self.storage.load_person(person_name)
        if not person:
            print(f"Person '{person_name}' not found.")
            return
        
        person.remove_item(item_name)
        self.storage.save_person(person)
        print(f"Removed item '{item_name}' from {person_name}'s wishlist")
    
    def list_items(self, person_name: str):
        """List all items for a person."""
        person = self.storage.load_person(person_name)
        if not person:
            print(f"Person '{person_name}' not found.")
            return
        
        if not person.wishlist:
            print(f"{person_name} has no items in their wishlist.")
            return
        
        print(f"\n{person_name}'s Wishlist:")
        print("-" * 50)
        for item in sorted(person.wishlist, key=lambda x: x.priority):
            print(f"  [{item.priority}] {item.name}")
            if item.description:
                print(f"      {item.description}")
    
    def find_prices(self, person_name: str):
        """Get Prisjakt links for all items."""
        person = self.storage.load_person(person_name)
        if not person:
            print(f"Person '{person_name}' not found.")
            return
        
        if not person.wishlist:
            print(f"{person_name} has no items in their wishlist.")
            return
        
        print(f"\nPrisjakt Links for {person_name}'s Wishlist:")
        print("=" * 70)
        
        for item in sorted(person.wishlist, key=lambda x: x.priority):
            link_info = self.prisjakt.get_product_link(item.name)
            print(f"\n[Priority {item.priority}] {item.name}")
            if item.description:
                print(f"  Description: {item.description}")
            print(f"  Prisjakt: {link_info['url']}")
    
    def run(self, args):
        """Run the CLI with given arguments."""
        if not args or args[0] == "help":
            self.print_help()
            return
        
        command = args[0]
        
        try:
            if command == "add-person" and len(args) >= 2:
                self.add_person(args[1])
            elif command == "list-people":
                self.list_people()
            elif command == "remove-person" and len(args) >= 2:
                self.remove_person(args[1])
            elif command == "add-item" and len(args) >= 3:
                person_name = args[1]
                item_name = args[2]
                description = args[3] if len(args) > 3 else ""
                priority = int(args[4]) if len(args) > 4 else 1
                self.add_item(person_name, item_name, description, priority)
            elif command == "remove-item" and len(args) >= 3:
                self.remove_item(args[1], args[2])
            elif command == "list-items" and len(args) >= 2:
                self.list_items(args[1])
            elif command == "find-prices" and len(args) >= 2:
                self.find_prices(args[1])
            else:
                print(f"Unknown command or invalid arguments: {' '.join(args)}")
                print("Type 'help' for usage information.")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point for the CLI."""
    cli = CLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
