# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from typing import Any, Dict, List

from azure.cli.core.azclierror import ArgumentUsageError
from rich.console import Console

from ..common import CheckTaskStatus, ListableEnum, OpsServiceType
from .check.base import check_pre_deployment, process_as_list
from .check.common import ResourceOutputDetailLevel
from .check.dataprocessor import check_dataprocessor_deployment
from .check.deviceregistry import check_deviceregistry_deployment
from .check.lnm import check_lnm_deployment
from .check.mq import check_mq_deployment
from .check.opcua import check_opcua_deployment
from .edge_api.dataprocessor import DataProcessorResourceKinds
from .edge_api.deviceregistry import DeviceRegistryResourceKinds
from .edge_api.lnm import LnmResourceKinds
from .edge_api.mq import MqResourceKinds
from .check.akri import check_akri_deployment
from .edge_api.akri import AkriResourceKinds
from .edge_api.opcua import OpcuaResourceKinds

console = Console(width=100, highlight=False)


def run_checks(
    detail_level: int = ResourceOutputDetailLevel.summary.value,
    ops_service: str = OpsServiceType.mq.value,
    pre_deployment: bool = True,
    post_deployment: bool = True,
    as_list: bool = False,
    resource_kinds: List[str] = None,
    resource_name: str = None,
) -> Dict[str, Any]:
    result = {}

    # check if the resource_kinds are valid for the requested service
    if resource_kinds:
        _validate_resource_kinds_under_service(ops_service, resource_kinds)

    with console.status(status="Analyzing cluster...", refresh_per_second=12.5):
        from time import sleep

        sleep(0.5)

        result["title"] = f"Evaluation for {{[bright_blue]{ops_service}[/bright_blue]}} service deployment"

        if pre_deployment:
            check_pre_deployment(result, as_list)
        if post_deployment:
            result["postDeployment"] = []
            service_check_dict = {
                OpsServiceType.akri.value: check_akri_deployment,
                OpsServiceType.mq.value: check_mq_deployment,
                OpsServiceType.dataprocessor.value: check_dataprocessor_deployment,
                OpsServiceType.deviceregistry.value: check_deviceregistry_deployment,
                OpsServiceType.lnm.value: check_lnm_deployment,
                OpsServiceType.opcua.value: check_opcua_deployment,
            }
            service_check_dict[ops_service](
                detail_level=detail_level,
                resource_name=resource_name,
                result=result,
                as_list=as_list,
                resource_kinds=resource_kinds
            )

        if as_list:
            return process_as_list(console=console, result=result) if as_list else result
        return result


def check_node_readiness():
    from kubernetes import client
    from kubernetes.client.models import V1NodeList, V1Node, V1NodeStatus, V1NodeSystemInfo, V1ObjectMeta
    from kubernetes.utils import parse_quantity
    core_client = client.CoreV1Api()
    nodes: V1NodeList = core_client.list_node()

    if not nodes or not nodes.items:
        raise Exception("this cluster has no nodes")

    is_multinode = len(nodes.items) > 1
    # to verify:
    node_count_status = CheckTaskStatus.warning.value if is_multinode else CheckTaskStatus.success.value
    # single node green / multi-node yellow?
    # for each node, verify:
    node: V1Node
    for node in nodes.items:
        metadata = node.metadata
        status = node.status
        info = status.node_info
        arch = info.architecture  # kernelversion, osimage, kubeletversion, OS
        capacity: dict = status.capacity

        # 16GB memory (single node, multi-node may be higher)
        memory_capacity = int(parse_quantity(capacity.get("memory")) / 1024 / 1024 / 1024)  # "memory": "16365028Ki"

        # 4 vCPU (single node, multi-node may be higher)
        cpu_capacity = parse_quantity(capacity.get("cpu"))  # "cpu": "4"

        # 30GB storage
        storage_capacity = int(parse_quantity(capacity.get("ephemeral-storage")) / 1024 / 1024 / 1024)  # "ephemeral-storage": "32847680Ki"

        print(f"Node - {metadata.name}")
        print(f"Architecture - {arch}")
        print(f"CPU - {cpu_capacity}")
        print(f"Memory - {memory_capacity}")
        print(f"Storage - {storage_capacity}")

    pass


def _validate_resource_kinds_under_service(ops_service: str, resource_kinds: List[str]) -> None:
    service_kinds_dict: Dict[str, ListableEnum] = {
        OpsServiceType.akri.value: AkriResourceKinds,
        OpsServiceType.dataprocessor.value: DataProcessorResourceKinds,
        OpsServiceType.deviceregistry.value: DeviceRegistryResourceKinds,
        OpsServiceType.mq.value: MqResourceKinds,
        OpsServiceType.lnm.value: LnmResourceKinds,
        OpsServiceType.opcua.value: OpcuaResourceKinds,
    }

    valid_resource_kinds = service_kinds_dict[ops_service].list() if ops_service in service_kinds_dict else []

    for resource_kind in resource_kinds:
        if resource_kind not in valid_resource_kinds:
            raise ArgumentUsageError(
                f"Resource kind {resource_kind} is not supported for service {ops_service}. "
                f"Allowed resource kinds for this service are {valid_resource_kinds}"
            )
