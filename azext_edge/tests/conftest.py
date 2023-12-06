# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

import pytest
import os


from .helpers import create_spc_yaml
from ..edge.providers.base import DEFAULT_NAMESPACE, create_namespaced_custom_objects
from ..edge.providers.edge_api.keyvault import KEYVAULT_API_V1
from ..edge.providers.orchestration.work import CLUSTER_SECRET_CLASS_NAME

SECRET_PROVIDER_VALUES = [
    ("azure-iot-operations", "secret"),
    ("kafka-connector-auth", "secret"),
    ("datalake-sas", "secret"),
    ("mqtt-bridge-cert", "cert"),
]

TENANT_ID = os.environ.get("TENANT_ID", "")
KEYVAULT_NAME = os.environ.get("KEYVAULT_NAME", "")
SPC_PLURAL = "secretproviderclasses"

@pytest.fixture(scope="session")
def create_custom_resource(request):
    from kubernetes import client, config, dynamic

    config.load_kube_config()

    # Dynamic API client workaround for utils.create_from_yaml not processing CRDs
    # https://github.com/kubernetes-client/python/issues/1792#issuecomment-1127393010
    DYNAMIC_CLIENT = dynamic.DynamicClient(
        client.api_client.ApiClient()
    )
    resource = request.param
    api_version = resource.get("apiVersion")
    kind = resource.get("kind")
    resource_name = resource.get("metadata").get("name")
    namespace = resource.get("metadata").get("namespace")
    crd_api = DYNAMIC_CLIENT.resources.get(api_version=api_version, kind=kind)

    try:
        crd_api.get(namespace=namespace, name=resource_name)
        crd_api.patch(body=resource, content_type="application/merge-patch+json")
    except dynamic.exceptions.NotFoundError:
        crd_api.create(body=resource, namespace=namespace)


@pytest.fixture(scope="session", autouse=True)
def setup_secret_provider():
    from kubernetes import config

    # load kubeconfig
    config.load_kube_config()

    # define the SPC with secrets
    secrets_config = create_spc_yaml(
        keyvault_name=KEYVAULT_NAME,
        name=CLUSTER_SECRET_CLASS_NAME,
        namespace=DEFAULT_NAMESPACE,
        secrets=SECRET_PROVIDER_VALUES,
        tenantId=TENANT_ID
    )

    # update SPC
    create_namespaced_custom_objects(
        group=KEYVAULT_API_V1.group,
        version=KEYVAULT_API_V1.version,
        plural=SPC_PLURAL,
        namespace=DEFAULT_NAMESPACE,
        yaml_objects=[secrets_config],
        delete_first=True,
    )


# Sets current working directory to the directory of the executing file
@pytest.fixture
def set_cwd(request):
    os.chdir(os.path.dirname(os.path.abspath(str(request.fspath))))


@pytest.fixture
def mocked_get_subscription_id(mocker):
    from .generators import get_zeroed_subscription

    patched = mocker.patch("azure.cli.core.commands.client_factory.get_subscription_id", autospec=True)
    patched.return_value = get_zeroed_subscription()
    yield patched


@pytest.fixture
def mocked_cmd(mocker, mocked_get_subscription_id):
    az_cli_mock = mocker.patch("azure.cli.core.AzCli", autospec=True)
    config = {"cli_ctx": az_cli_mock}
    patched = mocker.patch("azure.cli.core.commands.AzCliCommand", autospec=True, **config)
    yield patched


@pytest.fixture
def mocked_send_raw_request(request, mocker):
    request_mock = mocker.Mock()
    raw_request_result = getattr(request, "param", {})
    request_mock.content = True
    if raw_request_result.get("side_effect"):
        request_mock.json.side_effect = raw_request_result["side_effect"]
        request_mock.json.side_effect_values = raw_request_result["side_effect"]
    if raw_request_result.get("return_value"):
        request_mock.json.return_value = raw_request_result["return_value"]
    patched = mocker.patch("azure.cli.core.util.send_raw_request", autospec=True)
    patched.return_value = request_mock
    yield patched
