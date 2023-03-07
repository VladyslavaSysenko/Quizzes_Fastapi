from sqlalchemy import Integer, String,Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    user_id = Column("user_id", Integer, primary_key=True)
    user_username = Column("user_username", String, unique=True, nullable=False)
    user_email = Column("user_email", String, unique=True, nullable=False)
    user_password = Column("user_password", String, nullable=False)
    user_first_name = Column("user_first_name", String, nullable=False)
    user_last_name = Column("user_last_name", String, nullable=False)
