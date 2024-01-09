import pytest
from pytest_mock import mocker
import backend.database as db
from unittest.mock import patch, Mock
import mysql.connector
import datetime
import math
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
        db.get_user_data(1)
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


def test_get_possible_match_offer_list_success(mocker):
    # Mockowanie obiektu kursora i połączenia
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')

    # Symulowanie wyniku zapytania
    mock_cursor.fetchall.return_value = [(1, 'USD', 'EUR', 1.2, 100.0), (2, 'GBP', 'USD', 1.5, 150.0)]

    # Wywołanie funkcji
    result = db.get_possible_match_offer_list(2, 1, 1.3)

    # Sprawdzenie, czy funkcja zwraca oczekiwany wynik
    assert result == [(1, 'USD', 'EUR', 1.2, 100.0), (2, 'GBP', 'USD', 1.5, 150.0)]


def test_get_possible_match_offer_list_exception(mocker):
    # Mockowanie obiektu kursora i połączenia z ogólnym wyjątkiem
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Some other error')

    # Wywołanie funkcji i sprawdzenie, czy oczekiwany wyjątek został rzucony
    with pytest.raises(Exception, match='Some other error'):
        db.get_possible_match_offer_list(2, 1, 1.3)

def test_add_match_offers_success(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')

    # Mock bcrypt.checkpw to always return True
    mocker.patch('backend.database.bcrypt.checkpw', return_value=True)

    result = db.add_match_offers(1, 10.0, 2, 8.0)

    assert result == True

# def test_add_match_offers_error(mocker):
#     # Mock the cursor and execute method to raise an exception
#     mocker.patch('backend.database.mysql.connector.connect')
#     mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
#     mock_cursor.execute.side_effect = Exception('Database error')

#     with pytest.raises(Exception, match='Database error'):
#         db.add_match_offers(1, 10.0, 2, 8.0)


def test_offer_match(mocker):
    # Given
    offer_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 1.5
    mocker.patch('backend.database.mysql.connector.connect')
    # Mockowanie funkcji bazodanowych                                               1, 2, 50.0, 3, 1.5
    mocker.patch('backend.database.get_possible_match_offer_list', return_value=[(1, datetime.datetime(2024, 1, 9, 16, 11, 27), None, 1, 2, 50.0, 3, 1.86, 50.0, 0)])  # Możesz dostosować wartości zwracane do swojego testu
    mocker.patch('backend.database.add_match_offers', return_value=True)

    # When
    result = db.offer_match(offer_id, selled_currency_id, value, wanted_currency_id, exchange_rate)

    # Then
    assert result == [[93.0, 50.0]]  # Oczekuj odpowiedniego wyniku

def test_offer_match_2(mocker):
    # Given
    offer_id = 1
    selled_currency_id = 2
    value = 50.0
    wanted_currency_id = 3
    exchange_rate = 2.0
    mocker.patch('backend.database.mysql.connector.connect')
    # Mockowanie funkcji bazodanowych                                               1, 2, 50.0, 3, 1.5
    mocker.patch('backend.database.get_possible_match_offer_list', return_value=[(1, datetime.datetime(2024, 1, 9, 16, 11, 27), None, 1, 2, 200.0, 3, 0.5, 100.0, 0)])  # Możesz dostosować wartości zwracane do swojego testu
    mocker.patch('backend.database.add_match_offers', return_value=True)

    # When
    result = db.offer_match(offer_id, selled_currency_id, value, wanted_currency_id, exchange_rate)

    # Then
    assert result == [[50.0, 25.0]]  # Oczekuj odpowiedniego wyniku

def test_new_offer_with_match(mocker):
    # Given
    user_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 1.5
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.add_internal_transaction', return_value=True)
    mocker.patch('backend.database.add_new_offer', return_value=1)
    mocker.patch('backend.database.offer_match', return_value=[[50.0, 3]])  # Mozesz dostosować wartości zwracane do swojego testu

    # When
    result = db.new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)

    # Then
    assert result == [[50.0, 3]]  # Oczekuj odpowiedniego wyniku


def test_new_offer_without_match(mocker):
    # Given
    user_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 1.5
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.add_internal_transaction', return_value=True)
    mocker.patch('backend.database.add_new_offer', return_value=1)
    mocker.patch('backend.database.offer_match', return_value=[])

    # When
    result = db.new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)

    # Then
    assert result == []
