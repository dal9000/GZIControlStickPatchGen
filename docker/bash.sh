#!/bin/bash

docker run -it \
    -v $PWD:/code \
    -v /etc/passwd:/etc/passwd \
    -v /etc/group:/etc/group \
    -h wii-dev \
    --workdir /code \
    --user $(id -u):$(id -g) \
    --entrypoint "/bin/bash" \
    wii-dev