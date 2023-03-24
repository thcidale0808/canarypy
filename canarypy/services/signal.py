import requests
from typing import Dict
import json


class SignalService:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def add_signal(self, signal: Dict):
        response = requests.post(url=f'{self.base_url}/signal', data=json.dumps(signal))
        return response
