
from bearstech/nukai:debian-wheezy-python2

RUN apt-get update && apt-get install -y \
        build-essential python2.7-dev python-virtualenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python2.7 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ["/bin/bash", "-c", "while true; do sleep 1493922554; done"]
