
from debian:jessie

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python3 ca-certificates curl && \
    apt-get clean

CMD ["/bin/bash", "-c", "while true; do sleep 99999999999999; done"]
