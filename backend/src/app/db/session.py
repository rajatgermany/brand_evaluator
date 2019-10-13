from app.core import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

a = 'postgresql://postgres:changethis@34.65.154.15:5432/app'
print('a', a)
# engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
engine = create_engine(a, pool_pre_ping=True)


db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
