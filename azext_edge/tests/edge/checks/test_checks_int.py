import pytest
from yaml import safe_load
from os import environ
from azext_edge.edge.common import OpsServiceType
from azext_edge.edge.providers.check.common import ResourceOutputDetailLevel
from azext_edge.edge.providers.checks import run_checks

ALL_BOOLS = [True, False]
NAMESPACE = "azure-iot-operations"
MQTT_CERT_NAME = "mqtt-bridge-cert"
MQTT_ENDPOINT = environ.get("MQTT_EVENTGRID_ENDPOINT", "")
TENANT_ID = environ.get("TENANT_ID", "")
KEYVAULT_NAME = environ.get("KEYVAULT_NAME", "")


def generate_keyvault_cert_auth():
    return f"""
        keyVault:
          vault:
            name: {KEYVAULT_NAME}
            directoryId: {TENANT_ID}
            credentials:
              servicePrincipalLocalSecretName: {NAMESPACE}
          vaultCert:
            name: {MQTT_CERT_NAME}
"""


MQTT_BRIDGE = safe_load(
    f"""
apiVersion: mq.iotoperations.azure.com/v1beta1
kind: MqttBridgeConnector
metadata:
  name: test-mqtt-bridge
  namespace: {NAMESPACE}
spec:
  image: 
    repository: mcr.microsoft.com/azureiotoperations/mqttbridge 
    tag: 0.1.0-preview
    pullPolicy: IfNotPresent
  protocol: v5
  bridgeInstances: 1
  clientIdPrefix: factory-gateway-
  logLevel: debug
  remoteBrokerConnection:
    endpoint: {MQTT_ENDPOINT}
    tls:
      tlsEnabled: true
    authentication:
      x509:
        {generate_keyvault_cert_auth()}
  localBrokerConnection:
    endpoint: aio-mq-dmqtt-frontend:8883
    tls:
      tlsEnabled: true
      trustedCaCertificateConfigMap: aio-ca-trust-bundle-test-only
    authentication:
      kubernetes: {{}}
"""
)

MQTT_TOPIC_MAP = "test_configs/mqtttopicmap.yml"


@pytest.mark.parametrize("detail_level", ResourceOutputDetailLevel.list())
@pytest.mark.parametrize("as_list", ALL_BOOLS)
@pytest.mark.parametrize("create_custom_resource", [[MQTT_BRIDGE, MQTT_TOPIC_MAP]], indirect=True)
def test_mq_checks(setup_secret_provider, create_custom_resource, detail_level, as_list):
    test = run_checks(
        detail_level=detail_level,
        as_list=as_list,
        ops_service=OpsServiceType.mq.value,
        pre_deployment=False,
        post_deployment=True,
    )
