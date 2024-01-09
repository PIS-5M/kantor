import pytest
from pytest_mock import mocker
from backend.database import login
import backend.database as db

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


def test_user_data_correct_id(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ('Test name', 'Test surname', 'test@example.com')

    name, surname, email = db.get_user_data(1)

    assert name == 'Test name'
    assert surname == 'Test surname'
    assert email == 'test@example.com'


def test_user_data_incorrect_id(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ()

    name, surname, email = db.get_user_data(1)

    assert name == None
    assert surname == None
    assert email == None


def test_user_data_database_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        db.get_user_data(1)
