
from debian:jessie

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y python2.7
