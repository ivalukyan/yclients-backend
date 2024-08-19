FROM python:3.12-alpine3.20

RUN mkdir /backend_app
WORKDIR /backend_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .