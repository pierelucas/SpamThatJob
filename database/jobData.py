# PiereLucas 05.06.2025

''' REDEFINE THIS (!)
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()

class Job(Base):

    Name: str = None
    Description: str = None
    Type: str = None
    Ref: str = None
    Url: str = None

    Contact: dict = {
        'email': None,
        'phone': None,
        'company': None,
        'contactPerson': None,
        'address': {
            'street': None,
            'city': None,
            'state': None,
            'zip': None,
            'country': None
        }
    }

    Status: dict = {
        'active': False,
        'completed': False,
        'when': None
    }

    def __init__(self,
                 name: str = None,
                 Description: str = None,
                 Type: str = None,
                 Ref: str = None,
                 Url: str = None,) -> None:
        self.name = name
        self.Description = Description
        self.Type = Type
        self.Ref = Ref
        self.Url = Url
        return

    def toJSON(self) -> str:
        # TODO: Return database to JSON String
        return ""

    def fromJSON(self, jsondata: str):
        # TODO: read from JSON
        return
'''

import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the Database URL
DATABASE_URL = "sqlite:///./jobs.db"

# SQLalchemy Setup
Base = declarative_base()
engine = create_engine(DATABASE_URL,
                       connect_args={'check_same_thread': False}
)

# SessionLocal will be sued to crreate database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Jobs(Base):
    __tablename__ = 'jobs'

    # Auto-Incrementing User ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    Name = Column(String, index=True)
    Description = Column(String, nullable=True)
    Type = Column(String, nullable=True)
    Ref = Column(String, unique=True, index=True, nullable=True)
    Url = Column(String, nullanle=True)

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now(datetime.UTC))

    


