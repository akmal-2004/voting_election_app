import psycopg2

DATABASE_NAME = 'voting_election_db'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '1234'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

def create_connection():
    return psycopg2.connect(
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            balance INTEGER,
            username VARCHAR(100),
            password VARCHAR(100)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS election_rooms (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            user_id INTEGER,
            status INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            about TEXT,
            election_room_id INTEGER,
            FOREIGN KEY (election_room_id) REFERENCES election_rooms(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id SERIAL PRIMARY KEY,
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

def print_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")
    columns = cursor.fetchall()

    # Extract column names
    column_names = [col[0] for col in columns]

    print(f"Columns of table 'users':")
    print(column_names)

    conn.close()