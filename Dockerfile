FROM python:3.12-alpine3.20
LABEL maintainer="cven28@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY . /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
