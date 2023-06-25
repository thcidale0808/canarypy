import pandas as pd
from sqlalchemy.orm import Session


class ReleaseMetricsService:
    """Service class for handling operations related to Release Metrics.

    Attributes:
    db_session (Session): A SQLAlchemy Session instance used to query the database.
    """

    def __init__(self, db_session: Session):
        """Initialize ReleaseMetricsService with the database session.

        Parameters:
        db_session (Session): A SQLAlchemy Session instance used to query the database.
        """
        self.db_session = db_session

    def get_release_metrics(self):
        """Execute a SQL query to extract metrics for each product release.

        This function extracts metrics such as success and failure counts for both canary and non-canary signals,
        grouped by product name, release version, canary band number, and time (rounded to the nearest hour).

        Returns:
        df (DataFrame): A pandas DataFrame containing the release metrics.
        """
        sql_query = """
            SELECT
                p.name AS product_name,
                r.semver_version AS release_version,
                rcb.band_number AS canary_band_number,
                s.is_canary AS release_is_canary,
                date_trunc('hour', s.created_date) AS hour,
                COUNT(s.id) FILTER (WHERE s.status = 'success' AND s.is_canary = True)::float  as success_canary_count,
                COUNT(s.id) FILTER (WHERE s.status = 'success' AND s.is_canary = False)::float  as success_non_canary_count,
                COUNT(s.id) FILTER (WHERE s.status = 'failed' AND s.is_canary = True)::float  as failed_canary_count,
                COUNT(s.id) FILTER (WHERE s.status = 'failed' AND s.is_canary = False)::float  as failed_non_canary_count,
                COUNT(s.id)::float AS total_count
            FROM
                signal s
            JOIN
                release r ON s.release_id = r.id
            JOIN
                product p ON r.product_id = p.id
            LEFT JOIN
                release_canary_band rcb ON s.release_canary_band_id = rcb.id
            GROUP BY
                p.name,
                r.semver_version,
                rcb.band_number,
                s.is_canary,
                hour
            ORDER BY
                p.name,
                r.semver_version,
                rcb.band_number,
                hour
        """

        df = pd.read_sql(sql_query, self.db_session.bind)
        return df
