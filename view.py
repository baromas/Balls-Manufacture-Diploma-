import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox


# Этот класс реализует GUI (графический пользовательский интерфейс) приложения с использованием библиотеки Tkinter
class View:
    def __init__(self, controller):
        self.friction = None
        self.roundness = None
        self.edit_window = None
        self.table_for_id = None
        self.tables_frame = None
        self.load_button = None
        self.table_window = None
        self.main_frame = None
        self.db_button = None
        self.submit_button = None
        self.database_entry = None
        self.password_entry = None
        self.user_entry = None
        self.host_entry = None
        self.connect_window = None
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Quality Control System")
        self.root.geometry("800x600")
        self.create_widgets()

        # Метод для создания основных виджетов главного окна

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.db_button = tk.Button(self.main_frame, text="Connect to DB", command=self.create_connect_window)
        self.db_button.pack(padx=10, pady=10)
        self.load_button = tk.Button(self.main_frame, text='Insert data from .xlsx',
                                     command=self.insert_data_from_excel, state=tk.DISABLED)
        self.load_button.pack()
        self.roundness = tk.Button(self.main_frame, text="Roundness Test", command=self.create_connect_window)
        self.roundness.pack(padx=10, pady=10)
        self.friction = tk.Button(self.main_frame, text="Friction Rate", command=self.create_connect_window)
        self.friction.pack(padx=10, pady=10)
        self.tables_frame = tk.Frame(self.main_frame)
        self.tables_frame.pack()

    # Метод для создания вспомогательного окна подключения к базе данных
    def create_connect_window(self):
        self.connect_window = tk.Toplevel(self.root)
        self.connect_window.geometry("250x370")
        self.connect_window.title("MySQL Connection")

        self.host_entry, self.user_entry, self.password_entry, self.database_entry = self.create_connect_entries()

        self.submit_button = tk.Button(self.connect_window, text="Connect", command=self.test_connection)
        self.submit_button.pack()

    # Метод для создания полей ввода в окне подключения к базе данных
    def create_connect_entries(self):
        host_label = tk.Label(self.connect_window, text="Host:")
        host_label.pack(pady=10)
        host_entry = tk.Entry(self.connect_window)
        host_entry.pack(pady=10)

        user_label = tk.Label(self.connect_window, text="User:")
        user_label.pack(pady=10)
        user_entry = tk.Entry(self.connect_window)
        user_entry.pack(pady=10)

        password_label = tk.Label(self.connect_window, text="Password:")
        password_label.pack(pady=10)
        password_entry = tk.Entry(self.connect_window, show='*')
        password_entry.pack(pady=10)

        database_label = tk.Label(self.connect_window, text="Database:")
        database_label.pack(pady=10)
        database_entry = tk.Entry(self.connect_window)
        database_entry.pack(pady=10)

        return host_entry, user_entry, password_entry, database_entry

    # Метод для тестирования подключения к базе данных
    def test_connection(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        result = self.controller.test_connection(host, user, password, database)

        if result is True:
            messagebox.showinfo("Success", "Connection successful")
            self.connect_window.destroy()
            self.db_button.config(text="Reconnect")
            self.load_button.config(state=tk.ACTIVE)
            self.update_table_buttons()
        else:
            messagebox.showerror("Error", f"Failed connecting to database: {result}")

    # Метод для обновления списка кнопок таблиц после успешного подключения к базе данных
    def update_table_buttons(self):
        tables = self.controller.get_all_tables()

        for widget in self.tables_frame.winfo_children():
            widget.destroy()

        for table in tables:
            button = tk.Button(self.tables_frame, text=f"Show {table}",
                               command=lambda db_table=table: self.show_table(db_table))
            button.pack(pady=10)
        calculate_button = tk.Button(self.tables_frame, text="Calculate defect rate",
                                     command=self.calculate_defect_rate)
        calculate_button.pack(pady=10)

    # Метод для открытия вспомогательного окна расчета процента дефектов
    def calculate_defect_rate(self):
        calculate_window = tk.Toplevel(self.root)
        calculate_window.geometry("250x370")
        calculate_window.title("Calculate defect rate")
        batch_id_label = tk.Label(calculate_window, text="Batch ID:")
        batch_id_label.pack(pady=10)
        batch_id_entry = tk.Entry(calculate_window)
        batch_id_entry.pack(pady=10)
        apply_button = tk.Button(calculate_window, text="Apply",
                                 command=lambda: View.show_defect_rate(
                                     self.controller.calculate_defect_rate(batch_id_entry.get())[0][0]
                                 ))
        apply_button.pack(pady=10)

    # Статический метод для отображения процента дефектов
    @staticmethod
    def show_defect_rate(defect_rate):
        messagebox.showinfo("Defect rate", f"Defect rate is {defect_rate}")

    # Метод для отображения выбранной таблицы в новом окне
    def show_table(self, table):
        columns = self.controller.get_columns(table)
        data = self.controller.get_table_data(table)
        self.table_window = tk.Toplevel(self.root)
        self.table_window.title(table)
        self.table_window.geometry("920x640")
        self.table_for_id = table
        # Создание меток для названий столбцов
        for i, column_name in enumerate(columns):
            label = tk.Label(self.table_window, text=column_name)
            label.grid(row=0, column=i)

        # Отображение данных
        for i, row in enumerate(data, start=1):  # начинаем с 1, чтобы оставить место для названий столбцов
            for j, value in enumerate(row):
                table = tk.Text(self.table_window, height=1.5, width=20)
                table.grid(row=i, column=j)
                table.insert(tk.END, str(value))
                edit_button = tk.Button(self.table_window, text='Edit',
                                        command=lambda num=i,
                                                       db_table=table: self.edit_data(j, db_table))
                edit_button.grid(row=i, column=len(row))

    # Метод для открытия окна редактирования выбранного объекта из таблицы
    def edit_data(self, object_id, table_name):
        table_name = self.table_for_id
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title(f'Edit {table_name} row {object_id}')
        self.edit_window.geometry("200x150")
        data = self.controller.get_table_data_by_id(table_name, object_id)
        entries = {}

        for i, (column, value) in enumerate(data.items()):
            label = tk.Label(self.edit_window, text=column)
            label.grid(row=i, column=0)
            entry = tk.Entry(self.edit_window)
            entry.insert(tk.END, str(value))
            entry.grid(row=i, column=1)
            entries[column] = entry

        save_button = tk.Button(self.edit_window, text='Save',
                                command=lambda: (self.controller.update_table_data(table_name, object_id,
                                                                                   {column: e.get() for column, e in
                                                                                    entries.items()}),
                                                 self.table_window.destroy(),
                                                 self.edit_window.destroy(),
                                                 self.show_table(table_name)))
        save_button.grid(row=len(data), column=0)

    # Метод для загрузки данных из файла Excel в выбранную таблицу базы данных
    def insert_data_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if not file_path:
            return
        table_name = simpledialog.askstring("Input", "Enter the table name")
        if not table_name:
            return
        self.controller.load_excel_data_to_db(table_name, file_path)
        self.show_table(table_name)

    # Метод для запуска главного цикла Tkinter
    def run(self):
        self.root.mainloop()
