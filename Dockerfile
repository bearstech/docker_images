
from bearstech/nukai:debian-stretch-python3

RUN apt-get update && apt-get install -y \
        build-essential python3-dev python-virtualenv && \
    mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python3 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage && \
    bash /docker_clean.sh

CMD ["/bin/bash", "-c", "while true; do sleep 1493932178; done"]
