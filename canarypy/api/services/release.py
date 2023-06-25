import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from canarypy.api.models.product import Product
from canarypy.api.models.release import Release, ReleaseCanaryBand
from canarypy.api.models.signal import Signal
from canarypy.api.schemas import release as release_schema


class ReleaseService:
    """ReleaseService provides methods to interact with Release objects stored in a
    database."""

    def __init__(self, db_session: Session):
        """Initialize ReleaseService with the database session.

        Parameters:
        db_session (Session): SQLAlchemy session object.
        """
        self.db_session = db_session

    def get_release_by_id(self, release_id: UUID):
        """Retrieve a Release by its ID.

        Parameters:
        release_id (UUID): The ID of the Release to retrieve.

        Returns:
        Release: The Release object or None if not found.
        """
        return self.db_session.query(Release).filter(Release.id == release_id)

    def get_latest_active_release(self, product_name: str):
        """Get the latest active release of the specified product.

        Parameters:
        product_name (str): The name of the product.

        Returns:
        Release: The latest active Release object or None if not found.
        """
        product = (
            self.db_session.query(Product)
            .filter(Product.name == product_name)
            .one_or_none()
        )
        return (
            self.db_session.query(Release)
            .outerjoin(Signal)
            .filter(
                Release.is_active == True,
                Release.is_canary == False,
                Release.product_id == product.id,
            )
            .order_by(Release.release_date.desc())
            .first()
        )

    def update_canary_release(self, active_canary_release: Release) -> bool:
        """Update the is_active status of the given canary release to False.

        Parameters:
        active_canary_release (Release): The canary release to update.

        Returns:
        None
        """
        active_canary_release.is_active = False
        self.db_session.commit()

    def is_canary_performance_good(self, active_canary_release: Release) -> bool:
        """Check if the performance of the canary release is good.

        Parameters:
        active_canary_release (Release): The canary release to check.

        Returns:
        bool: True if the performance is good, False otherwise.
        """
        signals_list = (
            self.db_session.query(Signal)
            .join(Release)
            .filter(Release.id == active_canary_release.id)
            .order_by(Signal.created_date.desc())
            .all()
        )
        failed_signals_count = 0
        for signal in signals_list:
            if signal.status == "failed":
                failed_signals_count += 1
        total_signals_count = len(signals_list)
        failed_signals_percentage = (
            (failed_signals_count / total_signals_count) * 100
            if total_signals_count > 0
            else 0
        )
        return failed_signals_percentage < active_canary_release.threshold

    def should_continue_canary_period(
        self, active_canary_release: Release, latest_active_release: Release
    ):
        """Check if the canary period should continue or not.

        Parameters:
        active_canary_release (Release): The active canary release.
        latest_active_release (Release): The latest active release.

        Returns:
        bool: True if the canary period should continue, False otherwise.
        """
        current_time = datetime.datetime.now()
        canary_time_limit = active_canary_release.release_date + datetime.timedelta(
            days=float(active_canary_release.canary_period)
        )
        if current_time < canary_time_limit and self.is_canary_performance_good(
            active_canary_release
        ):
            return True
        elif current_time > canary_time_limit and self.is_canary_performance_good(
            active_canary_release
        ):
            self.finish_canary_release(
                active_canary_release, latest_active_release, True
            )
        else:
            self.finish_canary_release(
                active_canary_release, latest_active_release, False
            )
        return False

    def finish_canary_release(
        self,
        active_canary_release: Release,
        active_release: Release,
        is_winner: bool = False,
    ):
        """Finalize the canary release process based on whether it is a winner or not.

        Parameters:
        active_canary_release (Release): The active canary release.
        active_release (Release): The active release.
        is_winner (bool): A flag indicating if the canary release is a winner. Default is False.

        Returns:
        None
        """
        if is_winner:
            active_canary_release.is_canary = False
            active_canary_release.is_active = True
            active_release.is_active = False
        else:
            active_canary_release.is_active = False
        self.db_session.commit()

    def get_latest_signal(self, release: Release):
        """Get the latest signal for the given release.

        Parameters:
        release (Release): The release to get the latest signal for.

        Returns:
        Signal: The latest Signal object or None if not found.
        """
        return (
            self.db_session.query(Signal)
            .join(Release)
            .filter(Release.id == release.id)
            .order_by(Signal.created_date.desc())
            .first()
        )

    def get_latest_canary_release(self, product_name: str):
        """Get the latest canary release of the specified product.

        Parameters:
        product_name (str): The name of the product.

        Returns:
        Release: The latest canary Release object or None if not found.
        """
        product = (
            self.db_session.query(Product)
            .filter(Product.name == product_name)
            .one_or_none()
        )
        return (
            self.db_session.query(Release)
            .outerjoin(Signal)
            .filter(
                Release.is_active == True,
                Release.is_canary == True,
                Release.product_id == product.id,
            )
            .order_by(Release.release_date.desc())
            .first()
        )

    def get_latest_release(self, product_name: str):
        """Get the latest release (either canary or active) of the specified product.

        Parameters:
        product_name (str): The name of the product.

        Returns:
        Release: The latest Release object or None if not found.
        """
        latest_active = self.get_latest_active_release(product_name)
        latest_canary = self.get_latest_canary_release(product_name)
        if not latest_canary:
            return latest_active
        if not latest_active:
            return latest_canary
        if self.should_continue_canary_period(latest_canary, latest_active):
            latest_active_version_signal = self.get_latest_signal(latest_active)
            latest_canary_version_signal = self.get_latest_signal(latest_canary)
            if not latest_canary_version_signal:
                return latest_canary
            elif not latest_active_version_signal:
                return latest_active
            elif (
                latest_canary.active_canary_band_pc
                >= latest_canary.active_canary_band_executed_pc
            ):
                return latest_canary
        return latest_active

    def create_canary_bands_for_release(self, release: Release):
        """Create canary bands for the given release.

        Parameters:
        release (Release): The release to create canary bands for.

        Returns:
        None
        """
        for i in range(0, release.band_count):
            new_canary_band_release = ReleaseCanaryBand(
                release_id=release.id,
                start_date=release.release_date
                + i
                * datetime.timedelta(
                    seconds=(float(release.canary_period) / release.band_count)
                    * 24
                    * 60
                    * 60
                ),
                band_number=i + 1,
                release=release,
            )
            self.db_session.add(new_canary_band_release)
            # release.canary_bands.append(new_canary_band_release)
            self.db_session.commit()

    def save(self, release: release_schema.Release):
        """Save a new Release to the database.

        Parameters:
        release (Release): The Release to save.

        Returns:
        Release: The newly saved Release object.
        """
        product = (
            self.db_session.query(Product)
            .filter(Product.artifact_url == release.artifact_url)
            .one_or_none()
        )
        latest_active = self.get_latest_active_release(product.name)
        latest_canary = self.get_latest_canary_release(product.name)
        if latest_canary and self.is_canary_performance_good(latest_canary):
            self.finish_canary_release(latest_canary, latest_active, True)
        elif latest_canary and not self.is_canary_performance_good(latest_canary):
            self.finish_canary_release(latest_canary, latest_active, False)
        new_release = Release(
            product_id=product.id,
            semver_version=release.semver_version,
            is_canary=release.is_canary,
            is_active=release.is_active,
            threshold=release.threshold,
            canary_period=release.canary_period,
            band_count=release.band_count,
            release_date=release.release_date,
        )
        self.db_session.add(new_release)

        self.db_session.flush()

        if release.is_canary:
            self.create_canary_bands_for_release(new_release)

        self.db_session.commit()
        return new_release
