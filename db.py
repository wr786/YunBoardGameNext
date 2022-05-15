from functools import wraps
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_USER, DATABASE_PWD, DATABASE_HOST, DATABASE_PORT
from config import DATABASE

from utils import Eprint

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    name = Column(String(20))
    password = Column(String(100))

engine = create_engine(f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}')
DBSession = sessionmaker(bind=engine)

def Fail2None(func):
    @wraps(func)
    def Fail2None(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            Eprint(e)
            return None
    return Fail2None

@Fail2None
def get_user(username):
    session = DBSession()
    user = session.query(User).filter(User.name == username).one()
    return user

def add_user(username, password):
    session = DBSession()
    new_user = User(name=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()