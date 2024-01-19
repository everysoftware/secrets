# Используйте официальный образ Python
FROM python:3.11.2
LABEL authors="everysoftware"

# Установите рабочую директорию в контейнере
WORKDIR /app

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/backend
ENV ENVLOADED 1

# Установите зависимости
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Копируйте проект
COPY .. /app

# Запустите сервер
CMD alembic upgrade head && gunicorn $API_APP -w 1 -k uvicorn.workers.UvicornWorker --bind=$API_HOST:$API_PORT
