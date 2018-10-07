FROM python:2.7-alpine

ENV SLACK_API_TOKEN ""

RUN pip install slackclient

RUN pip install avro

VOLUME /scripts
