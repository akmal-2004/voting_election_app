from typing import List, Dict, Any
from database import create_connection
import psycopg2


def create_election_room(room_data: Dict[str, Any]) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO election_rooms (name, user_id, status)
        VALUES (%s, %s, %s)
        ''',
        (room_data['name'], room_data['user_id'], room_data['status'])
    )
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return room_id


def create_paid_election_room(room_data: Dict[str, Any], cost: float):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Begin transaction
        conn.autocommit = False

        # Check user's balance
        cursor.execute('SELECT balance FROM users WHERE id = %s', (room_data['user_id'],))
        user_balance = cursor.fetchone()[0]
        
        # Check if user has enough balance to cover the cost
        if user_balance < cost:
            raise ValueError("Insufficient balance to create an election room")

        # Deduct cost from user's balance
        cursor.execute('UPDATE users SET balance = balance - %s WHERE id = %s', (cost, room_data['user_id']))

        # Create election room if deduction is successful
        cursor.execute('INSERT INTO election_rooms (name, user_id, status) VALUES (%s, %s, %s)', (room_data['name'], room_data['user_id'], room_data['status']))

        # Commit transaction if everything is successful
        conn.commit()
        result = True

    except psycopg2.Error as e:
        # Rollback on failure
        conn.rollback()
        result = f"Failed to create paid election room: {e}"

    finally:
        # Reset autocommit and close connection
        conn.autocommit = True
        conn.close()
        return result


def get_election_room_by_id(room_id: int) -> Dict[str, Any]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM election_rooms WHERE id = %s', (room_id,))
    room = cursor.fetchone()
    conn.close()
    if room:
        return {
            'id': room[0],
            'name': room[1],
            'user_id': room[2],
            'status': room[3]
        }
    return None


def get_all_election_rooms() -> List[Dict[str, Any]]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM election_rooms')
    rooms = cursor.fetchall()
    conn.close()
    return [
        {
            'id': room[0],
            'name': room[1],
            'user_id': room[2],
            'status': room[3]
        }
        for room in rooms
    ]


def update_election_room(room_id: int, updated_data: Dict[str, Any]) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE election_rooms
        SET name = %s, user_id = %s, status = %s
        WHERE id = %s
        ''',
        (updated_data['name'], updated_data['user_id'], updated_data['status'], room_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_election_room(room_id: int) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM election_rooms WHERE id = %s', (room_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0
