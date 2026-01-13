from config.constants import DbConstants
from config.settings import configuration, SupabaseDBConfig


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigService(metaclass=Singleton):

    @property
    def supabaseConfig(self) -> SupabaseDBConfig:
        conn = (
            configuration.supabase.connection_string
            if configuration.supabase and configuration.supabase.connection_string
            else None
        )
        if not conn:
            from os import getenv

            conn = getenv(DbConstants.SUPABASE_CONNECTION_STRING, "")
        schema = (
            configuration.supabase.db_schema
            if configuration.supabase and configuration.supabase.db_schema
            else DbConstants.SCHEMA
        )
        return SupabaseDBConfig(connection_string=conn, db_schema=schema)
