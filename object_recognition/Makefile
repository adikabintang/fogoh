IMAGE_NAME=fogoh-obj-recognition
PREFIX=adikabintang/fogoh-obj-recognition
TAG=latest

.PHONY: docker
docker:
	docker build -t $(IMAGE_NAME) .

.PHONY: push
push:
	docker tag $(IMAGE_NAME) $(PREFIX):$(TAG)
	docker push $(PREFIX):$(TAG)
