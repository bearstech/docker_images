
from debian:wheezy

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python2.7 ca-certificates adduser curl gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale \
    dpkg-reconfigure --frontend=noninteractive locales

CMD ["/bin/bash", "-c", "while true; do sleep 1493887548; done"]
