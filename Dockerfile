# Alpine base image that contains python 3.7
FROM python:3.7-alpine

MAINTAINER Loide Mara Verdes "mara.verdes@gmail.com"

RUN apk update \
    && apk upgrade

WORKDIR /usr/src/app
COPY src ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "./proxy.py" ]
