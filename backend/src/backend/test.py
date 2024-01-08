import pytest
from pytest_mock import mocker
from unittest.mock import patch
from backend.database import login, add_new_offer

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


# add offer

def test_add_new_offer():
    user_id = 1
    selled_currency_id = 2
    value = 100.0
    wanted_currency_id = 3
    exchange_rate = 4.5

    with patch("backend.database.mysql.connector.connect") as mock_connect:
        # Ustawienie symulowanych wyników
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (123,)  # Symulowany wynik z procedury

        # Wywołanie funkcji i sprawdzenie wyniku
        result = add_new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)

        assert result == 123
        # Sprawdzenie, czy metoda cursor.callproc została wywołana z odpowiednimi parametrami
        mock_cursor.callproc.assert_called_once_with(
            'add_offer', (user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
        )
        # Sprawdzenie, czy metoda cursor.execute została wywołana z odpowiednim zapytaniem
        mock_cursor.execute.assert_called_once_with("SELECT LAST_INSERT_ID()")
        # Sprawdzenie, czy metoda commit została wywołana
        mock_connect.return_value.commit.assert_called_once()

    # Sprawdzenie, czy metoda close została wywołana na połączeniu
    mock_connect.return_value.close.assert_called_once()

def test_add_new_offer_error(mocker):
    mocker.patch('backend.database.mysql.connector.connect')
    mock_cursor = mocker.patch('backend.database.mysql.connector.connect.return_value.cursor.return_value')
    mock_cursor.execute.side_effect = Exception('Database error')
        # Wywołanie funkcji i sprawdzenie, czy oczekiwany wyjątek został rzucony
    with pytest.raises(Exception, match='Database error'):
        add_new_offer(1, 2, 100.0, 3, 4.5)


