
from debian:stretch

COPY 01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends \
        python2.7 locales ca-certificates adduser curl gnupg

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales


RUN apt-get clean && \
    rm -rf /root/.cache && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /etc/dpkg/dpkg.cfg.d/02apt-speedup && \
    rm -rf /var/cache/debconf/*-old && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/man/* /usr/share/groff/* /usr/share/info/* && \
    rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/*


CMD ["/bin/bash", "-c", "while true; do sleep 1493928090; done"]
