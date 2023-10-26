# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Private distribution for NDA customers only. Governed by license terms at https://preview.e4k.dev/docs/use-terms/
# --------------------------------------------------------------------------------------------

from typing import NamedTuple, Dict


class TemplateVer(NamedTuple):
    commit_id: str
    content: dict

    @property
    def component_vers(self):
        return self.content["variables"]["VERSIONS"]

    @property
    def content_ver(self):
        return self.content["contentVersion"]


class TemplateManager(NamedTuple):
    version_map: Dict[str, TemplateVer]


TEMPLATE_VER_1000 = TemplateVer(
    commit_id="",
    content={
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "_generator": {"name": "bicep", "version": "0.22.6.54827", "templateHash": "15061446158033430252"},
            "description": "This template deploys Azure IoT Operations.",
        },
        "parameters": {
            "clusterName": {"type": "string"},
            "clusterLocation": {
                "type": "string",
                "defaultValue": "[parameters('location')]",
                "allowedValues": ["eastus", "eastus2", "westus", "westus2", "westus3", "westeurope", "northeurope"],
            },
            "location": {
                "type": "string",
                "defaultValue": "[resourceGroup().location]",
                "allowedValues": ["eastus", "eastus2", "westus", "westus2", "westus3", "westeurope", "northeurope"],
            },
            "customLocationName": {"type": "string", "defaultValue": "[format('{0}-cl', parameters('clusterName'))]"},
            "simulatePLC": {"type": "bool", "defaultValue": False},
            "opcuaDiscoveryEndpoint": {"type": "string", "defaultValue": "opc.tcp://<NOT_SET>:<NOT_SET>"},
            "targetName": {
                "type": "string",
                "defaultValue": "[format('{0}-target', toLower(parameters('clusterName')))]",
            },
            "dataProcessorInstanceName": {
                "type": "string",
                "defaultValue": "[format('{0}-processor', toLower(parameters('clusterName')))]",
            },
            "mqServiceType": {
                "type": "string",
                "defaultValue": "clusterIp",
                "allowedValues": ["clusterIp", "loadBalancer", "nodePort"],
            },
            "dataProcessorSecrets": {
                "type": "object",
                "defaultValue": {
                    "secretProviderClassName": "aio-default-spc",
                    "servicePrincipalSecretRef": "aio-akv-sp",
                },
            },
            "mqSecrets": {
                "type": "object",
                "defaultValue": {
                    "enabled": True,
                    "secretProviderClassName": "aio-default-spc",
                    "servicePrincipalSecretRef": "aio-akv-sp",
                },
            },
            "opcUaBrokerSecrets": {
                "type": "object",
                "defaultValue": {"kind": "csi", "csiServicePrincipalSecretRef": "aio-akv-sp"},
            },
            "dataProcessorCardinality": {
                "type": "object",
                "defaultValue": {"readerWorker": 1, "runnerWorker": 1, "messageStore": 1},
            },
        },
        "variables": {
            "akri": {
                "opcUaDiscoveryDetails": '[format(\'opcuaDiscoveryMethod:\n  - asset:\n      endpointUrl: "{0}"\n      useSecurity: false\n      autoAcceptUntrustedCertificates: true\n      userName: "user1"\n      password: "password"  \n\', parameters(\'opcuaDiscoveryEndpoint\'))]'
            },
            "AIO_CLUSTER_RELEASE_NAMESPACE": "azure-iot-operations",
            "AIO_EXTENSION_SCOPE": {"cluster": {"releaseNamespace": "[variables('AIO_CLUSTER_RELEASE_NAMESPACE')]"}},
            "AIO_TRUST_CONFIG_MAP": "aio-ca-trust-bundle-test-only",
            "AIO_TRUST_ISSUER": "aio-ca-issuer",
            "AIO_TRUST_CONFIG_MAP_KEY": "ca.crt",
            "AIO_TRUST_SECRET_NAME": "aio-ca-key-pair-test-only",
            "OBSERVABILITY": {
                "genevaCollectorAddressNoProtocol": "[format('geneva-metrics-service.{0}.svc.cluster.local:4317', variables('AIO_CLUSTER_RELEASE_NAMESPACE'))]",
                "otelCollectorAddressNoProtocol": "[format('aio-otel-collector.{0}.svc.cluster.local:4317', variables('AIO_CLUSTER_RELEASE_NAMESPACE'))]",
                "otelCollectorAddress": "[format('http://aio-otel-collector.{0}.svc.cluster.local:4317', variables('AIO_CLUSTER_RELEASE_NAMESPACE'))]",
                "genevaCollectorAddress": "[format('http://geneva-metrics-service.{0}.svc.cluster.local:4317', variables('AIO_CLUSTER_RELEASE_NAMESPACE'))]",
            },
            "MQ_PROPERTIES": {
                "domain": "[format('aio-mq-dmqtt-frontend.{0}', variables('AIO_CLUSTER_RELEASE_NAMESPACE'))]",
                "port": 8883,
                "localUrl": "[format('mqtts://aio-mq-dmqtt-frontend.{0}:8883', variables('AIO_CLUSTER_RELEASE_NAMESPACE'))]",
                "name": "aio-mq-dmqtt-frontend",
                "satAudience": "aio-mq",
            },
            "VERSIONS": {
                "adr": "0.12.0",
                "opcUaBroker": "0.1.0-preview.4",
                "observability": "0.62.3",
                "mq": "0.1.0-preview-rc2",
                "akri": "0.1.0-preview-rc2",
                "aio": "0.45.1-buddy-20231018.2",
                "layeredNetworking": "0.1.0-alpha.4",
                "processor": "0.1.0-preview.13",
            },
            "TRAINS": {
                "mq": "dev",
                "aio": "dev",
                "processor": "dev",
                "adr": "private-preview",
                "akri": "private-preview",
                "layeredNetworking": "private-preview",
                "opcUaBroker": "helm",
                "observability": "helm",
            },
            "observability_helmChart": {
                "name": "aio-observability",
                "type": "helm.v3",
                "properties": {
                    "chart": {
                        "repo": "alicesprings.azurecr.io/helm/opentelemetry-collector",
                        "version": "[variables('VERSIONS').observability]",
                    },
                    "values": {
                        "mode": "deployment",
                        "fullnameOverride": "aio-otel-collector",
                        "config": {
                            "processors": {
                                "memory_limiter": {
                                    "limit_percentage": 80,
                                    "spike_limit_percentage": 10,
                                    "check_interval": "60s",
                                }
                            },
                            "receivers": {
                                "jaeger": None,
                                "prometheus": None,
                                "zipkin": None,
                                "otlp": {"protocols": {"grpc": {"endpoint": ":4317"}, "http": {"endpoint": ":4318"}}},
                            },
                            "exporters": {
                                "prometheus": {
                                    "endpoint": ":8889",
                                    "resource_to_telemetry_conversion": {"enabled": True},
                                }
                            },
                            "service": {
                                "extensions": ["health_check"],
                                "pipelines": {
                                    "metrics": {"receivers": ["otlp"], "exporters": ["prometheus"]},
                                    "logs": None,
                                    "traces": None,
                                },
                                "telemetry": None,
                            },
                            "extensions": {"memory_ballast": {"size_mib": 0}},
                        },
                        "resources": {"limits": {"cpu": "100m", "memory": "512Mi"}},
                        "ports": {
                            "metrics": {"enabled": True, "containerPort": 8889, "servicePort": 8889, "protocol": "TCP"},
                            "jaeger-compact": {"enabled": False},
                            "jaeger-grpc": {"enabled": False},
                            "jaeger-thrift": {"enabled": False},
                            "zipkin": {"enabled": False},
                        },
                    },
                },
            },
            "akri_daemonset": {
                "name": "akri-opcua-asset-discovery-daemonset",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "apps/v1",
                        "kind": "DaemonSet",
                        "metadata": {"name": "akri-opcua-asset-discovery-daemonset"},
                        "spec": {
                            "selector": {"matchLabels": {"name": "akri-opcua-asset-discovery"}},
                            "template": {
                                "metadata": {"labels": {"name": "akri-opcua-asset-discovery"}},
                                "spec": {
                                    "containers": [
                                        {
                                            "name": "akri-opcua-asset-discovery",
                                            "image": "[format('mcr.microsoft.com/opcuabroker/discovery-handler:{0}', variables('VERSIONS').opcUaBroker)]",
                                            "imagePullPolicy": "Always",
                                            "resources": {
                                                "requests": {"memory": "64Mi", "cpu": "10m"},
                                                "limits": {"memory": "300Mi", "cpu": "100m"},
                                            },
                                            "ports": [{"name": "discovery", "containerPort": 80}],
                                            "env": [
                                                {
                                                    "name": "POD_IP",
                                                    "valueFrom": {"fieldRef": {"fieldPath": "status.podIP"}},
                                                },
                                                {"name": "DISCOVERY_HANDLERS_DIRECTORY", "value": "/var/lib/akri"},
                                            ],
                                            "volumeMounts": [
                                                {"name": "discovery-handlers", "mountPath": "/var/lib/akri"}
                                            ],
                                        }
                                    ],
                                    "volumes": [{"name": "discovery-handlers", "hostPath": {"path": "/var/lib/akri"}}],
                                },
                            },
                        },
                    }
                },
            },
            "broker_fe_issuer_configuration": {
                "name": "mq-fe-issuer-configuration",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "cert-manager.io/v1",
                        "kind": "Issuer",
                        "metadata": {"name": "e4k-frontend-server"},
                        "spec": {"ca": {"secretName": "aio-ca-key-pair-test-only"}},
                    }
                },
            },
            "broker_diagnostics_configuration": {
                "name": "mq-default-diagnostics-configuration",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "mq.iotoperations.azure.com/v1beta1",
                        "kind": "DiagnosticService",
                        "metadata": {"name": "diagnostics"},
                        "spec": {
                            "image": {
                                "repository": "alicesprings.azurecr.io/diagnostics-service",
                                "tag": "[variables('VERSIONS').mq]",
                            },
                            "enableSelfCheck": True,
                            "logLevel": "info",
                            "logFormat": "text",
                        },
                    }
                },
            },
            "broker_listener_configuration": {
                "name": "mq-default-listener-configuration",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "mq.iotoperations.azure.com/v1beta1",
                        "kind": "BrokerListener",
                        "metadata": {"name": "listener"},
                        "spec": {
                            "serviceType": "[parameters('mqServiceType')]",
                            "authenticationEnabled": True,
                            "authorizationEnabled": False,
                            "brokerRef": "broker",
                            "port": 8883,
                            "tls": {"automatic": {"issuerRef": {"name": "e4k-frontend-server", "kind": "Issuer"}}},
                        },
                    }
                },
            },
            "broker_auth_configuration": {
                "name": "mq-default-auth-configuration",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "mq.iotoperations.azure.com/v1beta1",
                        "kind": "BrokerAuthentication",
                        "metadata": {"name": "authn"},
                        "spec": {
                            "listenerRef": ["listener"],
                            "authenticationMethods": [
                                {"sat": {"audiences": ["[variables('MQ_PROPERTIES').satAudience]"]}}
                            ],
                        },
                    }
                },
            },
            "broker_configuration": {
                "name": "mq-default-configuration",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "mq.iotoperations.azure.com/v1beta1",
                        "kind": "Broker",
                        "metadata": {"name": "broker"},
                        "spec": {
                            "authImage": {
                                "pullPolicy": "Always",
                                "repository": "alicesprings.azurecr.io/dmqtt-authentication",
                                "tag": "[variables('VERSIONS').mq]",
                            },
                            "brokerImage": {
                                "pullPolicy": "Always",
                                "repository": "alicesprings.azurecr.io/dmqtt-pod",
                                "tag": "[variables('VERSIONS').mq]",
                            },
                            "healthManagerImage": {
                                "pullPolicy": "Always",
                                "repository": "alicesprings.azurecr.io/dmqtt-operator",
                                "tag": "[variables('VERSIONS').mq]",
                            },
                            "diagnostics": {
                                "probeImage": "[format('alicesprings.azurecr.io/diagnostics-probe:{0}', variables('VERSIONS').mq)]",
                                "enableSelfCheck": True,
                            },
                            "mode": "distributed",
                            "memoryProfile": "medium",
                            "cardinality": {
                                "backendChain": {"partitions": 2, "workers": 2, "redundancyFactor": 2},
                                "frontend": {"replicas": 2, "workers": 2},
                            },
                        },
                    }
                },
            },
            "asset_configuration": {
                "name": "akri-opcua-asset",
                "type": "yaml.k8s",
                "properties": {
                    "resource": {
                        "apiVersion": "akri.sh/v0",
                        "kind": "Configuration",
                        "metadata": {"name": "akri-opcua-asset"},
                        "spec": {
                            "discoveryHandler": {
                                "name": "opcua-asset",
                                "discoveryDetails": "[variables('akri').opcUaDiscoveryDetails]",
                            },
                            "brokerProperties": {},
                            "capacity": 1,
                        },
                    }
                },
            },
            "opc_ua_broker_helmChart": {
                "type": "helm.v3",
                "name": "opc-ua-broker",
                "properties": {
                    "chart": {
                        "repo": "oci://mcr.microsoft.com/opcuabroker/helmchart/microsoft.iotoperations.opcuabroker",
                        "version": "[variables('VERSIONS').opcUaBroker]",
                    },
                    "values": {
                        "mqttBroker": {
                            "authenticationMethod": "serviceAccountToken",
                            "serviceAccountTokenAudience": "[variables('MQ_PROPERTIES').satAudience]",
                            "address": "[variables('MQ_PROPERTIES').localUrl]",
                            "caCertConfigMapRef": "[variables('AIO_TRUST_CONFIG_MAP')]",
                            "caCertKey": "[variables('AIO_TRUST_CONFIG_MAP_KEY')]",
                            "connectUserProperties": {"metriccategory": "aio-opc"},
                        },
                        "opcPlcSimulation": {"deploy": "[parameters('simulatePLC')]"},
                        "openTelemetry": {
                            "enabled": True,
                            "endpoints": {
                                "default": {
                                    "uri": "[variables('OBSERVABILITY').otelCollectorAddress]",
                                    "protocol": "grpc",
                                    "emitLogs": False,
                                    "emitMetrics": True,
                                    "emitTraces": False,
                                },
                                "geneva": {
                                    "uri": "[variables('OBSERVABILITY').genevaCollectorAddress]",
                                    "protocol": "grpc",
                                    "emitLogs": False,
                                    "emitMetrics": True,
                                    "emitTraces": False,
                                    "temporalityPreference": "delta",
                                },
                            },
                        },
                        "secrets": {
                            "kind": "[parameters('opcUaBrokerSecrets').kind]",
                            "csiServicePrincipalSecretRef": "[parameters('opcUaBrokerSecrets').csiServicePrincipalSecretRef]",
                            "csiDriver": "secrets-store.csi.k8s.io",
                        },
                    },
                },
            },
        },
        "resources": [
            {
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "azure-iot-operations",
                "identity": {"type": "SystemAssigned"},
                "properties": {
                    "extensionType": "microsoft.iotoperations",
                    "version": "[variables('VERSIONS').aio]",
                    "releaseTrain": "[variables('TRAINS').aio]",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {
                        "rbac.cluster.admin": "true",
                        "aioTrust.enabled": "true",
                        "aioTrust.secretName": "[variables('AIO_TRUST_SECRET_NAME')]",
                        "aioTrust.configmapName": "[variables('AIO_TRUST_CONFIG_MAP')]",
                        "aioTrust.issuerName": "[variables('AIO_TRUST_ISSUER')]",
                        "Microsoft.CustomLocation.ServiceAccount": "default",
                        "otelCollectorAddress": "[variables('OBSERVABILITY').otelCollectorAddressNoProtocol]",
                        "genevaCollectorAddress": "[variables('OBSERVABILITY').genevaCollectorAddressNoProtocol]",
                    },
                },
            },
            {
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "assets",
                "properties": {
                    "extensionType": "microsoft.deviceregistry.assets",
                    "version": "[variables('VERSIONS').adr]",
                    "releaseTrain": "[variables('TRAINS').adr]",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {"Microsoft.CustomLocation.ServiceAccount": "default"},
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]"
                ],
            },
            {
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "mq",
                "identity": {"type": "SystemAssigned"},
                "properties": {
                    "extensionType": "microsoft.iotoperations.mq",
                    "version": "[variables('VERSIONS').mq]",
                    "releaseTrain": "[variables('TRAINS').mq]",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {
                        "global.quickstart": "false",
                        "global.openTelemetryCollectorAddr": "[variables('OBSERVABILITY').otelCollectorAddress]",
                        "secrets.enabled": "[parameters('mqSecrets').enabled]",
                        "secrets.secretProviderClassName": "[parameters('mqSecrets').secretProviderClassName]",
                        "secrets.servicePrincipalSecretRef": "[parameters('mqSecrets').servicePrincipalSecretRef]",
                    },
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]"
                ],
            },
            {
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "processor",
                "properties": {
                    "extensionType": "microsoft.iotoperations.dataprocessor",
                    "version": "[variables('VERSIONS').processor]",
                    "releaseTrain": "[variables('TRAINS').processor]",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {
                        "Microsoft.CustomLocation.ServiceAccount": "default",
                        "otelCollectorAddress": "[variables('OBSERVABILITY').otelCollectorAddressNoProtocol]",
                        "genevaCollectorAddress": "[variables('OBSERVABILITY').genevaCollectorAddressNoProtocol]",
                        "cardinality.readerWorker.replicas": "[parameters('dataProcessorCardinality').readerWorker]",
                        "cardinality.runnerWorker.replicas": "[parameters('dataProcessorCardinality').runnerWorker]",
                        "nats.config.cluster.replicas": "[parameters('dataProcessorCardinality').messageStore]",
                        "secrets.secretProviderClassName": "[parameters('dataProcessorSecrets').secretProviderClassName]",
                        "secrets.servicePrincipalSecretRef": "[parameters('dataProcessorSecrets').servicePrincipalSecretRef]",
                        "caTrust.enabled": "true",
                        "caTrust.configmapName": "[variables('AIO_TRUST_CONFIG_MAP')]",
                        "serviceAccountTokens.MQClient.audience": "[variables('MQ_PROPERTIES').satAudience]",
                    },
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]"
                ],
            },
            {
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "akri",
                "properties": {
                    "extensionType": "microsoft.iotoperations.akri",
                    "version": "[variables('VERSIONS').akri]",
                    "releaseTrain": "[variables('TRAINS').akri]",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {"webhookConfiguration.enabled": "false"},
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]"
                ],
            },
            {
                "condition": False,
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "opc-ua-broker",
                "properties": {
                    "extensionType": "microsoft.iotoperations.opcuabroker",
                    "version": "[variables('VERSIONS').opcUaBroker]",
                    "releaseTrain": "private-preview",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {
                        "mqttBroker.authenticationMethod": "serviceAccountToken",
                        "mqttBroker.serviceAccountTokenAudience": "[variables('MQ_PROPERTIES').satAudience]",
                        "mqttBroker.caCertConfigMapRef ": "[variables('AIO_TRUST_CONFIG_MAP')]",
                        "mqttBroker.caCertKey": "[variables('AIO_TRUST_CONFIG_MAP_KEY')]",
                        "mqttBroker.address": "[variables('MQ_PROPERTIES').localUrl]",
                        "mqttBroker.connectUserProperties.metriccategory": "aio-opc",
                        "opcPlcSimulation.deploy": "[format('{0}', parameters('simulatePLC'))]",
                        "openTelemetry.enabled": "true",
                        "openTelemetry.endpoints.default.uri": "[variables('OBSERVABILITY').otelCollectorAddress]",
                        "openTelemetry.endpoints.default.protocol": "grpc",
                        "openTelemetry.endpoints.default.emitLogs": "false",
                        "openTelemetry.endpoints.default.emitMetrics": "true",
                        "openTelemetry.endpoints.default.emitTraces": "false",
                        "openTelemetry.endpoints.geneva.uri": "[variables('OBSERVABILITY').genevaCollectorAddress]",
                        "openTelemetry.endpoints.geneva.protocol": "grpc",
                        "openTelemetry.endpoints.geneva.emitLogs": "false",
                        "openTelemetry.endpoints.geneva.emitMetrics": "true",
                        "openTelemetry.endpoints.geneva.emitTraces": "false",
                        "openTelemetry.endpoints.geneva.temporalityPreference": "delta",
                        "secrets.kind": "[parameters('opcUaBrokerSecrets').kind]",
                        "secrets.csiServicePrincipalSecretRef": "[parameters('opcUaBrokerSecrets').csiServicePrincipalSecretRef]",
                        "secrets.csiDriver": "secrets-store.csi.k8s.io",
                    },
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]"
                ],
            },
            {
                "type": "Microsoft.KubernetesConfiguration/extensions",
                "apiVersion": "2022-03-01",
                "scope": "[format('Microsoft.Kubernetes/connectedClusters/{0}', parameters('clusterName'))]",
                "name": "layered-networking",
                "properties": {
                    "extensionType": "microsoft.iotoperations.layerednetworkmanagement",
                    "version": "[variables('VERSIONS').layeredNetworking]",
                    "releaseTrain": "[variables('TRAINS').layeredNetworking]",
                    "autoUpgradeMinorVersion": False,
                    "scope": "[variables('AIO_EXTENSION_SCOPE')]",
                    "configurationSettings": {},
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]"
                ],
            },
            {
                "type": "Microsoft.ExtendedLocation/customLocations",
                "apiVersion": "2021-08-31-preview",
                "name": "[parameters('customLocationName')]",
                "location": "[parameters('clusterLocation')]",
                "properties": {
                    "hostResourceId": "[resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName'))]",
                    "namespace": "[variables('AIO_CLUSTER_RELEASE_NAMESPACE')]",
                    "displayName": "[parameters('customLocationName')]",
                    "clusterExtensionIds": [
                        "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]",
                        "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'assets')]",
                        "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'processor')]",
                    ],
                },
                "dependsOn": [
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'azure-iot-operations')]",
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'processor')]",
                    "[extensionResourceId(resourceId('Microsoft.Kubernetes/connectedClusters', parameters('clusterName')), 'Microsoft.KubernetesConfiguration/extensions', 'assets')]",
                ],
            },
            {
                "type": "Microsoft.ExtendedLocation/customLocations/resourceSyncRules",
                "apiVersion": "2021-08-31-preview",
                "name": "[format('{0}/{1}', parameters('customLocationName'), format('{0}-aio-sync', parameters('customLocationName')))]",
                "location": "[parameters('clusterLocation')]",
                "properties": {
                    "priority": 100,
                    "selector": {
                        "matchLabels": {"management.azure.com/provider-name": "microsoft.iotoperationsorchestrator"}
                    },
                    "targetResourceGroup": "[resourceGroup().id]",
                },
                "dependsOn": [
                    "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]"
                ],
            },
            {
                "type": "Microsoft.ExtendedLocation/customLocations/resourceSyncRules",
                "apiVersion": "2021-08-31-preview",
                "name": "[format('{0}/{1}', parameters('customLocationName'), format('{0}-adr-sync', parameters('customLocationName')))]",
                "location": "[parameters('clusterLocation')]",
                "properties": {
                    "priority": 200,
                    "selector": {"matchLabels": {"management.azure.com/provider-name": "Microsoft.DeviceRegistry"}},
                    "targetResourceGroup": "[resourceGroup().id]",
                },
                "dependsOn": [
                    "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]"
                ],
            },
            {
                "type": "Microsoft.ExtendedLocation/customLocations/resourceSyncRules",
                "apiVersion": "2021-08-31-preview",
                "name": "[format('{0}/{1}', parameters('customLocationName'), format('{0}-dp-sync', parameters('customLocationName')))]",
                "location": "[parameters('clusterLocation')]",
                "properties": {
                    "priority": 300,
                    "selector": {
                        "matchLabels": {"management.azure.com/provider-name": "microsoft.iotoperationsdataprocessor"}
                    },
                    "targetResourceGroup": "[resourceGroup().id]",
                },
                "dependsOn": [
                    "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]"
                ],
            },
            {
                "type": "Microsoft.IoTOperationsDataProcessor/instances",
                "apiVersion": "2023-10-04-preview",
                "name": "[parameters('dataProcessorInstanceName')]",
                "location": "[parameters('location')]",
                "extendedLocation": {
                    "name": "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]",
                    "type": "CustomLocation",
                },
                "properties": {},
                "dependsOn": [
                    "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]"
                ],
            },
            {
                "type": "Microsoft.IoTOperationsOrchestrator/Targets",
                "apiVersion": "2023-10-04-preview",
                "name": "[parameters('targetName')]",
                "location": "[parameters('location')]",
                "extendedLocation": {
                    "name": "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]",
                    "type": "CustomLocation",
                },
                "properties": {
                    "scope": "[variables('AIO_CLUSTER_RELEASE_NAMESPACE')]",
                    "version": "[deployment().properties.template.contentVersion]",
                    "components": [
                        "[variables('observability_helmChart')]",
                        "[variables('broker_configuration')]",
                        "[variables('broker_diagnostics_configuration')]",
                        "[variables('broker_listener_configuration')]",
                        "[variables('broker_auth_configuration')]",
                        "[variables('broker_fe_issuer_configuration')]",
                        "[variables('akri_daemonset')]",
                        "[variables('asset_configuration')]",
                        "[variables('opc_ua_broker_helmChart')]",
                    ],
                    "topologies": [
                        {
                            "bindings": [
                                {
                                    "role": "helm.v3",
                                    "provider": "providers.target.helm",
                                    "config": {"inCluster": "true"},
                                },
                                {
                                    "role": "yaml.k8s",
                                    "provider": "providers.target.kubectl",
                                    "config": {"inCluster": "true"},
                                },
                            ]
                        }
                    ],
                },
                "dependsOn": [
                    "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]"
                ],
            },
        ],
        "outputs": {
            "customLocationId": {
                "type": "string",
                "value": "[resourceId('Microsoft.ExtendedLocation/customLocations', parameters('customLocationName'))]",
            },
            "customLocationName": {"type": "string", "value": "[parameters('customLocationName')]"},
            "targetName": {"type": "string", "value": "[parameters('targetName')]"},
            "processorInstanceName": {"type": "string", "value": "[parameters('dataProcessorInstanceName')]"},
            "aioNamespace": {"type": "string", "value": "[variables('AIO_CLUSTER_RELEASE_NAMESPACE')]"},
            "mq": {"type": "object", "value": "[variables('MQ_PROPERTIES')]"},
            "observability": {"type": "object", "value": "[variables('OBSERVABILITY')]"},
        },
    },
)


_version_map = {"1.0.0.0": TEMPLATE_VER_1000}
TEMPLATE_MANAGER = TemplateManager(version_map=_version_map)
