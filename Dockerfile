
from bearstech/nukai:debian-wheezy-python2

RUN apt-get update && apt-get install -y \
        build-essential python2.7-dev python-virtualenv && \
    mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python2.7 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage && \
    bash /docker_clean.sh

CMD ["/bin/bash", "-c", "while true; do sleep 1494497084; done"]
