from AbstractFactoryDBContextManager import AbstractDBManager, ConnectionError, CredentialError, SQLExecutionError # type: ignore

from mysql.connector import connect, InterfaceError, ProgrammingError

class MySQLDBManager(AbstractDBManager):
    def __enter__(self) -> 'cursor': # type: ignore
        try:
            self.connection = connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except InterfaceError as e:
            raise ConnectionError(f"Failed to connect to the database: {e}")
        except ProgrammingError as e:
            raise CredentialError(f"Invalid credentials or database configuration: {e}")

    def __exit__(self, exc_type, exc_val, exc_tab) -> None:
        if self.connection:
            if exc_type is None:
                self.connection.commit()
                self.cursor.close()
                self.connection.close()
            else:
                self.connection.rollback()
                if exc_type is ProgrammingError:
                    raise SQLExecutionError(f"An error occurred during SQL execution: {exc_val}")
                else:
                    raise exc_type(exc_val).with_traceback(exc_tab)
        