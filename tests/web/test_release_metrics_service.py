from sqlalchemy.orm import Session
from canarypy.api.models.product import Product
from canarypy.api.models.signal import Signal
from canarypy.api.models.release import Release, ReleaseCanaryBand
from canarypy.web.services.release import ReleaseMetricsService
import numpy as np


def test_web_get_release_metrics(db_session: Session):
    product = Product(name='Product1')
    release = Release(product=product, semver_version='1.0.0')
    canary_band = ReleaseCanaryBand(release=release, band_number=1)
    signal1 = Signal(release=release, is_canary=True, status='success', instance_id='1', release_canary_band=canary_band)
    signal2 = Signal(release=release, is_canary=False, instance_id='1', status='success')

    db_session.add(product)
    db_session.add(release)
    db_session.add(canary_band)
    db_session.add(signal1)
    db_session.add(signal2)
    db_session.commit()

    release_metrics_service = ReleaseMetricsService(db_session=db_session)

    df = release_metrics_service.get_release_metrics()

    assert not df.empty
    assert df.loc[0, 'product_name'] == 'Product1'
    assert df.loc[0, 'release_version'] == '1.0.0'
    assert df.loc[0, 'canary_band_number'] == 1
    assert df.loc[0, 'release_is_canary']
    assert df.loc[0, 'success_canary_count'] == 1.0
    assert df.loc[0, 'success_non_canary_count'] == 0.0
    assert df.loc[0, 'failed_canary_count'] == 0.0
    assert df.loc[0, 'failed_non_canary_count'] == 0.0
    assert df.loc[0, 'total_count'] == 1.0
    assert df.loc[1, 'product_name'] == 'Product1'
    assert df.loc[1, 'release_version'] == '1.0.0'
    assert np.isnan(df.loc[1, 'canary_band_number'])
    assert not df.loc[1, 'release_is_canary']
    assert df.loc[1, 'success_canary_count'] == 0.0
    assert df.loc[1, 'success_non_canary_count'] == 1.0
    assert df.loc[1, 'failed_canary_count'] == 0.0
    assert df.loc[1, 'failed_non_canary_count'] == 0.0
    assert df.loc[1, 'total_count'] == 1.0
