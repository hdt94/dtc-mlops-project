FROM python:3.8-slim

ENV APP_HOME /app
ENV PYTHONUNBUFFERED True

WORKDIR $APP_HOME

RUN pip install -U pip pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

COPY src/ ./
COPY templates/ ./templates/
CMD exec gunicorn --bind :$PORT app:app
