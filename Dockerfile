
from debian:jessie

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python2.7 && \
    apt-get clean

CMD ['bash', '-c', 'while true; do sleep 9999999999999999999; done']
