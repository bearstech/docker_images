
from bearstech/nukai:debian-stretch-python2

RUN apt-get install -y \
        build-essential python2.7-dev python-virtualenv && \
    apt-get clean
RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python2.7 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ['bash', '-c', 'while true; do sleep 9999999999999999999; done']
