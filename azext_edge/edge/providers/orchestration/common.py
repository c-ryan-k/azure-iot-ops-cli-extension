# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from enum import Enum

# Urls
ARM_ENDPOINT = "https://management.azure.com/"
MCR_ENDPOINT = "https://mcr.microsoft.com/"
GRAPH_ENDPOINT = "https://graph.microsoft.com/"
GRAPH_V1_ENDPOINT = f"{GRAPH_ENDPOINT}v1.0"
GRAPH_V1_SP_ENDPOINT = f"{GRAPH_V1_ENDPOINT}/servicePrincipals"

CUSTOM_LOCATIONS_RP_APP_ID = "bc313c14-388c-4e7d-a58e-70017303ee3b"

CONTRIBUTOR_ROLE_ID = "b24988ac-6180-42a0-ab88-20f7382dd24c"

EXTENDED_LOCATION_ROLE_BINDING = "AzureArc-Microsoft.ExtendedLocation-RP-RoleBinding"
ARC_CONFIG_MAP = "azure-clusterconfig"
ARC_NAMESPACE = "azure-arc"

PROVISIONING_STATE_SUCCESS = "Succeeded"

# Key Vault KPIs
KEYVAULT_CLOUD_API_VERSION = "2022-07-01"

# Custom Locations KPIs
CUSTOM_LOCATIONS_API_VERSION = "2021-08-31-preview"

AIO_INSECURE_LISTENER_NAME = "default-insecure"
AIO_INSECURE_LISTENER_SERVICE_NAME = "aio-broker-insecure"
AIO_INSECURE_LISTENER_SERVICE_PORT = 1883

TRUST_ISSUER_KIND_KEY = "issuerKind"
TRUST_SETTING_KEYS = ["issuerName", TRUST_ISSUER_KIND_KEY, "configMapName", "configMapKey"]

EXTENSION_TYPE_PLATFORM = "microsoft.iotoperations.platform"
EXTENSION_TYPE_OSM = "microsoft.openservicemesh"
EXTENSION_TYPE_ACS = "microsoft.arc.containerstorage"
EXTENSION_TYPE_SSC = "microsoft.azure.secretstore"
EXTENSION_TYPE_OPS = "microsoft.iotoperations"

OPS_EXTENSION_DEPS = frozenset([EXTENSION_TYPE_PLATFORM, EXTENSION_TYPE_SSC, EXTENSION_TYPE_ACS])

EXTENSION_TYPE_TO_MONIKER_MAP = {
    EXTENSION_TYPE_PLATFORM: "platform",
    EXTENSION_TYPE_OSM: "openServiceMesh",
    EXTENSION_TYPE_ACS: "containerStorage",
    EXTENSION_TYPE_SSC: "secretStore",
    EXTENSION_TYPE_OPS: "iotOperations",
}

EXTENSION_MONIKER_TO_ALIAS_MAP = {
    "platform": "plat",
    "openServiceMesh": "osm",
    "secretStore": "ssc",
    "containerStorage": "acs",
    "iotOperations": "ops",
}

EXTENSION_ALIAS_TO_TYPE_MAP = {
    "plat": EXTENSION_TYPE_PLATFORM,
    "osm": EXTENSION_TYPE_OSM,
    "ssc": EXTENSION_TYPE_SSC,
    "acs": EXTENSION_TYPE_ACS,
    "ops": EXTENSION_TYPE_OPS,
}


class ClusterConnectStatus(Enum):
    CONNECTED = "Connected"


class MqMode(Enum):
    auto = "auto"
    distributed = "distributed"


class MqMemoryProfile(Enum):
    tiny = "Tiny"
    low = "Low"
    medium = "Medium"
    high = "High"


class MqServiceType(Enum):
    CLUSTERIP = "ClusterIp"
    LOADBALANCER = "LoadBalancer"
    NODEPORT = "NodePort"


class KubernetesDistroType(Enum):
    k3s = "K3s"
    k8s = "K8s"
    microk8s = "MicroK8s"


class IdentityUsageType(Enum):
    dataflow = "dataflow"


class SchemaType(Enum):
    """value is user friendly, full_value is the service friendly"""

    message = "message"

    @property
    def full_value(self) -> str:
        type_map = {SchemaType.message: "MessageSchema"}
        return type_map[self]


class SchemaFormat(Enum):
    """value is user friendly, full_value is the service friendly"""

    json = "json"
    delta = "delta"

    @property
    def full_value(self) -> str:
        format_map = {SchemaFormat.json: "JsonSchema/draft-07", SchemaFormat.delta: "Delta/1.0"}
        return format_map[self]


class ConfigSyncModeType(Enum):
    ADD = "add"
    FULL = "full"
    NONE = "none"


class ListenerProtocol(Enum):
    MQTT = "Mqtt"
    WEBSOCKETS = "WebSockets"


class TlsKeyAlgo(Enum):
    EC256 = "Ec256"
    EC384 = "Ec384"
    EC521 = "Ec521"
    ED25519 = "Ed25519"
    RSA2048 = "Rsa2048"
    RSA4096 = "Rsa4096"
    RSA8192 = "Rsa8192"


class TlsKeyRotation(Enum):
    ALWAYS = "Always"
    NEVER = "Never"


class DataflowOperationType(Enum):
    SOURCE = "Source"
    TRANSFORMATION = "BuiltInTransformation"
    DESTINATION = "Destination"


class DataflowEndpointType(Enum):
    DATAEXPLORER = "DataExplorer"
    DATALAKESTORAGE = "DataLakeStorage"
    FABRICONELAKE = "FabricOneLake"
    KAFKA = "Kafka"
    LOCALSTORAGE = "LocalStorage"
    MQTT = "Mqtt"


class DataflowEndpointAuthenticationType(Enum):
    ACCESSTOKEN = "AccessToken"
    ANONYMOUS = "Anonymous"
    SASL = "Sasl"
    SERVICEACCESSTOKEN = "ServiceAccountToken"
    SYSTEMASSIGNED = "SystemAssignedManagedIdentity"
    USERASSIGNED = "UserAssignedManagedIdentity"
    X509 = "X509Certificate"


class DataflowEndpointFabricPathType(Enum):
    FILES = "Files"
    TABLES = "Tables"


DATAFLOW_ENDPOINT_AUTHENTICATION_TYPE_MAP = {
    DataflowEndpointType.DATAEXPLORER.value: {
        DataflowEndpointAuthenticationType.SYSTEMASSIGNED.value,
        DataflowEndpointAuthenticationType.USERASSIGNED.value,
    },
    DataflowEndpointType.DATALAKESTORAGE.value: {
        DataflowEndpointAuthenticationType.SYSTEMASSIGNED.value,
        DataflowEndpointAuthenticationType.USERASSIGNED.value,
        DataflowEndpointAuthenticationType.ACCESSTOKEN.value,
    },
    DataflowEndpointType.FABRICONELAKE.value: {
        DataflowEndpointAuthenticationType.SYSTEMASSIGNED.value,
        DataflowEndpointAuthenticationType.USERASSIGNED.value,
    },
    DataflowEndpointType.KAFKA.value: {
        DataflowEndpointAuthenticationType.SYSTEMASSIGNED.value,
        DataflowEndpointAuthenticationType.USERASSIGNED.value,
        DataflowEndpointAuthenticationType.SASL.value,
        DataflowEndpointAuthenticationType.X509.value,
        DataflowEndpointAuthenticationType.ANONYMOUS.value,
    },
    DataflowEndpointType.MQTT.value: {
        DataflowEndpointAuthenticationType.SYSTEMASSIGNED.value,
        DataflowEndpointAuthenticationType.USERASSIGNED.value,
        DataflowEndpointAuthenticationType.SERVICEACCESSTOKEN.value,
        DataflowEndpointAuthenticationType.X509.value,
        DataflowEndpointAuthenticationType.ANONYMOUS.value,
    },
}

DATAFLOW_ENDPOINT_TYPE_REQUIRED_PARAMS = {
    DataflowEndpointType.DATAEXPLORER.value: {"database_name", "host"},
    DataflowEndpointType.DATALAKESTORAGE.value: {"host"},
    DataflowEndpointType.FABRICONELAKE.value: {"lakehouse_name", "workspace_name", "path_type", "host"},
    DataflowEndpointType.KAFKA.value: {"host"},
    DataflowEndpointType.LOCALSTORAGE.value: {"pvc_reference"},
    DataflowEndpointType.MQTT.value: {"host"},
}

DATAFLOW_ENDPOINT_TYPE_SETTINGS = {
    DataflowEndpointType.DATAEXPLORER.value: "dataExplorerSettings",
    DataflowEndpointType.DATALAKESTORAGE.value: "dataLakeStorageSettings",
    DataflowEndpointType.FABRICONELAKE.value: "fabricOneLakeSettings",
    DataflowEndpointType.KAFKA.value: "kafkaSettings",
    DataflowEndpointType.LOCALSTORAGE.value: "localStorageSettings",
    DataflowEndpointType.MQTT.value: "mqttSettings",
}

AUTHENTICATION_TYPE_REQUIRED_PARAMS = {
    DataflowEndpointAuthenticationType.SYSTEMASSIGNED.value: {},
    DataflowEndpointAuthenticationType.USERASSIGNED.value: {"client_Id", "tenant_id"},
    DataflowEndpointAuthenticationType.SERVICEACCESSTOKEN.value: {"audience"},
    DataflowEndpointAuthenticationType.X509.value: {"secret_name"},
    DataflowEndpointAuthenticationType.ANONYMOUS.value: {},
}

DATAFLOW_OPERATION_TYPE_SETTINGS = {
    DataflowOperationType.SOURCE.value: "sourceSettings",
    DataflowOperationType.TRANSFORMATION.value: "builtInTransformationSettings",
    DataflowOperationType.DESTINATION.value: "destinationSettings",
}


X509_ISSUER_REF_KEYS = ["group", "kind", "name"]

# Clone
CLONE_INSTANCE_VERS_MAX = "1.2.0"
CLONE_INSTANCE_VERS_MIN = "1.0.34"


class CloneSummaryMode(Enum):
    SIMPLE = "simple"
    DETAILED = "detailed"


class CloneTemplateMode(Enum):
    NESTED = "nested"
    LINKED = "linked"


class CloneTemplateParams(Enum):
    INSTANCE_NAME = "instanceName"
    CLUSTER_NAME = "clusterName"
    CLUSTER_NAMESPACE = "clusterNamespace"
    CUSTOM_LOCATION_NAME = "customLocationName"
    OPS_EXTENSION_NAME = "opsExtensionName"
    SCHEMA_REGISTRY_ID = "schemaRegistryId"
    RESOURCE_SLUG = "resourceSlug"
    LOCATION = "location"
    APPLY_ROLE_ASSIGNMENTS = "applyRoleAssignments"
