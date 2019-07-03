ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache python3
RUN apk add --no-cache python3-dev

# Copy data for add-on
COPY run.sh /
COPY Ding1.mp3 /
COPY mp3-server.py /

RUN chmod a+x /run.sh

CMD  /run.sh
