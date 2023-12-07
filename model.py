from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime

class Base(DeclarativeBase):
    pass

class ContactUs(Base):
    __tablename__ = "contactus"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    full_name = Column("full_name", String(30), nullable=False)
    email = Column("email", String(256), nullable=False)
    message = Column("message", String(1024), nullable=False)
    created_date = Column("created_date", DateTime, nullable=False)
