from sqlalchemy import Integer, String, Column, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column("user_id", Integer, primary_key=True)
    user_username = Column("user_username", String, nullable=False)
    user_email = Column("user_email", String, unique=True, nullable=False)
    user_password = Column("user_password", String, nullable=False)
    user_first_name = Column("user_first_name", String, nullable=True)
    user_last_name = Column("user_last_name", String, nullable=True)
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now())

class Company(Base):
    __tablename__ = "company"
    company_id = Column("company_id", Integer, primary_key=True)
    company_name = Column("company_name", String, nullable=False)
    company_owner_id = Column("company_owner_id", Integer, nullable=False)
    company_description = Column("company_description", String, nullable=True)
