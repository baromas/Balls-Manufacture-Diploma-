import mysql.connector
import pandas as pd


class DatabaseConnection:
    def __init__(self, host, user, password, database):
        """
        Конструктор класса DatabaseConnection. Инициализирует параметры подключения к базе данных.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def __enter__(self):
        """
        Открывает соединение с базой данных при входе в контекст.
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрывает соединение с базой данных при выходе из контекста.
        """
        if self.connection:
            self.connection.close()


class SQLModel:
    """
    Класс для работы с базой данных MySQL.
    """
    host = "127.0.0.1"
    user = "root"
    password = "1"
    database = "ballsmanufacture"
    port = 3306

    @staticmethod
    def connect_to_db(host, user, password, database):
        """
        Статический метод для проверки соединения с базой данных.
        """
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1" or input(),
                user="root" or input(),
                password="1" or input(),
                database="ballsmanufacture" or input(),
                port=3306,
            )
            conn.close()
            return True
        except mysql.connector.Error as err:
            return err

    def get_primary_key(self, table):
        """
        Получает имя первичного ключа указанной таблицы.
        """
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
            primary_key_column = cursor.fetchone()[4]
        return primary_key_column

    def get_all_tables(self):
        """
        Получает все таблицы в базе данных.
        """
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                data = cursor.fetchall()
                tables = [table[0] for table in data]
                return tables

    def get_table_data(self, table):
        """
        Получает все данные из указанной таблицы.
        """
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table}")
                data = cursor.fetchall()
                return data

    def calculate_defect_rate(self, batch_id):
        """
        Вызывает хранимую процедуру CalculateDefectRate в базе данных с указанным batch_id.
        """
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"CALL CalculateDefectRate({batch_id})")
                result = cursor.fetchall()
                return result

    def get_columns(self, table):
        """
        Получает все колонки указанной таблицы.
        """
        # Проверка имени таблицы
        if not table.isidentifier():
            raise ValueError(f"Некорректное имя таблицы: {table}")

        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SHOW COLUMNS FROM {table}')
            columns = [column[0] for column in cursor.fetchall()]
        return columns

    def get_table_data_by_id(self, table, object_id):
        """
        Получает данные из указанной таблицы по ID.
        """
        primary_key = self.get_primary_key(table)
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f'SELECT * FROM {table} WHERE {primary_key} = {object_id}')
            result = cursor.fetchone()
        return result

    def update_table_data(self, table, object_id, data):
        """
        Обновляет данные в указанной таблице по ID.
        """
        primary_key = self.get_primary_key(table)
        columns = [column for column in self.get_columns(table) if column in data]
        query = 'UPDATE {} SET '.format(table)
        query += ', '.join(['{} = %s'.format(column) for column in columns])
        query += ' WHERE {} = %s'.format(primary_key)
        values = [data[column] for column in columns] + [object_id]
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(values))
            conn.commit()

    def load_excel_data_to_db(self, table_name, excel_file_path):
        df = pd.read_excel(excel_file_path)
        data = df.to_dict(orient='records')
        with DatabaseConnection(self.host, self.user, self.password, self.database) as conn:
            cursor = conn.cursor()
            columns = data[0].keys()
            for row_data in data:
                query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(columns))})'
                cursor.execute(query, list(row_data.values()))
            conn.commit()
