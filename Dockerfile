
from bearstech/nukai:debian-jessie-python3

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential python3-dev python-virtualenv

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python3 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

RUN apt-clean && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /etc/dpkg/dpkg.cfg.d/02apt-speedup && \
    rm -rf /usr/share/locale/* && \
    rm -rf /var/cache/debconf/*-old && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/*

CMD ["/bin/bash", "-c", "while true; do sleep 1493923575; done"]
