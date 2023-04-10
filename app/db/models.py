from sqlalchemy import Integer, String, Column, DateTime, func, ForeignKey, Date, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.dialects.postgresql import ARRAY 

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_username = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String, nullable=False)
    user_first_name = Column(String, nullable=True)
    user_last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Company(Base):
    __tablename__ = "company"
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    company_owner_id = Column(Integer, nullable=False)
    company_description = Column(String, nullable=True)

class Membership(Base):
    __tablename__ = "membership"

    ROLES = [
        ("owner", "owner"), 
        ("admin", "admin"),
        ("user", "user")
    ]

    membership_id = Column(Integer, primary_key=True)
    membership_user_id = Column(ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    membership_company_id = Column(ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)
    membership_role = Column(ChoiceType(ROLES), server_default=u"user", nullable=False)

class Invite(Base):
    __tablename__ = "invite"
    invite_id = Column(Integer, primary_key=True)
    invite_to_user_id = Column(ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    invite_from_company_id = Column(ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)
    invite_message = Column(String, nullable=False)

class Request(Base):
    __tablename__ = "request"
    request_id = Column(Integer, primary_key=True)
    request_from_user_id = Column(ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    request_to_company_id = Column(ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)
    request_message = Column(String, nullable=False)

class Quiz(Base):
    __tablename__ = "quiz"
    quiz_id = Column(Integer, primary_key=True)
    quiz_name = Column(String, nullable=False)
    quiz_description = Column(String, nullable=True)
    quiz_frequency_in_days = Column(Integer, nullable=False)
    quiz_company_id = Column(ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)

class QuizQuestion(Base):
    __tablename__ = "quiz_question"
    question_id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False)
    question_choices = Column(ARRAY(String), nullable=False)
    question_answer = Column(String, nullable=False)
    question_quiz_id = Column(ForeignKey("quiz.quiz_id", ondelete='CASCADE'))

class QuizWorkflow(Base):
    __tablename__ = "quiz_workflow"
    workflow_id = Column(Integer, primary_key=True)
    workflow_user_id = Column(ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    workflow_quiz_id = Column(ForeignKey("quiz.quiz_id", ondelete="NO ACTION"), nullable=False)
    workflow_company_id = Column(ForeignKey("company.company_id", ondelete='NO ACTION'), nullable=False)
    workflow_record_correct_answers = Column(Integer, nullable=True)
    workflow_record_all_questions = Column(Integer, nullable=False)
    workflow_record_result = Column(Float, nullable=True)
    workflow_quiz_correct_answers = Column(Integer, nullable=True)
    workflow_quiz_all_questions = Column(Integer, nullable=False)
    workflow_quiz_result = Column(Float, nullable=True)
    workflow_company_correct_answers = Column(Integer, nullable=True)
    workflow_company_all_questions = Column(Integer, nullable=False)
    workflow_company_result = Column(Float, nullable=True)
    workflow_system_correct_answers = Column(Integer, nullable=True)
    workflow_system_all_questions = Column(Integer, nullable=False)
    workflow_system_result = Column(Float, nullable=True)
    workflow_date = Column(Date(), server_default=func.now())


class Notification(Base):

    __tablename__ = "notification"
    notification_id = Column(Integer, primary_key=True)
    notification_user_id = Column(ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    notification_quiz_id = Column(ForeignKey("quiz.quiz_id", ondelete="CASCADE"), nullable=False)
    notification_company_id = Column(ForeignKey("company.company_id", ondelete='CASCADE'), nullable=False)
    notification_text = Column(String, nullable=False)
    notification_status = Column(Boolean, nullable=False)
    notification_time = Column(DateTime(timezone=True), server_default=func.now())
