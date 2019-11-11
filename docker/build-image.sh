#!/bin/bash

if [ -f docker/image-files/Dockerfile ]; then
    rm docker/image-files/Dockerfile
fi

sed "s/__USER__/$USER/g" < docker/image-files/Dockerfile.templ > docker/image-files/Dockerfile

docker tag wii-dev:latest wii-dev:previous
docker build -t wii-dev:latest docker/image-files
docker image rm --force wii-dev:previous

rm docker/image-files/Dockerfile
