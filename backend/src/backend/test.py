import pytest
from pytest_mock import mocker
from backend.database import login
import backend.database as db
from unittest.mock import patch, MagicMock

def test_login_successful(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ('$2b$12$XuIY2Jv4/zYeuRTwS3OIOuWwMz5Uc7Fu3UDF.XOeR5qZaMuK1WgP6', 1)

    # Mock bcrypt.checkpw to always return True
    mocker.patch('backend.database.bcrypt.checkpw', return_value=True)

    result = login('test@example.com', 'password123')

    assert result == 1

def test_login_failed(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ('$2b$12$XuIY2Jv4/zYeuRTwS3OIOuWwMz5Uc7Fu3UDF.XOeR5qZaMuK1WgP6', 1)

    # Mock bcrypt.checkpw to always return False
    mocker.patch('backend.database.bcrypt.checkpw', return_value=False)

    result = login('test@example.com', 'wrong_password')

    assert result is None

def test_login_database_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        login('test@example.com', 'password123')



def test_wallet_add(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ()
    wallet_id = 1
    value = 100.0
    db.wallet_add(wallet_id, value)

def test_wallet_add_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')
    wallet_id = 1
    value = 100.0

    with pytest.raises(Exception, match='Database error'):
        db.wallet_add(wallet_id, value)


def test_wallet_subtract(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = (200.0,)
    wallet_id = 1
    value = 50.0

    result = db.wallet_subtract(wallet_id, value)

    assert result is True



def test_wallet_subtract_to_little(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = (50.0,)
    wallet_id = 1
    value = 200.0

    result = db.wallet_subtract(wallet_id, value)

    assert result is False


def test_wallet_subtract_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')
    wallet_id = 1
    value = 100.0

    with pytest.raises(Exception, match='Database error'):
        db.wallet_subtract(wallet_id, value)
