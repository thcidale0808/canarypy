import json
from typing import Dict

import requests


class SignalService:
    """Service class for handling operations related to Signal.

    Attributes:
    base_url (str): The base URL for the signal API.
    """

    def __init__(self, base_url: str):
        """Initialize SignalService with the base URL.

        Parameters:
        base_url (str): The base URL for the signal API.
        """
        self.base_url = base_url

    def add_signal(self, signal: Dict):
        """Send a POST request to add a new Signal to the signal API.

        Parameters:
        signal (Dict): The Signal to add as a dictionary.

        Returns:
        response (Response): The Response object from the signal API.
        """
        response = requests.post(url=f"{self.base_url}/signal", data=json.dumps(signal))
        response.raise_for_status()
        return response
