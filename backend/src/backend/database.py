import mysql.connector
import bcrypt
from db_config import db_config


def registration(pass_hash, name, surname, mail):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc('user_registration', (pass_hash, name, surname, mail))
        cursor.execute("COMMIT;")
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
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
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return result[1]
        else:
            # złe hasło
            return None
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def email_used(email):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Wywołaj funkcję
        args = (email, )
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
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
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
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
