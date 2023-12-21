from typing import List, Dict, Any
from sqlite_database import create_connection


def create_user(user_data: Dict[str, Any]) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO users (first_name, last_name, email, balance, password)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (user_data['first_name'], user_data['last_name'], user_data['email'], user_data['balance'], user_data['password'])
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_id(user_id: int) -> Dict[str, Any]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'balance': user[4],
            'password': user[5]
        }
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
            'password': user[5]
        }
        for user in users
    ]


def update_user(user_id: int, updated_data: Dict[str, Any]) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE users
        SET first_name = ?, last_name = ?, email = ?, balance = ?, password = ?
        WHERE id = ?
        ''',
        (updated_data['first_name'], updated_data['last_name'], updated_data['email'], updated_data['balance'], updated_data['password'], user_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_user(user_id: int) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0