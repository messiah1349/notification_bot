from sqlalchemy import create_engine, insert, func
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from typing import Any
from datetime import datetime
import logging

from lib.db.deed import Deed
from configs.definitions import ROOT_DIR

logger = logging.getLogger(__name__)


@dataclass
class Response:
    """every backend method should return response object"""
    status: int  # 0 status - everything is good, else - there is error
    answer: Any  # result


def db_executor(func):
    """create and close sqlalchemy session for class methods which execute sql statement"""
    def inner(*args, **kwargs):
        self_ = args[0]

        with Session(self_.engine) as session:
            func(*args, **kwargs, session=session)
            session.commit()
    return inner


def db_selector(func):
    """create and close sqlalchemy session for class methods which return query result"""
    def inner(*args, **kwargs):
        self_ = args[0]

        with Session(self_.engine) as session:
            result = func(*args, **kwargs, session=session)
            return result
    return inner


class TableProcessor:

    def __init__(self, engine):
        session_factory = sessionmaker(bind=engine)
        self.engine = engine
        self.Session = scoped_session(session_factory)

    @db_selector
    def get_query_result(self, query: "sqlalchemy.orm.query.Query", session=None) -> list["table_model"]:
        logger.error('inside get query result 1')
        result = session.execute(query).scalars().all()
        logger.error('inside get query result 2')
        return result

    @db_executor
    def _insert_values(self, table_model: "sqlalchemy.orm.decl_api.DeclarativeMeta", data: dict, session=None) -> None:
        ins_command = insert(table_model).values(**data)
        session.execute(ins_command)

    @db_selector
    def _get_all_data(self, table_model: "sqlalchemy.orm.decl_api.DeclarativeMeta", session=None) -> list[
        'table_model']:
        query = session.query(table_model)
        result = self.get_query_result(query)
        return result

    @db_selector
    def _get_filtered_data(self, table_model, filter_values: dict, session=None) -> list['table_model']:
        logger.error('inside selector')
        query = session.query(table_model)
        logger.error('inside selector2')
        for filter_column in filter_values:
            query = query.filter(getattr(table_model, filter_column) == filter_values[filter_column])
        logger.error('inside selector3')
        result = self.get_query_result(query)
        logger.error('inside selector4')
        return result

    @db_executor
    def _change_column_value(self, table_model, filter_values: dict, change_values: dict, session=None) -> None:
        query = session.query(table_model)
        for filter_column in filter_values:
            query = query.filter(getattr(table_model, filter_column) == filter_values[filter_column])
        query.update(change_values)

    @db_selector
    def _get_max_value_of_column(self, table_model, column: str, session=None):

        query = func.max(getattr(table_model, column))
        result = self.get_query_result(query)[0]

        # case with empty table
        if not result:
            result = 0

        return result


class DeedProcessor(TableProcessor):

    def __init__(self, engine):
        super().__init__(engine)
        self.table_model = Deed

    def insert_deed(self, deed_name: str, telegram_id: int) -> int:

        try:
            current_id = self.get_max_id() + 1
            data = {
                'id': current_id,
                'telegram_id': telegram_id,
                'name': deed_name,
                'create_time': datetime.now(),
                'notify_time': None,
                'done_flag': False,
            }
            self._insert_values(self.table_model, data)
            logger.info(f"deed '{deed_name}' was inserted to DB")
            return Response(0, current_id)
        except Exception as e:
            logger.error(f"deed '{deed_name}' was not inserted to DB, exception - {e}")
            return Response(1, e)

    def get_all_active_deeds(self) -> list[Deed]:
        filter_values = {
            'done_flag': False
        }
        try:
            logger.error('try to get data')
            deeds = self._get_filtered_data(self.table_model, filter_values)
            active_deeds = [deed for deed in deeds if deed.notify_time]
            logger.info(f"all active deeds was passed")
            return Response(0, active_deeds)
        except Exception as e:
            logger.error(f"all active deeds was not passed, exception - {e}")
            return Response(1, e)

    def get_max_id(self):
        return self._get_max_value_of_column(self.table_model, 'id')

    def add_notification(self, deed_id: int, notification_time: datetime) -> Response(int, str):
        filter_values = {
            'id': deed_id
        }
        change_values = {
            'notify_time': notification_time
        }
        try:
            self._change_column_value(self.table_model, filter_values, change_values)
            logger.info(f"notification for {deed_id=} was set to {notification_time}")
            return Response(0, 'OK')
        except Exception as e:
            logger.error(f"notification for {deed_id=} was NOT set to {notification_time}, exception - {e}")
            return Response(1, e)

    def mark_deed_as_done(self, deed_id: int) -> Response(int, str):
        filter_values = {
            'id': deed_id
        }
        change_values = {
            'done_flag': True
        }
        try:
            self._change_column_value(self.table_model, filter_values, change_values)
            logger.info(f"{deed_id=} was marked as done")
            return Response(0, 'OK')
        except Exception as e:
            logger.error(f"{deed_id=} was NOT marked as done, exception - {e}")
            return Response(1, e)

    def get_deeds_for_user(self, telegram_id: int) -> Response(int, list[Deed]):
        filter_values = {
            'telegram_id': telegram_id,
            'done_flag': False
        }
        deeds = self._get_filtered_data(self.table_model, filter_values)
        logger.info(f"returned deeds for user - {telegram_id}")
        return Response(0, deeds)

    def get_deed_by_id(self, deed_id: int) -> Response(int, Deed):
        filter_values = {
            'id': deed_id
        }
        deed = self._get_filtered_data(self.table_model, filter_values)[0]
        logger.info(f"returned {deed_id=}")
        return Response(0, deed)

    def rename_deed_name(self, deed_id: int, new_deed_name: str):
        filter_values = {
            'id': deed_id
        }
        change_values = {
            'name': new_deed_name
        }
        try:
            self._change_column_value(self.table_model, filter_values, change_values)
            logger.info(f"{deed_id=} was renamed to {new_deed_name}")
            return Response(0, 'OK')
        except Exception as e:
            logger.error(f"{deed_id=} was NOT renamed to {new_deed_name}, exception - {e}")
            return Response(1, e)


class Backend:

    def __init__(self, engine):
        self.deed_processor = DeedProcessor(engine)

    def add_deed(self, deed_name: str, telegram_id: int) -> Response:
        return self.deed_processor.insert_deed(deed_name, telegram_id)

    def get_active_deeds(self) -> Response:
        return self.deed_processor.get_all_active_deeds()

    def add_notification(self, deed_id: int, notification_time: datetime) -> Response:
        return self.deed_processor.add_notification(deed_id, notification_time)

    def mark_deed_as_done(self, deed_id: int) -> Response:
        return self.deed_processor.mark_deed_as_done(deed_id)

    def rename_deed(self, deed_id: int, new_deed_name: str) -> Response:
        return self.deed_processor.rename_deed_name(deed_id, new_deed_name)

    def get_deed_for_user(self, telegram_id: int) -> Response:
        return self.deed_processor.get_deeds_for_user(telegram_id)

    def get_deed(self, deed_id) -> Response:
        return self.deed_processor.get_deed_by_id(deed_id)
