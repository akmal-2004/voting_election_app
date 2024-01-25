from typing import List, Dict, Any
from database import create_connection


def create_candidate(candidate_data: Dict[str, Any]) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO candidates (name, about, election_room_id)
        VALUES (%s, %s, %s)
        ''',
        (candidate_data['name'], candidate_data['about'], candidate_data['election_room_id'])
    )
    candidate_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return candidate_id


def get_candidate_by_id(candidate_id: int) -> Dict[str, Any]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM candidates WHERE id = %s', (candidate_id,))
    candidate = cursor.fetchone()
    conn.close()
    if candidate:
        return {
            'id': candidate[0],
            'name': candidate[1],
            'about': candidate[2],
            'election_room_id': candidate[3]
        }
    return None


def get_all_candidates() -> List[Dict[str, Any]]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM candidates')
    candidates = cursor.fetchall()
    conn.close()
    return [
        {
            'id': candidate[0],
            'name': candidate[1],
            'about': candidate[2],
            'election_room_id': candidate[3]
        }
        for candidate in candidates
    ]


def update_candidate(candidate_id: int, updated_data: Dict[str, Any]) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE candidates
        SET name = %s, about = %s, election_room_id = %s
        WHERE id = %s
        ''',
        (updated_data['name'], updated_data['about'], updated_data['election_room_id'], candidate_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_candidate(candidate_id: int) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM candidates WHERE id = %s', (candidate_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0
