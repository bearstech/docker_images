
from debian:jessie

COPY 01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc
COPY build.sh /docker_build.sh
COPY clean.sh /docker_clean.sh

RUN bash /docker_build.sh 2.7 && bash /docker_clean.sh

CMD ["/bin/bash", "-c", "while true; do sleep 1493930969; done"]
