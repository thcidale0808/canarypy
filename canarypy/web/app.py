from canarypy.web.services.release import ReleaseMetricsService
from canarypy.web.views.release import render_ui
from canarypy.api.dependencies.db import get_db
from contextlib import contextmanager


db_context = contextmanager(get_db)


def main():
    with db_context() as session:

        release_metrics_service = ReleaseMetricsService(db_session=session)

        df = release_metrics_service.get_release_metrics()

        render_ui(df)


if __name__ == "__main__":
    main()
