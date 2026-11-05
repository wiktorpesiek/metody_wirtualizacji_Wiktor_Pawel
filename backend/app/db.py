import os
import psycopg
from psycopg.rows import dict_row


def get_conn():
    """Nowe połączenie z bazą; dane logowania tylko ze zmiennych środowiskowych."""
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        row_factory=dict_row, 
    )