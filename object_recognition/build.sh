#/bin/bash

docker build -t fogoh-obj-recognition .
TAG=$(docker images | grep -w "^fogoh-obj-recognition" | awk '{print $3}')
docker tag $TAG adikabintang/fogoh-obj-recognition:latest
docker push adikabintang/fogoh-obj-recognition:latest
