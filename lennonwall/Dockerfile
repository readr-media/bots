FROM python:3.7-alpine

RUN addgroup user && adduser -h /home/user -D user -G user -s /bin/sh

RUN mkdir -p /usr/src/app/lennonwall

COPY requirements.txt /usr/src/app/lennonwall

WORKDIR /usr/src/app/lennonwall

RUN apk update \
    && apk add gcc libc-dev linux-headers \
    && apk add libffi-dev python-dev libevent-dev libressl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /usr/src/app/lennonwall

EXPOSE 8080

CMD ["/usr/local/bin/uwsgi", "--ini", "server.ini"]
