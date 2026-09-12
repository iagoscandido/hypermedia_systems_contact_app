from typing import Optional

from pydantic import BaseModel


class Contact(BaseModel):
    id: Optional[int] = None
    first: str | None = None
    last: str | None = None
    phone: str | None = None
    email: str | None = None
