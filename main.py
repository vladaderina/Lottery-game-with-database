import random
import sqlite3
import hashlib
import random
import re

def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()

co = sqlite3.connect("1задание.db")
con = sqlite3.connect("python.db") #подключаемся к БД
cursor = con.cursor() #устанавливаем курсор

# создаем таблицу people
cursor.executescript(""" 
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30),
                age INTEGER(3), 
                balance INTEGER NOT NULL DEFAULT 2000, 
                login VARCHAR(15),
                password VARCHAR(20)
                );
                
                CREATE TABLE IF NOT EXISTS lottery(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50),
                description TEXT(300),
                balance BIGINT NOT NULL DEFAULT 10000
                );
                
                """)
def registration():
    name = input("Name: ")
    age = int(input("Age: "))
    regularExpression = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+'
    login = input("LOGIN: ")
    isMatch = re.match(regularExpression, login)
    if isMatch:
        print("ОК")
    else:
        print("НЕ ОК")
    password = input("PASSWORD: ")

    try:
        con = sqlite3.connect("python.db")  # подключаемся к БД
        cursor = con.cursor()  # устанавливаем курсор

        con.create_function("md5", 1, md5sum)

        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            values = [name, age, login, password]
            cursor.execute("INSERT INTO users(name, age, login, password) "
                           "VALUES (?, ?, ?, md5(?))", values)
            con.commit()
        else:
            print("Такой логин уже существует")
            registration()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        con.commit()
        cursor.close()
        con.close()

def log_in():
    login = input("Login: ")
    password = input("Password: ")

    try:
        con = sqlite3.connect("python.db")  # подключаемся к БД
        cursor = con.cursor()  # устанавливаем курсор
        con.create_function("md5", 1, md5sum)

        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            print("Такого логина не существует")
        else:
            cursor.execute("SELECT password FROM users WHERE login = ? AND password = md5(?)",
                           [login, password])
            if cursor.fetchone() is None:
                print("Пароль неверный!")
            else:
                play_lottery(login)
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        con.commit()
        cursor.close()
        con.close()
def play_lottery(login):
    print("ЛОТЕРЕЯ")
    con = sqlite3.connect("python.db")  # подключаемся к БД
    cursor = con.cursor()  # устанавливаем курсор
    cursor.execute("SELECT age FROM users WHERE login = ? AND age >= ?",
                   [login, 18])
    try:
        if cursor.fetchone() is None:
            print("Вам недостаточно лет!")
        else:
            bet = int(input("Ваша ставка: "))
            number = random.randint(1, 10)
            balance = cursor.execute("SELECT balance FROM users WHERE login = ?",
                                     [login]).fetchone()[0]
            if balance < bet or balance <= 0:
                print("Мало денег")
            else:
                if number < 50:
                    cursor.execute("UPDATE users SET balance = balance - ? WHERE login = ?",
                                   [bet, login])
                    cursor.execute("UPDATE lottery SET balance = balance + ?",
                                   [bet])
                    print("Вы проиграли(")
                else:
                    cursor.execute("UPDATE users SET balance = balance + ? WHERE login = ?",
                                   [bet, login])
                    cursor.execute("UPDATE lottery SET balance = balance - ?",
                                   [bet])
                    print("Вы выиграли")
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        con.commit()
        cursor.close()
        con.close()
registration()
log_in()
