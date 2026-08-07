import os
import sys
from unittest.mock import patch

MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

import dbConnect


def test_get_dbconnection_uses_environment_variables(monkeypatch):
    monkeypatch.setenv("DB_ENGINE", "mysql")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "3306")
    monkeypatch.setenv("DB_NAME", "flask_demo")
    monkeypatch.setenv("DB_USER", "root")
    monkeypatch.setenv("DB_PASS", "secret")
    monkeypatch.setenv("TIMEOUT", "12")

    with patch("dbConnect.pymysql.connect", return_value="conn") as connect_mock:
        result = dbConnect.getDBconnection()

    assert result == "conn"
    connect_mock.assert_called_once()

    kwargs = connect_mock.call_args.kwargs
    assert kwargs["host"] == "localhost"
    assert kwargs["port"] == 3306
    assert kwargs["user"] == "root"
    assert kwargs["password"] == "secret"
    assert kwargs["database"] == "flask_demo"
    assert kwargs["connect_timeout"] == 12
    assert kwargs["read_timeout"] == 12
    assert kwargs["write_timeout"] == 12
