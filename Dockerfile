FROM pypy:3.8-slim-bullseye
LABEL org.opencontainers.image.authors="KBase Developer"

RUN apt-get update && apt-get upgrade && apt-get -y install nodejs npm

ENV PATH=/opt/pypy/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install Python dependencies
RUN mkdir -p /kb/tmp
RUN pypy3 -m ensurepip

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# RUN apk add --no-cache nodejs npm
COPY package.json  ./
RUN npm install

COPY ./django /usr/src/app/django

WORKDIR /usr/src/app/django