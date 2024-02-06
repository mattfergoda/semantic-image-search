# syntax=docker/dockerfile:1

# Container image for the API

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Need this to avoid error with egg_info dependency.
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Copy this first to take advantage of caching.
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy this after since it changes more frequently.
COPY ./app /code/app

# Run the application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
