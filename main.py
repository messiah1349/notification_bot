import os
from lib.client import Client
from sqlalchemy import create_engine

if __name__ == '__main__':

    API_TOKEN = os.environ["NOTIFICATION_BOT_TOKEN"]

    engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:1349/notification_bot',
                           connect_args={"options": "-c timezone=Asia/Yerevan"})
    client = Client(API_TOKEN, engine)
    client.build_application()
