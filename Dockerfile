
from debian:jessie

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y python2.7

RUN apt-get install -y build-essential python2.7-dev python-virtualenv
RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python2.7 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage && \
