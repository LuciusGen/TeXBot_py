import sqlite3

conn = sqlite3.connect("database_new.db")
cursor = conn.cursor()

# названия таблиц
table_names = ["Группы.", "Линии_и_их_уравнения.", "Матрицы", "Многочлены.", "Опр-ли 2 и 3 пор-ка.", "Определители",
               "Поля.", "Преобразование координат.", "Прямая на плоскости.", "С-мы координат на пл-ти.",
               "СЛАУ", "Теория конических сечений."]

# Создание таблиц
conf_sql = "CREATE TABLE conf ( token TEXT DEFAULT NULL) "
cursor.execute(conf_sql)

for name in table_names:
    cursor.execute("CREATE TABLE `" + name + "` ( "
                                             "теоремы TEXT DEFAULT NULL, "
                                             "callback_data TEXT DEFAULT NULL, "
                                             "img TEXT DEFAULT NULL, "
                                             "tex TEXT DEFAULT NULL"
                                             ")")

