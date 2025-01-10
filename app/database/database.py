from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/book_my_show"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://mysql_user:password123@localhost:3306/mydatabase"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, bind=engine)


Base = declarative_base()