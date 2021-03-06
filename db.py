from functools import wraps
from requests import session
from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymysql.converters import escape_string
import datetime
import json

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

    def __init__(self, u):
        self.uid, self.name, self.password, self.avatarUrl = u

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
    user = session.execute(f"""
        SELECT * from user where user.name = '{escape_string(username)}'
    """).fetchone()
    # user = session.query(User).filter(User.name == username).one()
    return user

@Fail2None
def get_user_by_uid(uid):
    session = DBSession()
    user = session.execute(f"""
        SELECT * from user where uid = {uid}
    """).fetchone()
    # user = session.query(User).filter(User.uid == uid).one()
    return user

def add_user(username, password):
    session = DBSession()
    session.execute(f"""
        REPLACE into user (name, password) values('{escape_string(username)}', '{escape_string(password)}')
    """)
    # new_user = User(name=username, password=password)
    # session.add(new_user)
    session.commit()
    session.close()

@Fail2None
def get_all_users():
    session = DBSession()
    users = session.execute("""
        SELECT * from user
    """).fetchall()
    # users = session.query(User).all()
    return users

def add_board_game(name, imgUrl):
    session = DBSession()
    session.execute(f"""
        REPLACE into boardGame(name, imgUrl) values('{escape_string(name)}', '{escape_string(imgUrl)}')
    """)
    # new_board_game = BoardGame(name=name, imgUrl=imgUrl)
    # session.add(new_board_game)
    session.commit()
    session.close()

@Fail2None
def get_board_game_by_name(name):
    session = DBSession()
    board_game = session.execute(f"""
        SELECT * from boardGame where name = '{escape_string(name)}'
    """).fetchone()
    # board_game = session.query(BoardGame).filter(BoardGame.name==name).one()
    return board_game

@Fail2None
def get_board_game_by_id(bgid):
    session = DBSession()
    board_game = session.execute(f"""
        SELECT * from boardGame where bgid={bgid}
    """).fetchone()
    # board_game = session.query(BoardGame).filter(BoardGame.bgid==bgid).one()
    return board_game

@Fail2None
def get_all_board_games():
    session = DBSession()
    bgs = session.execute(f"""
        SELECT * from boardGame
    """).fetchall()
    # bgs = session.query(BoardGame).all()
    return bgs

def modify_avatar_url(name, avatarUrl):
    session = DBSession()
    session.execute(f"""
        UPDATE user SET avatarUrl = '{escape_string(avatarUrl)}'
        where name = '{escape_string(name)}'
    """)
    # user = session.query(User).filter(User.name==name).one()
    # user.avatarUrl = avatarUrl
    # session.add(user)
    session.commit()
    session.close()

@Fail2None
def get_all_plays():
    session = DBSession()
    plays = session.execute(f"""
        SELECT * from play
    """).fetchall()
    # plays = session.query(Play).all()
    return plays

def add_play(date, bgid, winnerid, loserid, scoreboard, order):
    session = DBSession()
    print(json.dumps(scoreboard))
    session.execute(f"""
        REPLACE into play(time, bgid, winnerid, loserid, scoreboard, `order`)
        values('{datetime.datetime.strptime(date, "%Y-%m-%d")}', {bgid}, {winnerid}, {loserid}, '{json.dumps(scoreboard)}', '{json.dumps(order)}')
    """)
    # session.add(Play(
    #     time=datetime.datetime.strptime(date, "%Y-%m-%d"), 
    #     bgid=bgid, 
    #     winnerid=winnerid, 
    #     loserid=loserid, 
    #     scoreboard=scoreboard, 
    #     order=order
    # ))
    session.commit()
    play = session.execute(f"""
        SELECT * from play where time='{datetime.datetime.strptime(date, "%Y-%m-%d")}' and bgid={bgid}
    """).fetchone()
    session.close()
    return play.pid

def add_participate(uid, pid):
    session = DBSession()
    session.execute(f"""
        REPLACE into participate(uid, pid) values({uid}, {pid})
    """)
    session.commit()
    session.close()

def add_extension(bgid, exname):
    session = DBSession()
    session.execute(f"""
        REPLACE into extension(name, bgid) values('{escape_string(exname)}', {bgid})
    """)
    session.commit()
    session.close()

def add_collection(uid, bgid):
    session = DBSession()
    session.execute(f"""
        REPLACE into collection(uid, bgid) values({uid}, {bgid})
    """)
    session.commit()
    session.close()