from pymysql import connect  # type: ignore


class DbManager:
    """
    A context manager for managing database connections and cursors.
    This class allows you to use a 'with' statement to automatically handle
    the opening and closing of database connections and cursors.
    """

    def __init__(self, db_config: dict) -> None:
        self.config = db_config or {}
        self.connection = None
        self.cursor = None

    def __enter__(self) -> 'cursor':
        self.connection = connect(**self.config)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tab) -> None:
        if self.connection:
            self.connection.commit()
            self.connection.close()
            self.cursor.close()