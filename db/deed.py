import os
from sqlalchemy import create_engine, Column, Integer, String, DATETIME, Float
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

from config.definitions import ROOT_DIR
import utils.utils as ut

Base = declarative_base()


class Deed(Base):

    __tablename__ = 'deed'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String)
    create_time = Column(DATETIME)
    notify_time = Column(DATETIME)
    done_flag = Column(Integer)

    # def __repr__(self):
    #     return self.name + ' ' + str(self.telegram_id)


if __name__ == '__main__':

    CONFIG_PATH = ROOT_DIR + '/config/config.yaml'
    config = ut.read_config(CONFIG_PATH)
    bd_directory = config['bd_directory']
    bd_name = config['bd_name']

    if not os.path.exists(f"{ROOT_DIR}/{bd_directory}"):
        os.makedirs(f"{ROOT_DIR}/{bd_directory}")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT_DIR}/{bd_directory}{bd_name}"

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
