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
        nodes = []
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM nodes
        ''')
        rows = c.fetchall()
        for row in rows:
            nodes.append({"id": row[1], "name": row[2], "soil": row[3], "up_time": row[4]}) 
        conn.close()
        return nodes

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
