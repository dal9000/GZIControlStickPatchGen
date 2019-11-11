#!/bin/bash

if [ -f docker/Dockerfile ]; then
    rm docker/Dockerfile
fi

sed "s/__USER__/$USER/g" < docker/Dockerfile.templ > docker/Dockerfile

docker tag wii-dev:latest wii-dev:previous
docker build -t wii-dev:latest docker/
docker image rm --force wii-dev:previous

rm docker/Dockerfile
