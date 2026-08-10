import os
import sys
import pytest
from unittest.mock import MagicMock, patch

MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"MODULE_DIR: {MODULE_DIR}")
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from AbstractFactoryDBContextManager import DBManagerFactory, AbstractDBManager
from MySQLDBContextManager import MySQLDBManager, ConnectionError, CredentialError, SQLExecutionError

def test_abstract_factory_db_context_manager_creates_mysql_manager():
    
    db_config = {
        'host': 'localhost',
        'user': 'test_user',
        'password': 'test_password',
        'database': 'test_db'
    }

    db_manager = DBManagerFactory.create_db_manager("mysql", db_config)

    assert isinstance(db_manager, AbstractDBManager)
    assert db_manager.__class__.__name__ == "MySQLDBManager"


def test_abstract_factory_db_context_manager_unsupported_type_raises_value_error():

    with pytest.raises(ValueError, match="Unsupported database type"):
        DBManagerFactory.create_db_manager("sqlite", {})


def test_mysql_db_manager_enter_raises_connection_error_on_interface_error():
    from mysql.connector import InterfaceError

    db_config = {
        'host': 'localhost',
        'user': 'test_user',
        'password': 'test_password',
        'database': 'test_db'
    }

    with patch("MySQLDBContextManager.connect", side_effect=InterfaceError("server down")):
        manager = MySQLDBContextManager.MySQLDBManager(db_config)

        with pytest.raises(ConnectionError, match="Failed to connect to the database"):
            with manager as cursor:
                pass


def test_mysql_db_manager_enter_raises_credential_error_on_programming_error():
    from AbstractFactoryDBContextManager import CredentialError
    from mysql.connector import ProgrammingError

    db_config = {
        'host': 'localhost',
        'user': 'test_user',
        'password': 'test_password',
        'database': 'test_db'
    }

    with patch("MySQLDBContextManager.connect", side_effect=ProgrammingError("bad credentials")):
        manager = MySQLDBContextManager.MySQLDBManager(db_config)

        with pytest.raises(CredentialError, match="Invalid credentials or database configuration"):
            with manager as cursor:
                pass


def test_mysql_db_manager_exit_commits_and_closes_when_no_exception():
    manager = MySQLDBContextManager.MySQLDBManager({})
    manager.connection = MagicMock()
    manager.cursor = MagicMock()

    manager.__exit__(None, None, None)

    manager.connection.commit.assert_called_once_with()
    manager.cursor.close.assert_called_once_with()
    manager.connection.close.assert_called_once_with()


def test_mysql_db_manager_exit_rolls_back_and_raises_sql_execution_error_on_programming_error():
    from mysql.connector import ProgrammingError

    manager = MySQLDBContextManager.MySQLDBManager({})
    manager.connection = MagicMock()
    manager.cursor = MagicMock()

    with pytest.raises(SQLExecutionError, match="An error occurred during SQL execution"):
        manager.__exit__(ProgrammingError, ProgrammingError("sql issue"), None)

    manager.connection.rollback.assert_called_once_with()