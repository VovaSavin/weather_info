import pymysql
import pymysql.cursors
from parsing import take_info_weather


# Ввод имени пользователя для подключения к БД
username = input("Enter username: ")
# Ввод пароля пользователя для подключения к БД
passwordDB = input("Enter password: ")


def create_table(connection: pymysql.Connection, data_list: list):
    """
    Создаёт таблицу и вставляет начальные данные.
    Принимает, в качестве аргументов, соединение с БД и список данных о погоде.
    Если таблица уже существует, то обновляет данные и добавляет новые.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE weather(
                    id int AUTO_INCREMENT PRIMARY KEY,
                    date DATE,
                    temperature int,
                    weather_description TEXT
                );
                """
            )
            print("Таблица данных создана...")
            insert_sq = """INSERT INTO weather (date, temperature, weather_description) VALUES (%s, %s, %s);"""
            cursor.executemany(insert_sq, data_list)
            connection.commit()
            print("Данные добавлены...")
    except pymysql.err.OperationalError:
        with connection.cursor() as cursor:
            insert_sq = """INSERT INTO weather (date, temperature, weather_description) VALUES (%s, %s, %s);"""
            cursor.execute(insert_sq, data_list[-1])
            update_sq = """UPDATE weather SET temperature=%s, weather_description=%s WHERE date=%s;"""
            for x in range(len(data_list)-1):
                cursor.execute(
                    update_sq, (
                        data_list[x][1],
                        data_list[x][2],
                        data_list[x][0],
                    )
                )
            connection.commit()
            print("Данные обновлены...")


def create_db():
    """
    Создаёт БД и вызывает метод create_table для записи данных.
    Если база данных уже существует, то вызывает метод create_table.
    """
    connect = pymysql.connect(host="127.0.0.1", user=username,
                              password=passwordDB)
    try:
        with connect.cursor() as cursor:
            cursor.execute(
                """CREATE DATABASE weatherDB;"""
            )
            print("База данных создана...")
        new_connect = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user=username,
            password=passwordDB,
            database="weatherDB",
            cursorclass=pymysql.cursors.DictCursor
        )
        create_table(new_connect, take_info_weather())
        connect.commit()
    except pymysql.err.ProgrammingError:
        new_connect = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user=username,
            password=passwordDB,
            database="weatherDB",
            cursorclass=pymysql.cursors.DictCursor
        )
        create_table(new_connect, take_info_weather())
    finally:
        connect.close()
        print("Соединение закрыто...")


def main():
    create_db()
