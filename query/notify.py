import sqlite3
from datetime import datetime

class Notify:
    def __init__(self):
        self.create_notify_table()

    def create_notify_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS notify (
                id INTEGER PRIMARY KEY,
                mess TEXT NOT NULL,
                up_time DATETIME NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_notify(self, mess):
        current_time = datetime.now()
        time = current_time.strftime("%H:%M %d/%m")
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'''
            INSERT INTO notify (mess, up_time) VALUES ('{mess}','{time}')
        ''')
        conn.commit()
        conn.close()

    def get_all_notify(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM notify
        ''')
        row_array = []
        rows = c.fetchall()
        for row in rows:
            row_array.append({"id": row[0], "mess": row[1], "time": row[2]})
        conn.close()
        return row_array

    def delete_notify(self, id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'''
            DELETE FROM notify WHERE id='{id}'
        ''')
        conn.commit()    
        conn.close()


