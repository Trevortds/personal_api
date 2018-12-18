FROM python:3.6-alpine

RUN adduser -D manager

WORKDIR /home/manager

RUN apk --update add --virtual build-dependencies gcc musl-dev freetype-dev libpng libffi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apk del build-dependencies gcc musl-dev

COPY app app
COPY migrations migrations
COPY flask_app.py config.py boot.sh ./

RUN chmod +x boot.sh

ENV FLASK_APP flask_app.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DATA_DIR=/home/manager/data


RUN chown -R manager:manager ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]