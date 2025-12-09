"""Prisjakt API client for price comparison."""

from typing import List, Dict
from urllib.parse import quote


class PrisjaktClient:
    """Client for interacting with Prisjakt's product search."""
    
    BASE_URL = "https://www.prisjakt.nu"
    SEARCH_URL = f"{BASE_URL}/search"
    
    def search_product(self, query: str) -> str:
        """Search for a product and return the search results URL.
        
        Args:
            query: Product name or description to search for
            
        Returns:
            URL to Prisjakt search results
        """
        # Create a direct search URL
        encoded_query = quote(query)
        search_url = f"{self.SEARCH_URL}?search={encoded_query}"
        return search_url
    
    def get_product_link(self, product_name: str) -> Dict[str, str]:
        """Get a link to search for a product on Prisjakt.
        
        Args:
            product_name: Name of the product to search for
            
        Returns:
            Dictionary with product name and search URL
        """
        return {
            'product': product_name,
            'url': self.search_product(product_name)
        }
    
    def get_multiple_product_links(self, product_names: List[str]) -> List[Dict[str, str]]:
        """Get links for multiple products.
        
        Args:
            product_names: List of product names to search for
            
        Returns:
            List of dictionaries with product names and search URLs
        """
        return [self.get_product_link(name) for name in product_names]
