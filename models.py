from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()

class Submission(Base):
    __tablename__ = "Submission"
    __table_args__ = {"schema": "Volha_Platnitskaya_submission"}

    submissionID = Column(Integer, primary_key=True)
    projectId = Column(Integer)
    userId = Column(Integer)
    statusId = Column(Integer)
    createdAt = Column(DateTime)