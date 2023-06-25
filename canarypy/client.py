import os

from canarypy.cli.services.release import ReleaseService
from canarypy.cli.services.signal import SignalService


class CanaryPyClient:
    """Client class for interacting with the Canary release system.

    Attributes:
    base_url (str): The base URL for the Canary release system, retrieved either from parameters or environment variables.
    """

    def __init__(self, base_url=None):
        """Initialize CanaryPyClient with the base URL for the Canary release system.

        Parameters:
        base_url (str, optional): The base URL for the Canary release system. If not provided,
                                  the value is fetched from the "CANARYPY_URL" environment variable.
        """
        self.base_url = base_url or os.getenv("CANARYPY_URL")

    def get_latest_stable_version(self, product_name: str):
        """Fetches the latest stable release version of a given product.

        Parameters:
        product_name (str): The name of the product.

        Returns:
        str: The semantic versioning (semver) string of the latest stable release.
        """
        release_service = ReleaseService(base_url=self.base_url)
        release = release_service.get_latest_stable_release(product_name)
        return f'{release.json().get("semver_version")}'

    def send_signal_to_canary(
        self, artifact_url, version, instance_id, description, status
    ):
        """Sends a signal to the Canary release system.

        Parameters:
        artifact_url (str): The URL of the artifact associated with the signal.
        version (str): The version associated with the signal.
        instance_id (str): The instance id associated with the signal.
        description (str): The description of the signal.
        status (str): The status of the signal.
        """
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
