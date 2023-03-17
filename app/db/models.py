from sqlalchemy import Integer, String, Column, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base

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
    company_owner_id = Column("company_owner_id", ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    company_description = Column("company_description", String, nullable=True)

class Membership(Base):
    __tablename__ = "membership"
    membership_id = Column("membership_id", Integer, primary_key=True)
    membership_user_id = Column("membership_user_id", ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    membership_company_id = Column("membership_company_id", ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)

class Invite(Base):
    __tablename__ = "invite"
    invite_id = Column("invite_id", Integer, primary_key=True)
    invite_to_user_id = Column("invite_to_user_id", ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    invite_from_company_id = Column("invite_from_company_id", ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)
    invite_message = Column("invite_message", String, nullable=False)

class Request(Base):
    __tablename__ = "request"
    request_id = Column("request_id", Integer, primary_key=True)
    request_from_user_id = Column("request_from_user_id", ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    request_to_company_id = Column("request_to_company_id", ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)
    request_message = Column("request_message", String, nullable=False)