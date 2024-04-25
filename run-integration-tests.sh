# vars
azext_edge_cluster="dockerize"
azext_edge_rg="ado-int-test-rg"

# create containers for cluster and tests
docker compose create

# start server
docker start azure-iot-ops-cli-extension-cluster-1

# grab kubeconfig from server and drop it on host
docker cp azure-iot-ops-cli-extension-cluster-1:/output/kubeconfig.yaml .

# todo - may not be needed with `--network host`
# modify host to point to our cluster from test container
# sed 127.0.0.1 - docker.host.internal

# connect to ARC
az connectedk8s connect --name $azext_edge_cluster -g $azext_edge_rg
az connectedk8s enable-features --name $azext_edge_cluster -g $azext_edge_rg --features cluster-connect custom-locations

# deploy AIO

# verify kubeconfig
kubectl get all -A

# AIO TESTS

# start tests with kubeconfig from host
docker run --network host --env azext_edge_rg=$azext_edge_rg --env azext_edge_cluster=$azext_edge_cluster --env azext_edge_skip_init=True --env KUBECONFIG=/root/.kube/config -v ./kubeconfig.yaml:/root/.kube/config:ro azure-iot-ops-cli-extension-tests-1