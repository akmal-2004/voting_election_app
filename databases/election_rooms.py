from typing import List, Dict, Any
from sqlite_database import create_connection


def create_election_room(room_data: Dict[str, Any]) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO election_rooms (name, user_id, status)
        VALUES (?, ?, ?)
        ''',
        (room_data['name'], room_data['user_id'], room_data['status'])
    )
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return room_id


def get_election_room_by_id(room_id: int) -> Dict[str, Any]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM election_rooms WHERE id = ?', (room_id,))
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
        SET name = ?, user_id = ?, status = ?
        WHERE id = ?
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
    cursor.execute('DELETE FROM election_rooms WHERE id = ?', (room_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0
