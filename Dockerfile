FROM hassioaddons/base-python:latest

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh /
COPY Ding1.mp3 /
COPY DingDong1.mp3 /
COPY doorbell-server.py /

RUN chmod a+x /run.sh

CMD  /run.sh
