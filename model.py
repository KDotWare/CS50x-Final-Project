from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Date, Boolean, ForeignKey

class Base(DeclarativeBase):
    pass

class ContactUs(Base):
    __tablename__ = "contactus"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    full_name = Column("full_name", String(60), nullable=False)
    email = Column("email", String(256), nullable=False)
    message = Column("message", String(1024), nullable=False)
    created_date = Column("created_date", DateTime, nullable=False)

class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    email = Column("email", String(256), nullable=False, unique=True)
    password = Column("password", Text, nullable=False)
    email_verified = Column("email_verified", Boolean, nullable=False)
    is_user_ext = Column("is_user_ext", Boolean, nullable=False) # False = userext is not setup, True = userext is setup
    registered_date = Column("registered_date", DateTime, nullable=False)

class UserExt(Base):
    __tablename__ = "userext"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    user = Column("user", Integer, ForeignKey("user.id"), nullable=False)
    first_name = Column("first_name", String(30), nullable=False)
    middle_name = Column("middle_name", String(30), nullable=False)
    last_name = Column("last_name", String(30), nullable=False)
    gender = Column("gender", String(15), nullable=False)
    birth = Column("birth", Date, nullable=False)

class Category(Base):
    __tablename__ = "category"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    name = Column("name", String(30), nullable=False, unique=True)
    description = Column("description", String(512), nullable=False)

class Product(Base):
    __tablename__ = "product"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    title = Column("title", String(100), nullable=False)
    price = Column("price", Float(18, 2), nullable=False)
    category = Column("category", Integer, ForeignKey("category.id"), nullable=False)
    description = Column("description", Text, nullable=True)
    availability = Column("availability", Boolean, nullable=False) # False = single item; True = in stock

class ProductImage(Base):
    __tablename__ = "productimage"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    product = Column("product", Integer, ForeignKey("product.id"), nullable=False)
    file_name = Column("file_name", Text, nullable=False)
