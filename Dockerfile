FROM python:3.10-slim-buster

ENV TZ=Europe/Helsinki

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV NOTIFICATION_BOT_TOKEN=$NOTIFICATION_BOT_TOKEN
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV TZ=$TZ

ENV PYTHONPATH=/code/

CMD ["python", "/code/main.py"]
