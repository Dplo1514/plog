from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL: str = "postgresql://admin:admin@localhost:5432/plog"
engine: Engine = create_engine(DATABASE_URL)
make_session: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)