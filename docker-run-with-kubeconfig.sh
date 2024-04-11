export azext_edge_cluster=musical-fishstick-4jgr4vq5vrrfj6jj
export azext_edge_rg=ops-cli-int-test-rg
export azext_edge_kv=
export config_path=/root/.kube/config
export local_config="C:\Users\rykelly\.kube\config"

# init steps

docker run --env azext_edge_rg=$azext_edge_rg --env azext_edge_cluster=$azext_edge_cluster --env azext_edge_skip_init=True --env KUBECONFIG= -v $local_config:$config_path:ro azure/azure-iot-ops-cli-test