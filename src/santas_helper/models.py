"""Data models for Santa's Helper."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class WishlistItem:
    """Represents an item on a wishlist."""
    name: str
    description: str = ""
    priority: int = 1  # 1 = highest priority
    
    def to_dict(self):
        """Convert to dictionary for YAML serialization."""
        return {
            'name': self.name,
            'description': self.description,
            'priority': self.priority
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(
            name=data['name'],
            description=data.get('description', ''),
            priority=data.get('priority', 1)
        )


@dataclass
class Person:
    """Represents a person with their wishlist."""
    name: str
    wishlist: List[WishlistItem] = field(default_factory=list)
    
    def add_item(self, item: WishlistItem):
        """Add an item to the wishlist."""
        self.wishlist.append(item)
    
    def remove_item(self, item_name: str):
        """Remove an item from the wishlist by name."""
        self.wishlist = [item for item in self.wishlist if item.name != item_name]
    
    def to_dict(self):
        """Convert to dictionary for YAML serialization."""
        return {
            'name': self.name,
            'wishlist': [item.to_dict() for item in self.wishlist]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(
            name=data['name'],
            wishlist=[WishlistItem.from_dict(item) for item in data.get('wishlist', [])]
        )
