import utils.utils as ut

answer_names = ut.get_answers_naming()


def chose_move() -> str:
    return answer_names.chose_move


def this_is_deeds() -> str:
    return answer_names.this_is_deeds + ':'


def deed_name_questions() -> str:
    return answer_names.deed_name_questions + '?'


def deed_added() -> str:
    return answer_names.deed_added


def notification_questions() -> str:
    return answer_names.notification_questions


def chose_day() -> str:
    return answer_names.chose_day


def chose_hour() -> str:
    return answer_names.chose_hour


def chose_minute() -> str:
    return answer_names.chose_minute


def time_passed() -> str:
    return answer_names.time_passed


def notify_added() -> str:
    return answer_names.notify_added


def deed_done() -> str:
    return answer_names.deed_done


def notification_canceled() -> str:
    return answer_names.notification_canceled


def text_new_deed_name() -> str:
    return answer_names.text_new_deed_name


def deed_renamed() -> str:
    return answer_names.deed_renamed


def dzyn() -> str:
    return answer_names.dzyn


def wow() -> str:
    return answer_names.wow
