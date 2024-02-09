from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Model():
  id = Column(UUID(as_uuid=True), primary_key=True)