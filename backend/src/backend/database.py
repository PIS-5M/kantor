import mysql.connector
import bcrypt
import math

# Ustawienia połączenia
db_config = {
    "host": "0.0.0.0",
    "user": "root",
    "password": "root",
    "database": "kantor",
}  # change password for correct


def registration(pass_hash, name, surname, mail):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc("user_registration", (pass_hash, name, surname, mail))
        cursor.execute("COMMIT;")
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def login(email, password):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Wywołaj funkcję
        args = (email,)
        cursor.execute(f"SELECT password, user_id from user where email=%s", args)

        # Pobierz wyniki
        result = cursor.fetchone()
        if result and bcrypt.checkpw(
            password.encode("utf-8"), result[0].encode("utf-8")
        ):
            return result[1]
        else:
            # złe hasło
            return None
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def email_used(email):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Wywołaj funkcję
        args = (email,)
        cursor.execute(f"SELECT user_id from user where email=%s", args)

        # Pobierz wyniki
        result = cursor.fetchall()
        if result:
            return True
        else:
            # email nie jest zajęty
            return False
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def get_all_currency():
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Wywołaj funkcję
        cursor.execute(f"select * from currency;")

        # Pobierz wyniki
        currency = cursor.fetchall()
        return currency
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()

def new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    trans_value = -value
    add_internal_transaction(user_id, selled_currency_id, trans_value)
    offer_id = add_new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
    reverse_exchange_rate = math.floor(1 / exchange_rate * 100) / 100
    print(reverse_exchange_rate)
    offer_match(offer_id, selled_currency_id, value, wanted_currency_id, reverse_exchange_rate)

def offer_match(offer_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    offer_list = get_offer_list(selled_currency_id, wanted_currency_id, exchange_rate)
    print(offer_list)
    remaining_value = value
    match_list = []
    while remaining_value > 0 and offer_list:
        best_offer = min(offer_list, key=lambda x: (x[7], x[2]))
        offer_list.remove(best_offer)
        match_wanted_money = math.floor(best_offer[5] * best_offer[7] * 100 ) / 100
        print((best_offer[0], best_offer[5], offer_id, match_wanted_money))
        if match_wanted_money <= remaining_value:
            print(1)
            add_match_offers(best_offer[0], best_offer[5], offer_id, match_wanted_money)
            remaining_value -= match_wanted_money
            match_list.append([match_wanted_money, best_offer[5]]) # [kwota sprzedana (ile chce zmaczowany), kwota kupiona(ile wystawił zmaczowany)]
        else:
            print(2)
            reverse_exchange_rate = math.floor(1 / exchange_rate * 100) / 100
            match_money = math.floor(reverse_exchange_rate * remaining_value * 100) / 100
            add_match_offers(best_offer[0], match_money, offer_id, remaining_value)
            match_list.append([remaining_value, match_money]) # [kwota sprzedana (ile mam zostało), kwota kupiona (ile płaci zmaczowany)]
            remaining_value = 0
    return match_list

def add_match_offers(earlier_offer_id, earlier_value, later_offer_id, later_value):
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        cursor.callproc('match_offers', (earlier_offer_id, later_offer_id, earlier_value, later_value))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def get_offer_list(selled_currency_id, wanted_currency_id, exchange_rate):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Pobierz wynik z procedury
        args = (wanted_currency_id, selled_currency_id, exchange_rate)
        cursor.execute(f"SELECT * from uncompleted_offers where publication_currency_id =%s and wanted_currency_id =%s and exchange_rate <= %s", args)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def add_new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc('add_offer', (user_id, selled_currency_id, value, wanted_currency_id, exchange_rate))

        # Pobierz wynik z procedury
        cursor.execute("SELECT LAST_INSERT_ID()")
        result = cursor.fetchone()
        conn.commit()
        return result[0]
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def add_internal_transaction(user_id, currency_id, value):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc('add_internal_transaction', (user_id, currency_id, value))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()