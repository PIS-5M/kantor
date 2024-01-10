import mysql.connector
import bcrypt

# Ustawienia polaczenia
db_config = {
    "host": "172.19.0.2",
    "user": "root",
    "password": "root",
    "database": "kantor",
}  # change password for correct


def registration(pass_hash, name, surname, mail):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc("user_registration", (pass_hash, name, surname, mail))
        cursor.execute("COMMIT;")
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def login(email, password):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Wywolaj funkcje
        args = (email,)
        cursor.execute(f"SELECT password_hash, user_id from user where email=%s", args)

        # Pobierz wyniki
        result = cursor.fetchone()
        if result and bcrypt.checkpw(
            password.encode("utf-8"), result[0].encode("utf-8")
        ):
            return result[1]
        else:
            # zle haslo
            return None
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def email_used(email):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Wywolaj funkcje
        args = (email,)
        cursor.execute(f"SELECT user_id from user where email=%s", args)

        # Pobierz wyniki
        result = cursor.fetchall()
        if result:
            return True
        else:
            # email nie jest zajety
            return False
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def get_all_currency():
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Wywolaj funkcje
        cursor.execute(f"select * from currency;")

        # Pobierz wyniki
        currency = cursor.fetchall()
        return currency
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()



def add_wallet(user_id, currency_id, account_number_hash):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Wywolaj funkcje
        # Sprawdz czy juz ma taki portfel
        args = (user_id, currency_id)
        cursor.execute(f"SELECT * from wallet where user_id=%s and currency_id=%s", args)

        # Pobierz wyniki
        result = cursor.fetchone()
        if not result:
            args = (user_id, currency_id, account_number_hash)
            cursor.execute(f"INSERT INTO `kantor`.`wallet` (`user_id`, `currency_id`, `account_number_hash`) VALUES (%s, %s, %s)", args)
            cursor.execute("COMMIT;")
            return True
        else:
            # juz ma
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()
