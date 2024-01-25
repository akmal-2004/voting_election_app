from typing import List, Dict, Any
from database import create_connection


def create_vote(vote_data: Dict[str, Any]) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO votes (user_id, election_room_id, candidate_id)
        VALUES (%s, %s, %s)
        ''',
        (vote_data['user_id'], vote_data['election_room_id'], vote_data['candidate_id'])
    )
    vote_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return vote_id


def get_vote_by_id(vote_id: int) -> Dict[str, Any]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM votes WHERE id = %s', (vote_id,))
    vote = cursor.fetchone()
    conn.close()
    if vote:
        return {
            'id': vote[0],
            'user_id': vote[1],
            'election_room_id': vote[2],
            'candidate_id': vote[3]
        }
    return None


def get_all_votes() -> List[Dict[str, Any]]:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM votes')
    votes = cursor.fetchall()
    conn.close()
    return [
        {
            'id': vote[0],
            'user_id': vote[1],
            'election_room_id': vote[2],
            'candidate_id': vote[3]
        }
        for vote in votes
    ]


def update_vote(vote_id: int, updated_data: Dict[str, Any]) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE votes
        SET user_id = %s, election_room_id = %s, candidate_id = %s
        WHERE id = %s
        ''',
        (updated_data['user_id'], updated_data['election_room_id'], updated_data['candidate_id'], vote_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_vote(vote_id: int) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM votes WHERE id = %s', (vote_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0
