#/bin/bash

pushd $PWD/kubernetes_files/nats
./install_nats_operator.sh
popd
k3s kubectl apply -f $PWD/kubernetes_files/deployment_and_svc/