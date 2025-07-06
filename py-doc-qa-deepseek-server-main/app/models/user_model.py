import uuid
from datetime import datetime
from typing import Optional
from fastapi import File, UploadFile
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, field_validator
class User(SQLModel, table=True):
    """用户表"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    password: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)

