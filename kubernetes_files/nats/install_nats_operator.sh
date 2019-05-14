#/bin/sh
kubectl apply -f https://github.com/nats-io/nats-operator/releases/download/v0.4.3/00-prereqs.yaml
kubectl apply -f ./nats_operator/10-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/nats-io/nats-streaming-operator/master/deploy/default-rbac.yaml
kubectl apply -f ./nats_operator/deployment.yaml
kubectl apply -f ./nats.yaml