# core/config.py
#!/usr/bin/env python3
""" Core library

Module docstring

Available classes
- AuthSettings: description
- DatabaseSettings: description

Available constants:
- AUTH_SETTINGS: description
- DATABASE_SETTINGS: description
"""

from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    """Represents OAuth2 settings

    Public attributes:
    - auth_secret_key: A string representing the authentication secret key.
    - auth_algorithm: A string representing the authentication algorithm.
    - auth_token_expire_minutes: An integer representing the expiration time
    for authentication tokens in minutes.
    """

    auth_secret_key: str
    auth_algorithm: str
    auth_token_expire_minutes: int


class DatabaseSettings(BaseSettings):
    """Represents database connection settings

    Public attributes:
    - azure_postgresql_connectionstring: A string representing the connection string for
    the Azure PostgreSQL database.
    - database_uri: A string representing the connection string for the Azure PostgreSQL database.
    """

    azure_postgresql_connectionstring: str

    @property
    def database_uri(self) -> str:
        """Extracts the necessary parameters from the azure_postgresql_connectionstring
        and constructs a PostgreSQL URI for the database connection.

        Returns
            postgresql connection string
        """
        conn_str_params = {
            pair.split("=")[0]: pair.split("=")[1]
            for pair in self.azure_postgresql_connectionstring.split(" ")
        }
        return f"postgresql+psycopg2://{conn_str_params['user']}:{conn_str_params['password']}@{conn_str_params['host']}/{conn_str_params['dbname']}"


AUTH_SETTINGS = AuthSettings()
DATABASE_SETTINGS = DatabaseSettings()
