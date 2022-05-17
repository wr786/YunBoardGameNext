from functools import wraps
from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

from config import DATABASE_USER, DATABASE_PWD, DATABASE_HOST, DATABASE_PORT
from config import DATABASE
from utils import Eprint

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True)
    name = Column(String(20))
    password = Column(String(100))
    avatarUrl = Column(String(120))

class BoardGame(Base):
    __tablename__ = 'boardGame'
    
    bgid = Column(Integer, primary_key=True)
    name = Column(String(50))
    imgUrl = Column(String(120))

class Play(Base):
    __tablename__ = 'play'
    
    pid = Column(Integer, primary_key=True)
    bgid = Column(Integer)
    time = Column(DateTime)
    winnerid = Column(Integer)
    loserid = Column(Integer)
    scoreboard = Column(JSON)
    order = Column(JSON)

class Collection(Base):
    __tablename__ = 'collection'

    uid = Column(Integer, primary_key=True)
    bgid = Column(Integer, primary_key=True)

class Participate(Base):
    __tablename__ = 'participate'

    uid = Column(Integer, primary_key=True)
    pid = Column(Integer, primary_key=True)

class Extension(Base):
    __tablename__ = 'extension'

    exid = Column(Integer, primary_key=True)
    name = Column(String(50))
    bgid = Column(Integer)


engine = create_engine(f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}', pool_size=100, max_overflow=20)
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

@Fail2None
def get_user_by_uid(uid):
    session = DBSession()
    user = session.query(User).filter(User.uid == uid).one()
    return user

def add_user(username, password):
    session = DBSession()
    new_user = User(name=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()

@Fail2None
def get_all_users():
    session = DBSession()
    users = session.query(User).all()
    return users

def add_board_game(name, imgUrl):
    session = DBSession()
    new_board_game = BoardGame(name=name, imgUrl=imgUrl)
    session.add(new_board_game)
    session.commit()
    session.close()

@Fail2None
def get_board_game_by_name(name):
    session = DBSession()
    board_game = session.query(BoardGame).filter(BoardGame.name==name).one()
    return board_game

@Fail2None
def get_board_game_by_name(name):
    session = DBSession()
    board_game = session.query(BoardGame).filter(BoardGame.name==name).one()
    return board_game

@Fail2None
def get_board_game_by_id(bgid):
    session = DBSession()
    board_game = session.query(BoardGame).filter(BoardGame.bgid==bgid).one()
    return board_game

@Fail2None
def get_all_board_games():
    session = DBSession()
    bgs = session.query(BoardGame).all()
    return bgs

def modify_avatar_url(name, avatarUrl):
    session = DBSession()
    user = session.query(User).filter(User.name==name).one()
    user.avatarUrl = avatarUrl
    session.add(user)
    session.commit()
    session.close()

@Fail2None
def get_all_plays():
    session = DBSession()
    plays = session.query(Play).all()
    return plays