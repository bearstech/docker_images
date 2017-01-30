
from debian:stretch

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python3 && \
    apt-get clean

CMD ["/bin/bash", "-c", "while true; do sleep 99999999999999; done"]
