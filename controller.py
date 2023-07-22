from sql import SQLModel


class Controller:
    def __init__(self):
        # Инициализирует экземпляр класса модели SQLModel
        self.model = SQLModel()

    def test_connection(self, host, user, password, database):
        # Тестирует подключение к базе данных
        # Возвращает True, если подключение успешно, иначе False
        return self.model.connect_to_db(host, user, password, database)

    def get_all_tables(self):
        # Возвращает список всех таблиц в базе данных
        return self.model.get_all_tables()

    def get_table_data(self, table):
        # Возвращает все записи из указанной таблицы
        return self.model.get_table_data(table)

    def get_table_data_by_id(self, table, object_id):
        # Возвращает запись из указанной таблицы по id
        return self.model.get_table_data_by_id(table, object_id)

    def update_table_data(self, table, object_id, data):
        # Обновляет запись в указанной таблице по id, используя предоставленные данные
        return self.model.update_table_data(table, object_id, data)

    def get_columns(self, table_name):
        # Возвращает список имен столбцов в указанной таблице
        return self.model.get_columns(table_name)

    def load_excel_data_to_db(self, table_name, excel_file_path):
        # Загружает данные из файла Excel в указанную таблицу
        return self.model.load_excel_data_to_db(table_name, excel_file_path)

    def calculate_defect_rate(self, batch_id):
        # Рассчитывает процент дефектности для указанной партии
        return self.model.calculate_defect_rate(batch_id)
