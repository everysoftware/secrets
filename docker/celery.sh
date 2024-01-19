#!/bin/bash

cd backend/infrastructure || exit

if [[ "${1}" == "celery" ]]; then
  celery -A tasks.app:app worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery -A tasks.app:app flower
fi
