
from debian:jessie

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python3 ca-certificates adduser curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "while true; do sleep 99999999999999; done"]
