import requests
from typing import Dict
import json


class ReleaseService:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def add_release(self, release: Dict):
        response = requests.post(url=f'{self.base_url}/release', data=json.dumps(release))
        return response

    def get_lastest_stable_release(self, artifact_url):
        response = requests.get(url=f'{self.base_url}/release/{artifact_url}/latest')
        return response
