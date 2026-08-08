from unittest.mock import MagicMock, patch
import os
import sys

MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

import DbContextManager

def test_dbmanager_enter_creates_connection_and_cursor():
    db_config = {"host": "localhost", "user": "root"}
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    with patch("DbContextManager.connect", return_value=mock_connection) as connect_mock:
        manager = DbContextManager.DbManager(db_config)
        with manager as cursor:
            assert cursor is mock_cursor
            connect_mock.assert_called_once_with(**db_config)
            mock_connection.cursor.assert_called_once_with()

    assert manager.connection is mock_connection
    assert manager.cursor is mock_cursor


def test_dbmanager_exit_commits_and_closes_resources():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    manager = DbContextManager.DbManager({})
    manager.connection = mock_connection
    manager.cursor = mock_cursor

    manager.__exit__(None, None, None)

    mock_connection.commit.assert_called_once_with()
    mock_connection.close.assert_called_once_with()
    mock_cursor.close.assert_called_once_with()

