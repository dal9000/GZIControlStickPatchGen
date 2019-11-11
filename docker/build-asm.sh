#!/bin/bash

docker run -ti \
    -v $PWD/assembly:/assembly \
    -v /etc/passwd:/etc/passwd \
    -v /etc/group:/etc/group \
    -h wii-dev \
    --workdir /assembly \
    --user $(id -u):$(id -g) \
    --entrypoint "/usr/bin/make" \
    wii-dev $@
