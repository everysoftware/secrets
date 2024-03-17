FROM python:3.11.2

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src
ENV ENVLOADED 1

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY .. /app

CMD alembic upgrade head && gunicorn $API_APP -w 1 -k uvicorn.workers.UvicornWorker --bind=$API_HOST:$API_PORT
