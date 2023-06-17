import os

from canarypy.cli.services.release import ReleaseService
from canarypy.cli.services.signal import SignalService


class CanaryPyClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("CANARYPY_URL")

    def get_latest_stable_version(self, product_name: str):
        release_service = ReleaseService(base_url=self.base_url)
        release = release_service.get_latest_stable_release(product_name)
        return f'{release.json().get("semver_version")}'

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
