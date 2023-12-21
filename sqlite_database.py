import sqlite3

DATABASE_NAME = 'voting_election_db.sqlite'

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            balance INTEGER,
            password VARCHAR(100)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS election_rooms (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            user_id INTEGER,
            status INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            about TEXT,
            election_room_id INTEGER,
            FOREIGN KEY (election_room_id) REFERENCES election_rooms(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            election_room_id INTEGER,
            candidate_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (election_room_id) REFERENCES election_rooms(id),
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
    ''')
    conn.commit()
    conn.close()


def print_talbes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    print("Tables:")
    for table in tables:
        print(table[0])