#/bin/bash

docker build -t fogoh-raw-video-pub .
TAG=$(docker images | grep -w "^fogoh-raw-video-pub" | awk '{print $3}')
docker tag $TAG adikabintang/fogoh-raw-video-pub:latest
docker push adikabintang/fogoh-raw-video-pub:latest

