# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /code/
