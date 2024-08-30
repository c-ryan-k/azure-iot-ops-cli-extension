# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from typing import List, Optional, Tuple

from ...util import url_safe_random_chars
from .template import (
    M2_ENABLEMENT_TEMPLATE,
    M2_INSTANCE_TEMPLATE,
    TemplateVer,
    get_basic_dataflow_profile,
)


class InitTargets:
    def __init__(
        self,
        cluster_name: str,
        resource_group_name: str,
        cluster_namespace: str = "azure-iot-operations",
        location: Optional[str] = None,
        custom_location_name: Optional[str] = None,
        disable_rsync_rules: Optional[bool] = None,
        instance_name: Optional[str] = None,
        instance_description: Optional[str] = None,
        enable_fault_tolerance: Optional[bool] = None,
        dataflow_profile_instances: int = 1,
        broker_config: Optional[dict] = None,
        add_insecure_listener: Optional[bool] = None,
        **_,
    ):
        self.cluster_name = cluster_name
        self.safe_cluster_name = self._sanitize_k8s_name(self.cluster_name)
        self.resource_group_name = resource_group_name
        self.cluster_namespace = self._sanitize_k8s_name(cluster_namespace)
        self.location = location
        self.custom_location_name = (
            self._sanitize_k8s_name(custom_location_name)
            or f"{self.safe_cluster_name}-{url_safe_random_chars(3).lower()}-ops-cl"
        )
        self.deploy_resource_sync_rules: bool = not disable_rsync_rules
        self.instance_name = self._sanitize_k8s_name(instance_name)
        self.instance_description = instance_description
        self.enable_fault_tolerance = enable_fault_tolerance
        self.dataflow_profile_instances = dataflow_profile_instances
        self.broker_config = broker_config
        self.add_insecure_listener = add_insecure_listener

    def _sanitize_k8s_name(self, name: str) -> str:
        if not name:
            return name
        sanitized = str(name)
        sanitized = sanitized.lower()
        sanitized = sanitized.replace("_", "-")
        return sanitized

    def _handle_apply_targets(
        self, param_to_target: dict, template_blueprint: TemplateVer
    ) -> Tuple[TemplateVer, dict]:
        template_copy = template_blueprint.copy()
        built_in_template_params = template_copy.parameters

        deploy_params = {}

        for param in param_to_target:
            if param in built_in_template_params and param_to_target[param]:
                deploy_params[param] = {"value": param_to_target[param]}

        return template_copy, deploy_params

    def get_ops_enablement_template(
        self,
    ) -> Tuple[dict, dict]:
        template, parameters = self._handle_apply_targets(
            param_to_target={
                "clusterName": self.cluster_name,
                "kubernetesDistro": "",
                "containerRuntimeSocket": "",
                "trustSource": "",
                # "trustBundleSettings": ""
                "schemaRegistryId": "",
            },
            template_blueprint=M2_ENABLEMENT_TEMPLATE,
        )
        return template.content, parameters

    def get_ops_instance_template(
        self,
    ) -> Tuple[dict, dict]:
        template, parameters = self._handle_apply_targets(
            param_to_target={
                "clusterName": self.cluster_name,
                "kubernetesDistro": "",
                "containerRuntimeSocket": "",
                "trustSource": "",
                # "trustBundleSettings": ""
                "schemaRegistryId": "",
            },
            template_blueprint=M2_INSTANCE_TEMPLATE,
        )

        content = template.content
        deploy_resources: List[dict] = content.get("resources", [])
        df_profile_instances = self.dataflow_profile_instances
        deploy_resources.append(get_basic_dataflow_profile(instance_count=df_profile_instances))

        if self.broker_config:
            broker_config = self.broker_config
            if "properties" in broker_config:
                broker_config = broker_config["properties"]
            broker: dict = template.get_resource_defs("Microsoft.IoTOperations/instances/brokers")
            broker["properties"] = broker_config

        if self.add_insecure_listener:
            # This solution entirely relies on the form of the "standard" template.
            # TODO - @digimaun - default resource names
            # TODO - @digimaun - new listener
            default_listener = template.get_resource_defs("Microsoft.IoTOperations/instances/brokers/listeners")
            if default_listener:
                ports: list = default_listener["properties"]["ports"]
                ports.append({"port": 1883})

        return content, parameters