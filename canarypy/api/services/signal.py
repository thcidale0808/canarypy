from canarypy.api.models.signal import Signal
from canarypy.api.schemas.signal import Signal
from sqlalchemy.orm import Session


class SignalService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, signal: Signal):
        new_signal = Signal(
            release_id=signal.release_id,
            description=signal.description,
            status=signal.status,
        )
        self.db_session.add(new_signal)
        self.db_session.commit()
