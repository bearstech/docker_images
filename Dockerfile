
from debian:jessie

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python2.7 ca-certificates adduser curl gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "while true; do sleep 1491909008; done"]
