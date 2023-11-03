import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            res = self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS users
            (id integer PRIMARY KEY AUTOINCREMENT,
            chat_id BIGINT UNIQUE,
            name varchar, 
            path  varchar,
            points int,
            state int
            )
            ''')
            return res

    def post_result(self, *args):
        l = (args)
        keys = "(chat_id, name, path, points, state)"
        print(l)
        try:
            with self.connection:
                self.cursor.execute(f"INSERT INTO users {keys} VALUES {l}")
        except:
            new_l = (args[1:])
            string = ''
            res = keys[1:-1].split(", ")
            new_keys = (res[1:])
            for elem in new_keys:
                string += f'{elem}=?, '
            print(string[:-2])
            with self.connection:
                self.cursor.execute(f"UPDATE users SET {string[:-2]} WHERE chat_id={l[0]}", new_l)

