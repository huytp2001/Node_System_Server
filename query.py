import sqlite3
from datetime import datetime

class Node:
    def __init__(self):
        self.create_node_table()

    def create_node_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                id INTEGER PRIMARY KEY,
                node_id TEXT UNIQUE NOT NULL CHECK(LENGTH(node_id) <= 16),
                name TEXT UNIQUE NOT NULL CHECK(LENGTH(name) <= 16),
                soil INTEGER NOT NULL,
                up_time DATETIME NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_node(self, node_id, node_name, soil) -> int:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        current_time = datetime.now()
        time = current_time.strftime("%H:%M %d-%m")
        code = 0
        try:
            c.execute(f'''
                INSERT INTO nodes (node_id, name, soil, up_time) VALUES ('{node_id}','{node_name}','{soil}','{time}')
            ''')
        except sqlite3.IntegrityError as e:
            if str(e) == "UNIQUE constraint failed: nodes.node_id":
                code = 1 # Duplicate node_id error
            if str(e) == "UNIQUE constraint failed: nodes.name":
                code = 2 # Duplicate node_name error
            if str(e) == "CHECK constraint failed: LENGTH(node_id) <= 16":
                code = 3 # Over max length in node_id 
            if str(e) == "CHECK constraint failed: LENGTH(name) <= 16":
                code = 4 # Over max length in name
        conn.commit()
        conn.close()
        return code

    def update_node(self, node_id, soil):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        current_time = datetime.now()
        time = current_time.strftime("%H:%M %d-%m")
        c.execute(f'''
            UPDATE nodes SET soil='{soil}', up_time='{time}' WHERE node_id='{node_id}'
        ''')
        conn.commit()
        conn.close()

    def rename_node(self, node_id, new_name) -> int:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        code = 0
        try:
            c.execute(f'''
                UPDATE nodes SET name='{new_name}' WHERE node_id='{node_id}'
            ''')
        except sqlite3.IntegrityError as e:
            if str(e) == "UNIQUE constraint failed: nodes.name":
                code = 2
            if str(e) == "CHECK constraint failed: LENGTH(name) <= 16":
                code = 4 
        conn.commit()
        conn.close()
        return code

    def fetch_all_node(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM nodes
        ''')
        rows = c.fetchall()
        conn.close()
        return rows

    def fetch_node(self, node_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'''
            SELECT * FROM nodes WHERE node_id='{node_id}'
        ''')
        node = c.fetchone()
        conn.close()
        return node

    def delete_node(self, node_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'''
            DELETE FROM nodes WHERE node_id='{node_id}'
        ''')
        conn.commit()    
        conn.close()

    def delete_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM nodes")
        conn.commit()
        conn.close()

    def drop_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS nodes")
        conn.commit()
        conn.close()

class DataChart():
    def __init__(self):
        self.create_data_table()
        self.max_row = 200

    def create_data_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                temp REAL NOT NULL,
                hum REAL NOT NULL,
                rain REAL NOT NULL,
                lux REAL NOT NULL,
                date TEXT NOT NULL,
                hour INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_data(self, temp, hum, rain, lux):
        current_time = datetime.now()
        time = current_time.strftime("%H %d-%m")
        if len(self.fetch_all_data()) > self.max_row:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("DELETE FROM data WHERE id=(SELECT MIN(id) FROM data )")
            conn.commit()
            conn.close()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        time = time.split(" ")
        c.execute(f'''
            INSERT INTO data (temp, hum, rain, lux, date, hour) VALUES ('{temp}','{hum}','{round((abs(int(rain)-1024)/10.24),2)}','{lux}', '{time[1]}', '{time[0]}')
        ''')
        conn.commit()
        conn.close()

    def debug_insert_data(self, temp, hum, rain, lux, date, hour):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'''
            INSERT INTO data (temp, hum, rain, lux, date, hour) VALUES ('{temp}','{hum}','{rain}','{lux}', '{date}', '{hour}')
        ''')
        conn.commit()
        conn.close()

    def fetch_all_data(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM data
        ''')
        rows = c.fetchall()
        conn.close()
        return rows

    def fetch_data_limit(self, limit):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM data ORDER BY id DESC LIMIT {limit}")
        rows = c.fetchall()
        conn.close()
        return rows

    def fetch_data_by_day_and_type(self, date, type):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"SELECT {type},hour FROM data WHERE date = '{date}'")
        rows = c.fetchall()
        data_array = [-1]*24
        for row in rows:
            try:
                data_array[row[1]] = row[0]
            except:
                pass
        conn.close()
        return data_array
        
    def delete_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM data")
        conn.commit()
        conn.close()

    def drop_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS data")
        conn.commit()
        conn.close()

class NotifyBoard():
    def __init__(self):
        self.create_notify_table()

    def create_notify_board(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS NOTIFY (
                id INTEGER PRIMARY KEY,
                notify TEXT NOT NULL,
                time TEXT NOT NULL,
            )
        ''')
        conn.commit()
        conn.close()