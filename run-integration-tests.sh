# vars
azext_edge_cluster="rykelly-docker-compose-cluster-local"
azext_edge_rg="ado-int-test-rg"

# create containers for cluster and tests
docker compose create

# start server
docker start azure-iot-ops-cli-extension-cluster-1

# grab kubeconfig
docker cp azure-iot-ops-cli-extension-cluster-1:/output/kubeconfig.yaml ~/.kube/config

# modify host to point to our cluster from test container
# sed 127.0.0.1 - whatever cluster is

# temp for local testing - activate az env
source env311/scripts/activate
az -v

# connect to ARC
az connectedk8s connect --name $azext_edge_cluster -g $azext_edge_rg
az connectedk8s enable-features --name $azext_edge_cluster -g $azext_edge_rg --features cluster-connect custom-locations

# verify kubeconfig
kubectl get all -A

# AIO TESTS

# start tests with kubeconfig from server
# docker run --env azext_edge_rg=$azext_edge_rg --env azext_edge_cluster=$azext_edge_cluster --env azext_edge_skip_init=True --env KUBECONFIG= -v ~/.kube/config:~/.kube/config:ro azure-iot-ops-cli-extension-tests-1