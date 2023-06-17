import json
from typing import Dict

import requests


class ReleaseService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def add_release(self, release: Dict):
        response = requests.post(
            url=f"{self.base_url}/release", data=json.dumps(release)
        )
        return response

    def get_latest_stable_release(self, product_name):
        response = requests.get(url=f"{self.base_url}/release/{product_name}/latest")
        return response
