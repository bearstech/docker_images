
from bearstech/nukai:debian-jessie-python3

RUN apt-get update && apt-get install -y \
        build-essential python3-dev python-virtualenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python3 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ["/bin/bash", "-c", "while true; do sleep 1493922554; done"]
