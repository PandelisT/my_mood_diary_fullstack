FROM ubuntu:latest

RUN apt-get update --fix-missing

RUN apt-get install python3.8 libpq-dev wait-for-it -y

WORKDIR /code

COPY src .

RUN apt-get install python3-pip -y

RUN pip3 install -r requirements.txt

ENV FLASK_APP=src/main:create_app

CMD ["gunicorn", "-b", "0.0.0.0", "-w", "3", "main:create_app()"]