import sqlite3


class Database:
    def __init__(self, database_name: str):
        self.name = database_name

    def simple_search(self, table_name: str, condition: str):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        operation = "select * from {} where {}".format(table_name, condition)
        print(operation)
        data = c.execute(operation).fetchall()
        conn.commit()
        conn.close()
        return data

    def add_new_user(self, data):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        table_name = "Users"
        headers = "id, password, email, name, time_joined"
        judge = lambda x: False if isinstance(x, str) else True
        quotation = lambda x: "\"" + x + "\""
        values = str()
        for i in ["id", "password", "email", "name"]:
            values += quotation(data[i]) + ", "
        values += "DATETIME(\"now\")"
        operation = "INSERT INTO {} ({}) VALUES ({})".format(table_name, headers, values)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()

    def insert(self, table_name: str, data: dict):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        headers = ", ".join(data.keys())
        judge = lambda x: False if isinstance(x, str) else True
        quotation = lambda x: "\"" + x + "\""
        values = ", ".join([str(i) if judge(i) else quotation(i) for i in data.values()])
        operation = "INSERT INTO {} ({}) VALUES ({})".format(table_name, headers, values)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()
