import yaml
import pytz
import os
from dataclasses import make_dataclass
from configs.definitions import ROOT_DIR
from datetime import datetime


def read_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        prime_service = yaml.safe_load(file)

    return prime_service


CONFIG_PATH = ROOT_DIR + '/configs/config.yaml'
config = read_config(CONFIG_PATH)


def get_menu_names():
    menu_naming = config['menu_naming']
    MenuNames = make_dataclass("MenuNames", [(eng, str, rus) for eng, rus in menu_naming.items()])
    menu_names = MenuNames()

    return menu_names


def get_answers_naming():
    answers_naming = config['answers_naming']
    AnswersNames = make_dataclass("AnswersNames", [(eng, str, rus) for eng, rus in answers_naming.items()])
    answers_names = AnswersNames()

    return answers_names


def name_to_reg(name: str) -> str:
    return f"^{name}$"


def localize(datetime_: datetime):
    timezone_ = os.getenv('TZ', None)
    tz = pytz.timezone(timezone_)
    datetime_.astimezone(tz)
    return datetime_.astimezone(tz)


def repr_date(datetime_: datetime, time_: bool = False) -> str:
    if not time_:
        return datetime_.strftime('%d %b, %a')
    else:
        return datetime_.strftime('%d %b, %a, %H:%M')
