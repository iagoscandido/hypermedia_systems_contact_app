import sqlite3
from typing import Optional

from models.contact_model import Contact


class Database:
    def __init__(self, database: str = "app.db"):
        self.database = database
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def _create_table(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first TEXT NOT NULL,
                    last TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)

    def create(self, contact: Contact) -> Optional[int]:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO contacts (
                    first,
                    last,
                    phone,
                    email
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    contact.first,
                    contact.last,
                    contact.phone,
                    contact.email,
                ),
            )
            return cursor.lastrowid

    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, first, last, phone, email
                FROM contacts
                WHERE id = ?
                """,
                (contact_id,),
            ).fetchone()

        if row is None:
            return None

        return Contact(
            id=row[0],
            first=row[1],
            last=row[2],
            phone=row[3],
            email=row[4],
        )

    def get_by_any(self, search: str) -> list[Contact]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, first, last, phone, email
                FROM contacts
                WHERE first LIKE ?
                   OR last LIKE ?
                   OR phone LIKE ?
                   OR email LIKE ?
                """,
                (
                    query_like(search),
                    query_like(search),
                    query_like(search),
                    query_like(search),
                ),
            ).fetchall()

            return [
                Contact(
                    id=row[0],
                    first=row[1],
                    last=row[2],
                    phone=row[3],
                    email=row[4],
                )
                for row in rows
            ]

    def get_all(self) -> list[Contact]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, first, last, phone, email
                FROM contacts
                """
            ).fetchall()

        return [
            Contact(
                id=row[0],
                first=row[1],
                last=row[2],
                phone=row[3],
                email=row[4],
            )
            for row in rows
        ]

    def update(self, contact: Contact) -> Optional[int]:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE contacts
                SET first = ?,
                    last = ?,
                    phone = ?,
                    email = ?
                WHERE id = ?
                """,
                (
                    contact.first,
                    contact.last,
                    contact.phone,
                    contact.email,
                    contact.id,
                ),
            )
            return cursor.lastrowid

    def delete(self, contact_id: int) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM contacts
                WHERE id = ?
                """,
                (contact_id,),
            )


def query_like(param: str):
    return f"%{param}%"
