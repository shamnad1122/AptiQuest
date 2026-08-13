from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = (
    "mssql+pyodbc://@localhost/AptiQuestDb"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Trusted_Connection=yes"
    "&TrustServerCertificate=yes"
)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    echo=True
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()