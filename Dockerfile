
from bearstech/nukai:debian-stretch-python3

RUN apt-get update && apt-get install -y \
        build-essential python3-dev python-virtualenv

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python3 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage


RUN apt-get clean && \
    rm -rf /root/.cache && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /etc/dpkg/dpkg.cfg.d/02apt-speedup && \
    rm -rf /var/cache/debconf/*-old && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/man/* /usr/share/groff/* /usr/share/info/* && \
    rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/*


CMD ["/bin/bash", "-c", "while true; do sleep 1493928332; done"]
