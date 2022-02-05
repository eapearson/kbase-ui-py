FROM python:3-alpine3.14

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache nodejs npm
COPY package.json  ./
RUN npm install

COPY ./django /usr/src/app/django

WORKDIR /usr/src/app/django