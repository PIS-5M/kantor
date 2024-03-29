import pytest
from pytest_mock import mocker
import backend.database as db
from unittest.mock import patch, Mock
import mysql.connector
import datetime
import math
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
        db.get_user_data(1)
        db.add_new_offer(1, 2, 100.0, 3, 4.5)

def test_add_internal_transaction_success():
    with patch("backend.database.mysql.connector.connect") as mock_connect:

        mock_cursor = mock_connect.return_value.cursor.return_value

        db.add_internal_transaction(1, 2, 100.0)

        mock_cursor.callproc.assert_called_once_with('add_internal_transaction', (1, 2, 100.0))
        mock_connect.return_value.commit.assert_called_once()

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
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = (1,)
    result = db.add_new_offer(1, 2, 100.0, 3, 1.5)
    assert result == 1

def test_add_new_offer_exception(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Some other error')
    with pytest.raises(Exception, match='Some other error'):
        db.add_new_offer(1, 2, 100.0, 3, 1.5)


def test_get_possible_match_offer_list_success(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchall.return_value = [(1, 'USD', 'EUR', 1.2, 100.0), (2, 'GBP', 'USD', 1.5, 150.0)]
    result = db.get_possible_match_offer_list(2, 1, 1.3)
    assert result == [(1, 'USD', 'EUR', 1.2, 100.0), (2, 'GBP', 'USD', 1.5, 150.0)]


def test_get_possible_match_offer_list_exception(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Some other error')
    with pytest.raises(Exception, match='Some other error'):
        db.get_possible_match_offer_list(2, 1, 1.3)

def test_add_match_offers_success(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.bcrypt.checkpw', return_value=True)

    result = db.add_match_offers(1, 10.0, 2, 8.0)

    assert result == True

def test_offer_match(mocker):
    offer_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 1.5
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.get_possible_match_offer_list', return_value=[(1, datetime.datetime(2024, 1, 9, 16, 11, 27), None, 1, 2, 50.0, 3, 1.86, 50.0, 0)])  # Możesz dostosować wartości zwracane do swojego testu
    mocker.patch('backend.database.add_match_offers', return_value=True)
    result = db.offer_match(offer_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
    assert result == [[93.0, 50.0]]

def test_offer_match_2(mocker):
    offer_id = 1
    selled_currency_id = 2
    value = 20.0
    wanted_currency_id = 3
    exchange_rate = 2.0
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.get_possible_match_offer_list', return_value=[(1, datetime.datetime(2024, 1, 9, 16, 11, 27), None, 1, 2, 200.0, 3, 0.5, 100.0, 0)])  # Możesz dostosować wartości zwracane do swojego testu
    mocker.patch('backend.database.add_match_offers', return_value=True)
    result = db.offer_match(offer_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
    assert result == [[20.0, 10.0]]

def test_new_offer_with_match(mocker):
    user_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 1.5
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.add_internal_transaction', return_value=True)
    mocker.patch('backend.database.add_new_offer', return_value=1)
    mocker.patch('backend.database.offer_match', return_value=[[50.0, 3]])
    result = db.new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
    assert result == [[50.0, 3]]


def test_new_offer_without_match(mocker):
    user_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 1.5
    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.add_internal_transaction', return_value=True)
    mocker.patch('backend.database.add_new_offer', return_value=1)
    mocker.patch('backend.database.offer_match', return_value=[])
    result = db.new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
    assert result == []


def test_add_wallet_success(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = None

    user_id = 1
    currency_id = 2
    account_number_hash = "hashed_account_number"

    result = db.add_wallet(user_id, currency_id, account_number_hash)

    assert result is True


def test_add_wallet_already_exist(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ['wallet']

    user_id = 1
    currency_id = 2
    account_number_hash = "hashed_account_number"

    result = db.add_wallet(user_id, currency_id, account_number_hash)

    assert result is False


def test_add_wallet_database_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    user_id = 1
    currency_id = 2
    account_number_hash = "hashed_account_number"

    with pytest.raises(Exception, match='Database error'):
        db.add_wallet(user_id, currency_id, account_number_hash)

def test_delete_offer_success(mocker):

    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value.rowcount', return_value=1)

    offer_id = 123
    result = db.delete_offer(offer_id)

    assert result is True


def test_user_offers_success(mocker):

    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = {
        "offer_history_id": 1,
        "publication_date": "2022-01-09T12:00:00",
        "last_modification_date": "2022-01-10T08:30:00",
        "value": 100.0,
        "currency": {
            "currency_id": 1,
            "abbreviation": "USD",
        },
        "wanted_currency_id": {
            "currency_id": 2,
            "abbreviation": "EUR",
        },
        "exchange_rate": 1.5,
        "account_number_hash": '12345678901234567890123456',
        "status": "Active"
    }

    result = db.user_offers(1)

    assert result == {
        "offer_history_id": 1,
        "publication_date": "2022-01-09T12:00:00",
        "last_modification_date": "2022-01-10T08:30:00",
        "value": 100.0,
        "currency": {
            "currency_id": 1,
            "abbreviation": "USD",
        },
        "wanted_currency_id": {
            "currency_id": 2,
            "abbreviation": "EUR",
        },
        "exchange_rate": 1.5,
        "account_number_hash": '12345678901234567890123456',
        "status": "Active"
    }

def test_user_offers_not_found(mocker):

    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = None

    result = db.user_offers(1)

    assert result is None

def test_user_offers_database_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception("Database error")


    with pytest.raises(Exception, match='Database error'):
        db.user_offers(1)

def test_delete_offer_not_found(mocker):

    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchone.return_value = ()

    offer_id = 123
    result = db.delete_offer(offer_id)

    assert result is True

def test_delete_offer_database_error(mocker):

    mocker.patch('backend.database.mysql.connector.connect')
    mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value.execute.side_effect', db.DatabaseError("Database error occurred"))

    offer_id = 123
    with pytest.raises(db.DatabaseError, match="Database error occurred"):
        db.delete_offer(offer_id)

def test_get_wallet(mocker):
    # Mock the cursor and execute method
    fake_results = [('USD', 1, 123, 500.0, 1000.0)]
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchall.return_value = fake_results
    # Przygotowanie danych testowych
    user_id = 1

    # Wywołanie funkcji
    result = db.get_wallet(user_id)

    assert result == fake_results


def test_get_wallet_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        db.get_wallet(1)


def test_get_transactions(mocker):
    # Mock the cursor and execute method
    transactions = [
        (1, -100.00, "USD", "1234567891234567")
    ]
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchall.return_value = transactions
    # Przygotowanie danych testowych
    fake_results = [
        {
            "transaction_id": 1,
            "value": -100.00,
            "value_currency_name": "USD",
            "bank_account": "1234567891234567",
        },
        {
            "transaction_id": 1,
            "value": -100.00,
            "value_currency_name": "USD",
            "bank_account": "1234567891234567",
        },
    ]

    # Wywołanie funkcji
    result = db.get_transactions(1)

    assert result == fake_results


def test_get_transactions_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        db.get_transactions(1)


def test_registration(mocker):
    # Mock the cursor and execute method
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.fetchall.return_value = ()

    # Wywołanie funkcji
    result = db.registration("pass_hash", "name", "surname", "mail")



def test_registration_error(mocker):
    # Mock the cursor and execute method to raise an exception
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')

    with pytest.raises(Exception, match='Database error'):
        result = db.registration("pass_hash", "name", "surname", "mail")


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
