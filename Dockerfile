
from bearstech/nukai:centos-7-python2

RUN yum install -y -q \
    python-devel python-virtualenv \
    make automake gcc gcc-c++ kernel-devel

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ["/bin/bash", "-c", "while true; do sleep 1494497084; done"]
