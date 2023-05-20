import os

from canarypy.services.release import ReleaseService
from canarypy.services.signal import SignalService


class CanaryPyClient:
    def __init__(self, base_url=os.getenv("CANARYPY_URL")):
        self.base_url = base_url

    def get_latest_stable_version(self, artifact_url: str):
        release_service = ReleaseService(base_url=self.base_url)
        release = release_service.get_lastest_stable_release(artifact_url)
        return f'{artifact_url}:{release.json().get("semver_version")}'

    def send_signal_to_canary(
        self, artifact_url, version, instance_id, description, status
    ):
        signal_service = SignalService(base_url=self.base_url)

        signal_service.add_signal(
            {
                "artifact_url": artifact_url,
                "semver_version": version,
                "instance_id": instance_id,
                "description": description,
                "status": status,
            }
        )
