#!/bin/bash

docker rmi -f $(docker images | grep nukai | awk '{print $3}' | xargs)
