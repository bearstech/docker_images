
from debian:jessie

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y \
        python3 locales ca-certificates adduser curl gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "while true; do sleep 1493922554; done"]
