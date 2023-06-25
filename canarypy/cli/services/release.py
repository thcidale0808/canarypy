import json
from typing import Dict

import requests


class ReleaseService:
    """Service class for handling operations related to Release.

    Attributes:
    base_url (str): The base URL for the release API.
    """

    def __init__(self, base_url: str):
        """Initialize ReleaseService with the base URL.

        Parameters:
        base_url (str): The base URL for the release API.
        """
        self.base_url = base_url

    def add_release(self, release: Dict):
        """Send a POST request to add a new Release to the release API.

        Parameters:
        release (Dict): The Release to add as a dictionary.

        Returns:
        response (Response): The Response object from the release API.
        """
        response = requests.post(
            url=f"{self.base_url}/release", data=json.dumps(release)
        )
        return response

    def get_latest_stable_release(self, product_name: str):
        """Send a GET request to retrieve the latest stable Release of a product from
        the release API.

        Parameters:
        product_name (str): The name of the product.

        Returns:
        response (Response): The Response object from the release API, containing the latest stable Release of the product.

        Raises:
        HTTPError: If the request to the release API returns a status code that indicates an error (i.e., 4xx or 5xx).
        """
        response = requests.get(url=f"{self.base_url}/release/{product_name}/latest")
        response.raise_for_status()
        return response
