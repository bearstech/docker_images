
from debian:jessie

COPY build.sh /docker_build.sh

RUN bash /docker_build.sh 2.7 && bash /docker_clean.sh

CMD ["/bin/bash", "-c", "while true; do sleep 1493932577; done"]
