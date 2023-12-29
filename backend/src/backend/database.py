import mysql.connector

# Ustawienia połączenia
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '*****',
    'database': 'kantor',
}
# db_config = {
#     'host': 'localhost:4000',
#     'user': 'root',
#     'password': 'root',
#     'database': 'kantor',
# }


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
        args = (email, password)
        cursor.execute(f"SELECT user_login({', '.join('%s' for _ in args)})", args)

        # Pobierz wyniki
        result = cursor.fetchone()
        print(result[0])
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    finally:
        # Zamknij kursor i połączenie
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()