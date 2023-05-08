import os
from lib.client import Client
from db.deed import get_engine, create_data_base_and_tables

if __name__ == '__main__':

    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '1349')
    API_TOKEN = os.getenv('NOTIFICATION_BOT_TOKEN', '214139458:AAH8UGU0PW3vUE1lRz-gjXnlB6TroUvpfUk')
    # just a test bot by default for testing

    engine = get_engine(POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_HOST)
    create_data_base_and_tables(engine)

    client = Client(API_TOKEN, engine)
    client.build_application()
