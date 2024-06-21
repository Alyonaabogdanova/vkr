import sqlite3

conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

# Создание таблицы клиентов
c.execute('''CREATE TABLE IF NOT EXISTS clients (
                fio TEXT,
                phone TEXT,
                birth_date TEXT,
                login TEXT,
                password TEXT)''')

# Создание таблицы товаров
c.execute('''CREATE TABLE IF NOT EXISTS goods (
                day text,
                name TEXT,
                quantity INTEGER,
                price integer)''')

# Создание таблицы расписания
c.execute('''CREATE TABLE IF NOT EXISTS schedule (
                day TEXT,
                time TEXT,
                activity TEXT)''')

#Создание таблицы продаж
c.execute('''CREATE TABLE IF NOT EXISTS sales (
                day TEXT,
                category Text,
                item TEXT,
                quantity INTEGER
                ,price Integer)''')
conn.commit()
conn.close()