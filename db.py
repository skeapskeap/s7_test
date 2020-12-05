from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
import json
from tools import logger, MyLocalException

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
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        raise MyLocalException


def insert(**kwargs):
    new_record = FLT(**kwargs)
    try:
        session.add(new_record)
        session.flush()
    except OperationalError:
        logger.error('Insert new person failed')
        raise MyLocalException


def save_to_db(json_data):
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
        logger.info('Commit to DB success')
    except OperationalError:
        logger.error('Commit to DB failed')
        raise MyLocalException