import pytest
from pytest_mock import mocker
from unittest.mock import patch
import backend.database as db
import mysql.connector

def test_login_successful(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ('$2b$12$XuIY2Jv4/zYeuRTwS3OIOuWwMz5Uc7Fu3UDF.XOeR5qZaMuK1WgP6', 1)

    # Mock bcrypt.checkpw to always return True
    mocker.patch('backend.database.bcrypt.checkpw', return_value=True)

    result = db.login('test@example.com', 'password123')

    assert result == 1

def test_login_failed(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ('$2b$12$XuIY2Jv4/zYeuRTwS3OIOuWwMz5Uc7Fu3UDF.XOeR5qZaMuK1WgP6', 1)

    # Mock bcrypt.checkpw to always return False
    mocker.patch('backend.database.bcrypt.checkpw', return_value=False)

    result = db.login('test@example.com', 'wrong_password')

    assert result is None

def test_login_database_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        db.login('test@example.com', 'password123')


# add offer

def test_add_new_offer():
    user_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 4.5

    with patch("backend.database.mysql.connector.connect") as mock_connect:

        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (123,)

        result = db.add_new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)

        assert result == 123

        mock_cursor.callproc.assert_called_once_with(
            'add_offer', (user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
        )

        mock_cursor.execute.assert_called_once_with("SELECT LAST_INSERT_ID()")

        mock_connect.return_value.commit.assert_called_once()

    mock_connect.return_value.close.assert_called_once()

def test_add_new_offer_error(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        db.add_new_offer(1, 2, 100.0, 3, 4.5)

def test_add_internal_transaction_success():
    with patch("backend.database.mysql.connector.connect") as mock_connect:

        mock_cursor = mock_connect.return_value.cursor.return_value

        db.add_internal_transaction(1, 2, 100.0)

        mock_cursor.callproc.assert_called_once_with('add_internal_transaction', (1, 2, 100.0))
        mock_connect.return_value.commit.assert_called_once()


# def test_add_internal_transaction_error(mocker):
#     with patch("backend.database.mysql.connector.connect") as mock_connect:
#         mock_cursor = mock_connect.return_value.cursor.return_value
#         mock_cursor.callproc.side_effect = mysql.connector.Error('Database error')

#         with pytest.raises(Exception):
#             add_internal_transaction(1, 2, 100.0)

def test_get_all_currency_success(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')

    mock_cursor.fetchall.return_value = [(1, 'USD'), (2, 'EUR'), (3, 'GBP')]

    result = db.get_all_currency()

    assert result == [(1, 'USD'), (2, 'EUR'), (3, 'GBP')]

def test_get_all_currency_exception(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Some other error')

    with pytest.raises(Exception, match='Some other error'):
        db.get_all_currency()


def test_add_new_offer_success(mocker):
    # Mockowanie obiektu kursora i połączenia
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')

    # Symulowanie wyniku procedury LAST_INSERT_ID()
    mock_cursor.fetchone.return_value = (1,)

    # Wywołanie funkcji
    result = db.add_new_offer(1, 2, 100.0, 3, 1.5)

    # Sprawdzenie, czy funkcja zwraca oczekiwany wynik
    assert result == 1

def test_add_new_offer_exception(mocker):
    # Mockowanie obiektu kursora i połączenia z ogólnym wyjątkiem
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Some other error')

    # Wywołanie funkcji i sprawdzenie, czy oczekiwany wyjątek został rzucony
    with pytest.raises(Exception, match='Some other error'):
        db.add_new_offer(1, 2, 100.0, 3, 1.5)
