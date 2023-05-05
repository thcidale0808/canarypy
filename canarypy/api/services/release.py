from canarypy.api.models.release import Release
from canarypy.api.models.product import Product
from canarypy.api.models.signal import Signal
from sqlalchemy.orm import Session
from uuid import UUID
import datetime


class ReleaseService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_release_by_id(self, release_id: UUID):
        return self.db_session.query(Release).filter(Release.id == release_id)

    def get_latest_active_release(self, product_name):
        product = self.db_session.query(Product).filter(Product.name == product_name).one_or_none()
        return self.db_session.query(Release).outerjoin(Signal).filter(
            Release.is_active == True, Release.is_canary == False,
            Release.product_id == product.id).order_by(Release.release_date.desc()).first()

    def update_canary_release(self, active_canary_release: Release) -> bool:
        active_canary_release.is_active = False
        self.db_session.commit()

    def is_canary_performance_good(self, active_canary_release: Release) -> bool:
        signals_list = self.db_session.query(Signal).join(Release).filter(
            Release.id == active_canary_release.id).order_by(Signal.created_date.desc()).all()
        failed_signals_count = 0
        for signal in signals_list:
            if signal.status == 'failed':
                failed_signals_count += 1

        # Calculate the percentage of signals that have status = 'failed'
        total_signals_count = len(signals_list)
        failed_signals_percentage = (failed_signals_count / total_signals_count) * 100 if total_signals_count >0 else 0
        return failed_signals_percentage < active_canary_release.threshold

    def should_continue_canary_period(self, active_canary_release: Release):
        current_time = datetime.datetime.now()
        canary_time_limit = active_canary_release.release_date + datetime.timedelta(days=active_canary_release.canary_period)
        if current_time < canary_time_limit and self.is_canary_performance_good(active_canary_release):
            return True
        self.finish_canary_release(active_canary_release)
        return False

    def finish_canary_release(self, active_canary_release):
        active_canary_release.is_active = False
        self.db_session.commit()

    def get_latest_signal(self, release):
        return self.db_session.query(Signal).join(Release).filter(
            Release.id == release.id).order_by(Signal.created_date.desc()).first()

    def get_latest_canary_release(self, product_name):
        product = self.db_session.query(Product).filter(Product.name == product_name).one_or_none()
        return self.db_session.query(Release).outerjoin(Signal).filter(
            Release.is_active == True, Release.is_canary == True,
            Release.product_id == product.id).order_by(Release.release_date.desc()).first()

    def get_latest_release(self, product_name):
        latest_active = self.get_latest_active_release(product_name)
        latest_canary = self.get_latest_canary_release(product_name)
        if not latest_canary:
            return latest_active
        if self.should_continue_canary_period(latest_canary):
            latest_active_version_signal = self.get_latest_signal(latest_active)
            latest_canary_version_signal = self.get_latest_signal(latest_canary)
            if not latest_canary_version_signal:
                return latest_canary
            elif not latest_active_version_signal:
                return latest_active
            elif latest_canary_version_signal.created_date > latest_active_version_signal.created_date:
                return latest_canary
        return latest_active

    def save(self, release):
        product = self.db_session.query(Product).filter(Product.artifact_url == release.artifact_url).one_or_none()

        new_release = Release(
            product_id=product.id,
            semver_version=release.semver_version,
            is_canary=release.is_canary,
            is_active=release.is_active,
            threshold=release.threshold,
            canary_period=release.canary_period
        )
        self.db_session.add(new_release)
        self.db_session.commit()
