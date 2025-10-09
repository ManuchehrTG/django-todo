from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
	id: int
	first_name: str
	username: str | None = None
	language_code: str | None = None
	is_admin: bool = False
	is_block: bool = False
	created_at: datetime
	updated_at: datetime

class Category(BaseModel):
    id: str
    name: str
    user: User
    created_at: datetime

class Task(BaseModel):
	id: str
	title: str
	description: str | None = None
	user: User
	category: Category
	due_date: datetime
	completed: bool = False
	created_at: datetime
	updated_at: datetime
