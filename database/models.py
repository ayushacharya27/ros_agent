from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WorkspaceSession(Base):

    __tablename__ = "workspace_sessions"

    id = Column(Integer, primary_key=True)

    workspace_state = Column(JSONB)