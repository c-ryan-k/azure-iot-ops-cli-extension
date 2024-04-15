export azext_edge_cluster="musical-fishstick-4jgr4vq5vrrfj6jj"
export azext_edge_rg="ops-cli-int-test-rg"
export azext_edge_kv=""
export config_path="/root/.kube/config"
export local_config="C:\Users\rykelly\.kube\config"

export AZURE_TENANT_ID=""
export AZURE_CLIENT_ID=""
export AIO_CLUSTER_NAME=""
export AIO_RG_NAME=""
export AIO_KV_ID=""
export AIO_SP_APP_ID=""
export AIO_SP_OBJECT_ID=""
export AIO_SP_SECRET=""
export CUSTOM_LOCATIONS_OID=""

# init steps

docker run --env azext_edge_rg=$azext_edge_rg --env azext_edge_cluster=$azext_edge_cluster --env azext_edge_skip_init=True --env KUBECONFIG= -v $local_config:$config_path:ro azure/azure-iot-ops-cli-test