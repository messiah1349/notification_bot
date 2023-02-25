import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

import utils.utils as ut
from configs.definitions import ROOT_DIR


Base = declarative_base()


class Deed(Base):

    __tablename__ = 'deed'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String)
    create_time = Column(DateTime)
    notify_time = Column(DateTime)
    done_flag = Column(Boolean)


if __name__ == '__main__':

    CONFIG_PATH = ROOT_DIR + '/configs/config.yaml'
    config = ut.read_config(CONFIG_PATH)
    bd_directory = config['bd_directory']
    bd_name = config['bd_name']

    if not os.path.exists(f"{ROOT_DIR}/{bd_directory}"):
        os.makedirs(f"{ROOT_DIR}/{bd_directory}")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT_DIR}/{bd_directory}{bd_name}"

    engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:1349/notification_bot')
    # engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
