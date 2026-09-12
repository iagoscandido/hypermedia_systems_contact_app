from pydantic import BaseModel

from database import Database
from models.contact_model import Contact

db = Database()


class ContactService(BaseModel):
    @staticmethod
    def create(c: Contact):
        return db.create(c)

    @staticmethod
    def all():
        return db.get_all()

    @staticmethod
    def get_by_id(id: int):
        return db.get_by_id(contact_id=id)

    @staticmethod
    def get_by_any(search: str):
        return db.get_by_any(search)

    @staticmethod
    def update(c: Contact):
        if c.id is None:
            return None

        find = db.get_by_id(c.id)

        if find is None:
            return None

        return db.update(find)

    @staticmethod
    def delete(contact_id: int):
        return db.delete(contact_id=contact_id)
