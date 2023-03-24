import requests
from typing import Dict
import json


class ProductService:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def add_project(self, product: Dict):
        response = requests.post(url=f'{self.base_url}/product', data=json.dumps(product))
        return response
