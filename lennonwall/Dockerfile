FROM python:3.7-alpine

RUN addgroup user && adduser -h /home/user -D user -G user -s /bin/sh

COPY . /usr/src/app/lennonwall

WORKDIR /usr/src/app/lennonwall

RUN apk update \
    && apk add gcc libc-dev linux-headers \
    && apk add libffi-dev python-dev libevent-dev libressl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8080

CMD ["/usr/local/bin/uwsgi", "--ini", "server.ini"]
