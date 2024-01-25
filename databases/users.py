from typing import List, Dict, Any
from passlib.context import CryptContext
from database import create_connection


def create_user(user_data: Dict[str, Any]) -> int:
    conn = create_connection()
    cursor = conn.cursor()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user_data['password'])

    cursor.execute(
        '''
        INSERT INTO users (first_name, last_name, email, balance, username, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        ''',
        (user_data['first_name'], user_data['last_name'], user_data['email'], user_data['balance'], user_data['username'], hashed_password)
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id


def get_user_by_id(user_id: int) -> Dict[str, Any]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'balance': user[4],
            'username': user[5],
            'password': user[6]
        }
    return None


def get_user_by_username(username: str):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'balance': user[4],
            'username': user[5],
            'password': user[6]
        }
    else:
        return None


def get_all_users() -> List[Dict[str, Any]]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return [
        {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'balance': user[4],
            'username': user[5],
            'password': user[6]
        }
        for user in users
    ]


def update_user(user_id: int, updated_data: Dict[str, Any]) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE users
        SET first_name = %s, last_name = %s, email = %s, balance = %s, username = %s, password = %s
        WHERE id = %s
        ''',
        (updated_data['first_name'], updated_data['last_name'], updated_data['email'], updated_data['balance'], updated_data['username'], updated_data['password'], user_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_user(user_id: int) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0