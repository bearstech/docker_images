
from debian:wheezy

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python2.7 ca-certificates adduser curl && \
    apt-get clean

CMD ["/bin/bash", "-c", "while true; do sleep 99999999999999; done"]
