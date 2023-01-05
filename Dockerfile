FROM python:3.10-slim-buster

ENV TZ=Asia/Yerevan

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV NOTIFICATION_BOT_TOKEN=$NOTIFICATION_BOT_TOKEN

ENV PYTHONPATH=/code/

RUN python /code/db/deed.py

CMD ["python", "/code/main.py"]
