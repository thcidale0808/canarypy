import json
from typing import Dict

import requests


class ProductService:
    """Service class for handling operations related to Product.

    Attributes:
    base_url (str): The base URL for the product API.
    """

    def __init__(self, base_url: str):
        """Initialize ProductService with the base URL.

        Parameters:
        base_url (str): The base URL for the product API.
        """
        self.base_url = base_url

    def add_product(self, product: Dict):
        """Send a POST request to add a new Product to the product API.

        Parameters:
        product (Dict): The Product to add as a dictionary.

        Returns:
        response (Response): The Response object from the product API.

        Raises:
        HTTPError: If the request to the product API returns a status code that indicates an error (i.e., 4xx or 5xx).
        """
        response = requests.post(
            url=f"{self.base_url}/product", data=json.dumps(product)
        )
        response.raise_for_status()
        return response
