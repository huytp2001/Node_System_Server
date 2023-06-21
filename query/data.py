import sqlite3
from datetime import datetime

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