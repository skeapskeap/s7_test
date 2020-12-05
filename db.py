from datetime import datetime as dt
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tools import logger, MyLocalException
import json


Base = declarative_base()
engine = create_engine('sqlite:///flights.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class FLT(Base):
    __tablename__ = 'flt'

    id = Column('index', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    flt = Column('flt', Integer, nullable=False)
    depdate = Column('dapdate', Date, nullable=False)
    dep = Column('dep', String, nullable=False)

    def __repr__(self):
        return f'<Flights({self.name} {self.flt})>'


def init_db():
    '''
    Crete db with table 'flt'
    Or do nothing if they exist
    '''
    try:
        Base.metadata.create_all(bind=engine)
        logger.info('Init DB - OK')
    except OperationalError:
        logger.info('Init DB - Error')
        raise MyLocalException


def insert(**kwargs):
    '''
    Expects DB fields as kwargs
    Flush changes to session
    '''
    new_record = FLT(**kwargs)
    try:
        session.add(new_record)
        session.flush()
    except OperationalError:
        logger.error('Insert new person failed')
        raise MyLocalException


def save_to_db(json_data):
    '''
    Parse json to DB fields
    Put them to session with insert()
    Commit changes
    '''
    data = json.loads(json_data)
    flt=data['flt']
    depdate=data['date']
    depdate = dt.strptime(depdate, '%Y-%m-%d')
    dep=data['dep']

    try:
        for person in data['prl']:
            insert(
                name=f"{person['surname']} {person['firstname']}",
                flt=flt,
                depdate=depdate,
                dep=dep)
        session.commit()
        logger.info('Commit to DB - OK')
    except OperationalError:
        logger.error('Commit to DB - Error')
        raise MyLocalException
