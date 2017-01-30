
from bearstech/nukai:debian-stretch-python3

RUN apt-get install -y \
        build-essential python3-dev python-virtualenv && \
    apt-get clean
RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python3 /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ["/bin/bash", "-c", "while true; do sleep 99999999999999; done"]
