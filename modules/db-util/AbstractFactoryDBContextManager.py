from abc import ABC, abstractmethod

class ConnectionError(Exception):
    pass

class CredentialError(Exception):
    pass

class SQLExecutionError(Exception):
    pass

# Define a common interface for database managers
class AbstractDBManager(ABC):
    """
    An abstract context manager for managing database connections and cursors.
    This class allows you to use a 'with' statement to automatically handle
    the opening and closing of database connections and cursors.
    """
    def __init__(self, db_config) -> None:
        self.config = db_config or {}
        self.connection = None
        self.cursor = None

    # Child classes must implement this method
    @abstractmethod
    def __enter__(self) -> 'cursor': # type: ignore
        pass

    # Child classes must implement this method
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tab) -> None: 
        pass

# The Factory Class
class DBManagerFactory:
    @staticmethod
    def create_db_manager(db_type: str, db_config: dict) -> AbstractDBManager:
        if db_type.lower() == "mysql":
            from MySQLDBContextManager import MySQLDBManager  # type: ignore
            return MySQLDBManager(db_config)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
