import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
import logging

from configs.definitions import ROOT_DIR
import utils.utils as ut

logger = logging.getLogger(__name__)

Base = declarative_base()


class Deed(Base):

    __tablename__ = 'deed'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String)
    create_time = Column(DateTime)
    notify_time = Column(DateTime)
    done_flag = Column(Boolean)


def get_engine(postgres_password: str, postgres_port:str, postgres_host:str):
    url = f'postgresql+psycopg2://postgres:{postgres_password}@{postgres_host}:{postgres_port}/notification_bot'
    postgres_engine = create_engine(url)
    return postgres_engine


def create_data_base_and_tables(engine):

    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"database was created, url={engine.url}")
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    CONFIG_PATH = ROOT_DIR + '/configs/config.yaml'
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
