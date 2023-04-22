import os
from canarypy.services.release import ReleaseService


class CanaryPyClient:

    def __init__(self, base_url=os.getenv('CANARYPY_URL')):
        self.base_url = base_url

    def get_latest_stable_version(self, artifact_url: str):
        release_service = ReleaseService(base_url=self.base_url)
        release = release_service.get_lastest_stable_release(artifact_url)
        return f'{artifact_url}:{release.get("semver_version")}'
