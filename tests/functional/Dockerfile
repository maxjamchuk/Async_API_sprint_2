FROM python:3.10-slim-buster

ENV PYTHONPATH=./
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./ /tests/functional/

RUN pip install --no-cache-dir -r /tests/functional/requirements.txt