import sqlite3


class Database:
    def __init__(self, database_name: str):
        self.name = database_name
        self.func = {
            "simple_search": self.simple_search,
            "simple_delete": self.simple_delete,
            "simple_set": self.simple_set,
            "add_new_user": self.add_new_user,
            "like": self.like,
            "sub": self.sub,
            "comment": self.comment,
            "review": self.review,
            "insert": self.insert,
            "post": self.post
        }

    def simple_search(self, table_name: str, condition: str):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        operation = "select * from {} where {}".format(table_name, condition)
        print(operation)
        data = c.execute(operation).fetchall()
        print('search', data)
        conn.commit()
        conn.close()
        return data

    def simple_delete(self, table_name, condition):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        operation = "delete from {} where {}".format(table_name, condition)
        print(operation)
        data = c.execute(operation).fetchall()
        conn.commit()
        conn.close()
        return data

    def simple_set(self, table_name, condition, col_name, value):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        operation = "UPDATE {} SET {} = {} WHERE {}".format(table_name, col_name, value, condition)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()

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

    def like(self, table_name, data):
        sub_id = str(data["sub_id"])
        user_id = str(data["user_id"])
        time = "DATETIME(\"now\")"
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        headers = "sub_id, user_id, time_liked"
        values = ", ".join([sub_id, user_id, time])
        operation = "INSERT INTO {} ({}) VALUES ({})".format(table_name, headers, values)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()

    def sub(self, data):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        headers = "id, poster_id, time_posted, publicity, likes, dislikes, comments"
        values = ", ".join(
            [data["id"], data["poster_id"], "DATETIME(\"now\")", data["publicity"], data["likes"], data["dislikes"],
             data["comments"]])
        operation = "INSERT INTO Sub ({}) VALUES ({})".format(headers, values)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()

    def comment(self, data):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        headers = "id, original_id, content, seen"
        quotation = lambda x: "\"" + x + "\""
        values = ", ".join([data["id"], data["parent_id"], quotation(data["content"])]) + ", " + '0'
        operation = "INSERT INTO Comments ({}) VALUES ({})".format(headers, values)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()

    def review(self, data):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        headers = "id, user_id, course_id, content, rating, anonymous, seen, quality"
        quotation = lambda x: "\"" + x + "\""
        values = ", ".join(
            [data["id"], data["user_id"], data["course_id"], quotation(data["content"]), data["rating"]]) + ", 0, 1, 0"
        operation = "INSERT INTO Review ({}) VALUES ({})".format(headers, values)
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

    # new functions
    def post(self, data):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        headers = "id, content"
        quotation = lambda x: "\"" + x + "\""
        values = ", ".join([data["id"], quotation(data["content"])])
        operation = "INSERT INTO Post ({}) VALUES ({})".format(headers, values)
        print(operation)
        c.execute(operation)
        conn.commit()
        conn.close()
