import mysql.connector
import bcrypt
import math

# Ustawienia polaczenia
db_config = {
    "host": "172.19.0.2",  # localhost
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


def get_user_data(id):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Wywołaj funkcję
        args = (id,)
        cursor.execute(f"SELECT name, surname, email from user where user_id=%s", args)

        # Pobierz wyniki
        result = cursor.fetchone()
        if result:
            print(result)
            return result
        else:
            # Użytkownik nie istnieje
            return None, None, None
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
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
        cursor.execute(
            f"SELECT * from wallet where user_id=%s and currency_id=%s", args
        )

        # Pobierz wyniki
        result = cursor.fetchone()
        if not result:
            args = (user_id, currency_id, account_number_hash)
            cursor.execute(
                f"INSERT INTO `kantor`.`wallet` (`user_id`, `currency_id`, `account_number_hash`) VALUES (%s, %s, %s)",
                args,
            )
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


def new_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    trans_value = -value
    add_internal_transaction(user_id, selled_currency_id, trans_value)
    offer_id = add_new_offer(
        user_id, selled_currency_id, value, wanted_currency_id, exchange_rate
    )
    reverse_exchange_rate = math.floor(1 / exchange_rate * 100) / 100
    print(reverse_exchange_rate)
    match_offer = offer_match(
        offer_id, selled_currency_id, value, wanted_currency_id, reverse_exchange_rate
    )
    return match_offer


def offer_match(offer_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    offer_list = get_possible_match_offer_list(
        selled_currency_id, wanted_currency_id, exchange_rate
    )
    remaining_value = value
    match_list = []
    while remaining_value > 0 and offer_list:
        best_offer = min(offer_list, key=lambda x: (x[7], x[2]))
        offer_list.remove(best_offer)
        match_wanted_money = math.floor(best_offer[8] * best_offer[7] * 100) / 100
        if match_wanted_money <= remaining_value:
            add_match_offers(best_offer[0], best_offer[8], offer_id, match_wanted_money)
            remaining_value -= match_wanted_money
            match_list.append(
                [match_wanted_money, best_offer[8]]
            )  # [kwota sprzedana (ile chce zmaczowany), kwota kupiona(ile wystawil zmaczowany)]
        else:
            reverse_exchange_rate = math.floor(1 / exchange_rate * 100) / 100
            match_money = (
                math.floor(reverse_exchange_rate * remaining_value * 100) / 100
            )
            add_match_offers(best_offer[0], match_money, offer_id, remaining_value)
            match_list.append(
                [remaining_value, match_money]
            )  # [kwota sprzedana (ile mam zostalo), kwota kupiona (ile placi zmaczowany)]
            remaining_value = 0
    return match_list


def add_match_offers(earlier_offer_id, earlier_value, later_offer_id, later_value):
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        cursor.callproc(
            "match_offers",
            (earlier_offer_id, later_offer_id, earlier_value, later_value),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def get_possible_match_offer_list(
    selled_currency_id, wanted_currency_id, exchange_rate
):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Pobierz wynik z procedury
        args = (wanted_currency_id, selled_currency_id, exchange_rate)
        cursor.execute(
            f"SELECT * from uncompleted_offers where publication_currency_id =%s and wanted_currency_id =%s and exchange_rate <= %s",
            args,
        )
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def add_new_offer(
    user_id, selled_currency_id, value, wanted_currency_id, exchange_rate
):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc(
            "add_offer",
            (user_id, selled_currency_id, value, wanted_currency_id, exchange_rate),
        )

        # Pobierz wynik z procedury
        cursor.execute("SELECT LAST_INSERT_ID()")
        result = cursor.fetchone()
        conn.commit()
        return result[0]
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def add_internal_transaction(user_id, currency_id, value):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        cursor.callproc("add_internal_transaction", (user_id, currency_id, value))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Blad: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def user_offers(seller_id):
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor(dictionary=True)
        query = (
            "SELECT "
            "   oh.offer_history_id, "
            "   oh.publication_date, "
            "   oh.last_modification_date, "
            "   oh.value, "
            "   c.currency_id, "
            "   c.abbreviation, "
            "   oh.wanted_currency_id, "
            "   oh.exchange_rate, "
            "   w.account_number_hash, "
            "   oh.is_cancelled "
            "FROM offer_history oh "
            "JOIN user u ON oh.seller_id = u.user_id "
            "JOIN currency c ON oh.publication_currency_id = c.currency_id "
            "JOIN wallet wa ON oh.seller_id = wa.user_id "
            "WHERE oh.seller_id = %s"
        )
        cursor.execute(query, (seller_id,))
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def get_wallet(user_id):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utwórz obiekt kursora
        cursor = conn.cursor()
        # Wywołaj funkcję
        args = (user_id,)
        cursor.execute(
            f"select f.currency_name, w.wallet_id, w.user_id, value_in_wallet, value_in_offer from money_in_wallet w join money_on_offer f on w.wallet_id = f.wallet_id where w.user_id = %s",
            args,
        )

        # Pobierz wyniki
        wallet = cursor.fetchall()
        print(wallet)
        return wallet
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


class DatabaseError(Exception):
    def __init__(self, message: str):
        self.message = message


def delete_offer(offer_id):
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        query = "DELETE FROM offer_history WHERE offer_history_id = %s"
        cursor.execute(query, (offer_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False  # Offer not found
        return True  # Offer found and deleted
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise DatabaseError(message="Database error occurred")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()

def wallet_add(wallet_id, value):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Wywolaj funkcje
        args = (wallet_id, value)
        cursor.execute(f"INSERT INTO `kantor`.`transaction` (`wallet_id`, value) VALUES (%s, %s);", args)
        cursor.execute("COMMIT;")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def get_transactions(id):
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        args = (id,)
        cursor.execute(
            f"select transaction_id, value, name, account_number_hash from transaction t join wallet w on t.wallet_id = w.wallet_id join currency c on w.currency_id = c.currency_id where w.user_id = %s",
            args,
        )

        result = cursor.fetchall()

        args = (id,)
        cursor.execute(
            f"select internal_transactions_id, value, name, account_number_hash from internal_transactions t join wallet w on t.wallet_id = w.wallet_id join currency c on w.currency_id = c.currency_id where w.user_id = %s",
            args,
        )

        result.extend(cursor.fetchall())
        end_data = []
        for data in result:
            end_data.append(
                {
                    "transaction_id": data[0],
                    "value": data[1],
                    "value_currency_name": data[2],
                    "bank_account": "1234567891234567",
                }
            )
        return end_data
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()

def wallet_subtract(wallet_id, value):
    conn = mysql.connector.connect(**db_config)
    try:
        # Utworz obiekt kursora
        cursor = conn.cursor()
        # Wywolaj funkcje
        args = (wallet_id,)
        cursor.execute(f"select value_in_wallet from money_in_wallet where wallet_id = %s", args)
        max_sum = cursor.fetchone()
        if value > max_sum[0]:
            return False

        args = (wallet_id, -value)
        cursor.execute(f"INSERT INTO `kantor`.`transaction` (`wallet_id`, value) VALUES (%s, %s);", args)
        cursor.execute("COMMIT;")
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Zamknij kursor i polaczenie
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()
