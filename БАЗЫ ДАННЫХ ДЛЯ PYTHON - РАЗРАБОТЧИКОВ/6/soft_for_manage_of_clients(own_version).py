import psycopg2

def create_db(conn):
    """
    Создает таблицы clients и phones, если они не существуют.
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
                phone_number VARCHAR(20) UNIQUE
            );
        """)
    conn.commit()
    print("База данных и таблицы созданы.")

def add_client(conn, first_name, last_name, email, phones=None):
    """
    Добавляет нового клиента.
    """
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO clients (first_name, last_name, email)
                VALUES (%s, %s, %s) RETURNING client_id;
            """, (first_name, last_name, email))
            client_id = cur.fetchone()[0]
            if phones:
                add_phone(conn, client_id, phones)
            conn.commit()
            print(f"Клиент {first_name} {last_name} добавлен с ID: {client_id}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print("Ошибка: Клиент с таким email уже существует.")

def add_phone(conn, client_id, phone):
    """
    Добавляет телефон для существующего клиента.
    Можно передать один номер или список номеров.
    """
    with conn.cursor() as cur:
        if isinstance(phone, list):
            for num in phone:
                try:
                    cur.execute("""
                        INSERT INTO phones (client_id, phone_number)
                        VALUES (%s, %s);
                    """, (client_id, num))
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    print(f"Ошибка: Номер {num} уже существует.")
        else:
            try:
                cur.execute("""
                    INSERT INTO phones (client_id, phone_number)
                    VALUES (%s, %s);
                """, (client_id, phone))
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                print(f"Ошибка: Номер {phone} уже существует.")
    conn.commit()
    print("Телефоны добавлены.")

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    """
    Изменяет данные о клиенте.
    """
    with conn.cursor() as cur:
        try:
            update_fields = []
            update_values = []
            if first_name is not None:
                update_fields.append("first_name = %s")
                update_values.append(first_name)
            if last_name is not None:
                update_fields.append("last_name = %s")
                update_values.append(last_name)
            if email is not None:
                update_fields.append("email = %s")
                update_values.append(email)

            if update_fields:
                update_values.append(client_id)
                query = f"UPDATE clients SET {', '.join(update_fields)} WHERE client_id = %s;"
                cur.execute(query, tuple(update_values))
                conn.commit()
                print(f"Данные клиента с ID {client_id} изменены.")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print("Ошибка: Клиент с таким email уже существует.")

def delete_phone(conn, client_id, phone):
    """
    Удаляет телефон для существующего клиента.
    """
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones
            WHERE client_id = %s AND phone_number = %s;
        """, (client_id, phone))
    conn.commit()
    print(f"Номер {phone} для клиента с ID {client_id} удалён.")

def delete_client(conn, client_id):
    """
    Удаляет клиента и все его телефоны.
    """
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients
            WHERE client_id = %s;
        """, (client_id,))
    conn.commit()
    print(f"Клиент с ID {client_id} и все его телефоны удалены.")

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    """
    Ищет клиента по заданным данным.
    """
    with conn.cursor() as cur:
        query_parts = []
        query_values = []
        
        if first_name:
            query_parts.append("first_name = %s")
            query_values.append(first_name)
        if last_name:
            query_parts.append("last_name = %s")
            query_values.append(last_name)
        if email:
            query_parts.append("email = %s")
            query_values.append(email)
        
        if phone:
            cur.execute("""
                SELECT client_id FROM phones WHERE phone_number = %s;
            """, (phone,))
            result = cur.fetchone()
            if result:
                client_id_from_phone = result[0]
                query_parts.append("client_id = %s")
                query_values.append(client_id_from_phone)

        if not query_parts:
            print("Укажите хотя бы один параметр для поиска.")
            return

        final_query = "SELECT * FROM clients WHERE " + " AND ".join(query_parts) + ";"
        cur.execute(final_query, tuple(query_values))
        
        clients = cur.fetchall()
        
        if clients:
            print("Найдены следующие клиенты:")
            for client in clients:
                cur.execute("SELECT phone_number FROM phones WHERE client_id = %s;", (client[0],))
                phones = [row[0] for row in cur.fetchall()]
                print(f"ID: {client[0]}, Имя: {client[1]}, Фамилия: {client[2]}, Email: {client[3]}, Телефоны: {phones}")
        else:
            print("Клиенты не найдены.")

def get_client_id_by_email(conn, email):
    """
    Вспомогательная функция для получения ID клиента по email.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT client_id FROM clients WHERE email = %s;", (email,))
        result = cur.fetchone()
        return result[0] if result else None

# --- Код, демонстрирующий работу всех функций ---
if __name__ == '__main__':
    try:
        with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
            # Создание структуры БД
            create_db(conn)

            print("\n--- Добавление клиентов ---")
            add_client(conn, "Иван", "Петров", "ivan@example.com", ["+79001234567"])
            add_client(conn, "Мария", "Иванова", "maria@example.com")
            add_client(conn, "Сергей", "Козлов", "sergey@example.com")

            print("\n--- Добавление телефона ---")
            ivan_id = get_client_id_by_email(conn, "ivan@example.com")
            if ivan_id:
                add_phone(conn, ivan_id, "+79009876543")

            print("\n--- Изменение данных клиента ---")
            maria_id = get_client_id_by_email(conn, "maria@example.com")
            if maria_id:
                change_client(conn, maria_id, last_name="Смирнова", email="maria_smirnova@example.com")

            print("\n--- Поиск клиентов ---")
            find_client(conn, first_name="Иван")
            find_client(conn, email="sergey@example.com")
            find_client(conn, phone="+79001234567")

            print("\n--- Удаление телефона ---")
            ivan_id_updated = get_client_id_by_email(conn, "ivan@example.com")
            if ivan_id_updated:
                delete_phone(conn, ivan_id_updated, "+79009876543")

            print("\n--- Поиск после удаления телефона ---")
            find_client(conn, first_name="Иван")

            print("\n--- Удаление клиента ---")
            sergey_id = get_client_id_by_email(conn, "sergey@example.com")
            if sergey_id:
                delete_client(conn, sergey_id)

            print("\n--- Поиск после удаления клиента ---")
            find_client(conn, email="sergey@example.com")

    except Exception as e:
        print(f"Ошибка подключения или выполнения: {e}")