#!/usr/bin/env bash

# wait-for-it -s "$DB_HOST:5432" -t 60

#fastapi dev /srv/app/core/main.py
uvicorn core.main:app --host 0.0.0.0 --port 8080 --reload