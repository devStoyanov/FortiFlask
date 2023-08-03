from pydantic import BaseModel


# Pydantic schemas for data validation
class UserData(BaseModel):
    username: str
    password: str


class ContactsData(BaseModel):
    is_organization: bool
    name: str
    first_name: str
    last_name: str
    title: str
    email: str
    mobile: int
    address: str
    description: str
    tags: str
