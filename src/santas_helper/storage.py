"""Storage management for person wishlists using YAML files."""

import os
import yaml
from pathlib import Path
from typing import List, Optional
from .models import Person


class StorageManager:
    """Manages storage of person data in YAML files."""
    
    def __init__(self, storage_dir: str = "wishlists"):
        """Initialize the storage manager.
        
        Args:
            storage_dir: Directory where YAML files are stored
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def _get_filepath(self, person_name: str) -> Path:
        """Get the filepath for a person's YAML file.
        
        Args:
            person_name: Name of the person
            
        Returns:
            Path to the YAML file
        """
        # Sanitize filename
        safe_name = "".join(c for c in person_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        return self.storage_dir / f"{safe_name}.yaml"
    
    def save_person(self, person: Person) -> None:
        """Save a person's data to a YAML file.
        
        Args:
            person: Person object to save
        """
        filepath = self._get_filepath(person.name)
        with open(filepath, 'w') as f:
            yaml.safe_dump(person.to_dict(), f, default_flow_style=False, sort_keys=False)
    
    def load_person(self, person_name: str) -> Optional[Person]:
        """Load a person's data from a YAML file.
        
        Args:
            person_name: Name of the person
            
        Returns:
            Person object or None if not found
        """
        filepath = self._get_filepath(person_name)
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        return Person.from_dict(data)
    
    def list_people(self) -> List[str]:
        """List all people with wishlists.
        
        Returns:
            List of person names
        """
        people = []
        for filepath in self.storage_dir.glob("*.yaml"):
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                people.append(data['name'])
        return sorted(people)
    
    def delete_person(self, person_name: str) -> bool:
        """Delete a person's wishlist file.
        
        Args:
            person_name: Name of the person
            
        Returns:
            True if deleted, False if not found
        """
        filepath = self._get_filepath(person_name)
        if filepath.exists():
            filepath.unlink()
            return True
        return False
