import os


class DBConfig:
    def __init__(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.db = os.getenv("POSTGRES_DB")

    def get_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class MigrationsConfig(DBConfig):
    def __init__(self):
        super().__init__()
        self.user = os.getenv("MIGRATIONS_USER") or self.user
        self.password = os.getenv("MIGRATIONS_PASSWORD") or self.password
