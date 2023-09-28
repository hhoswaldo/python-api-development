# utils.py

import os


def get_conn_str() -> str:
    """Get connection string for postgres database.

    Raises:
        KeyError: When any of the required env variables is not found
    """
    return (
        f"dbname={os.environ['POSTGRES_DB']} "
        f"user={os.environ['POSTGRES_USER']} "
        f"password={os.environ['POSTGRES_PASSWORD']} "
        f"host={os.environ['POSTGRES_HOST']} "
        f"port={os.environ['POSTGRES_PORT']}"
    )
