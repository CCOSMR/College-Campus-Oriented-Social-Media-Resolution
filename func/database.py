import sqlite3
import logging


# def execute(database):
#     def decorator(func):
#         def wrapper(*args):
#             def core():
#                 conn = sqlite3.connect(database.name)
#                 c = conn.cursor()
#                 operation = func(*args)
#                 print(operation)
#                 result = c.execute(operation).fetchall()
#                 conn.commit()
#                 conn.close()
#                 return result
#
#             return core()
#
#         return wrapper
#
#     return decorator


def execute(func):
    def decorator(self, *args):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        operation = func(self, *args)
        logging.info(operation)
        if operation[:6].lower() == "select":
            result = c.execute(operation).fetchall()
        else:
            result = c.execute(operation)
        conn.commit()
        conn.close()
        return result

    return decorator


class Database:
    def __init__(self, database_name: str):
        self.name = database_name

    @execute
    def test(self, operation):
        return operation

    @execute
    def simple_search(self, table_name: str, condition: str):
        operation = "select * from {} where {};".format(table_name, condition)
        return operation

    @execute
    def add_new_user(self, data):
        table_name = "Users"
        headers = "id, password, email, name, time_joined"
        quotation = lambda x: "\"" + x + "\""
        values = str()
        for i in ["id", "password", "email", "name"]:
            values += quotation(data[i]) + ", "
        values += "DATETIME(\"now\")"
        operation = "INSERT INTO {} ({}) VALUES ({})".format(table_name, headers, values)
        return operation

    @execute
    def follow(self, following_id, follower_id):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()

    @execute
    def insert(self, table_name: str, data: dict):
        headers = ", ".join(data.keys())
        judge = lambda x: False if isinstance(x, str) else True
        quotation = lambda x: "\"" + x + "\""
        values = ", ".join([str(i) if judge(i) else quotation(i) for i in data.values()])
        operation = "INSERT INTO {} ({}) VALUES ({})".format(table_name, headers, values)
        return operation
