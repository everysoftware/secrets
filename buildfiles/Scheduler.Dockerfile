FROM python:3.11.2

ENV DOCKER_MODE 1

# RUN apt-get update && apt-get -y upgrade

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

RUN chmod 755 .
COPY src/scheduler src/scheduler
COPY src/config.py src/config.py
