import os


class DBConfig:
    def __init__(self):
        self.user = os.getenv("CANARYPY_DB_USER")
        self.password = os.getenv("CANARYPY_DB_PASSWORD")
        self.host = os.getenv("CANARYPY_DB_HOST")
        self.port = os.getenv("CANARYPY_DB_PORT")
        self.db = os.getenv("CANARYPY_DB_NAME")

    def get_url(self) -> str:
        if connection_string := os.getenv("CANARYPY_DB_CONN_STRING"):
            return connection_string
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
