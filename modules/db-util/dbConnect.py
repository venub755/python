import os
import pymysql

DEFAULT_TIMEOUT = 10


def _get_env(name: str, default=None):
    value = os.getenv(name)
    if value is None or value == '':
        return default
    return value


def _get_timeout() -> int:
    timeout_value = _get_env('TIMEOUT', DEFAULT_TIMEOUT)
    try:
        return int(timeout_value)
    except (TypeError, ValueError):
        return DEFAULT_TIMEOUT


def getDBconnection() -> pymysql.connections.Connection:
    db_engine = (_get_env('DB_ENGINE') or 'mysql').lower()
    if db_engine != 'mysql':
        raise ValueError(f"Unsupported database engine: {db_engine}")

    required_values = {
        'DB_HOST': _get_env('DB_HOST'),
        'DB_PORT': _get_env('DB_PORT'),
        'DB_NAME': _get_env('DB_NAME'),
        'DB_USER': _get_env('DB_USER'),
        'DB_PASS': _get_env('DB_PASS'),
    }
    missing = [name for name, value in required_values.items() if not value]
    if missing:
        raise ValueError(f"Missing required DB environment variables: {', '.join(missing)}")

    timeout = _get_timeout()
    return pymysql.connect(
        host=required_values['DB_HOST'],
        port=int(required_values['DB_PORT']),
        user=required_values['DB_USER'],
        password=required_values['DB_PASS'],
        database=required_values['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4',
        connect_timeout=timeout,
        read_timeout=timeout,
        write_timeout=timeout,
    )


def connect():
    return getDBconnection()