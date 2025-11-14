# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

import os
import random
import secrets
import sys

import pytest
import responses


def pytest_configure(config):
    config.addinivalue_line("markers", "init_scenario_test: mark tests that will run az iot ops init.")
    config.addinivalue_line("markers", "no_global_setup: mark tests that will not use global setup.")
    
    # Seed random generators to ensure consistent test collection across pytest-xdist workers.
    # This is necessary because some tests use generate_random_string() in @pytest.mark.parametrize
    # decorators, which get evaluated during test collection. Without a consistent seed, each
    # worker would generate different random values, leading to test collection mismatches.
    #
    # The seed is generated randomly for each test run (using current time) unless explicitly set
    # via PYTEST_RANDOMLY_SEED environment variable for reproducibility.
    import time
    
    # Only generate a new seed in the main process (not in xdist workers)
    # Workers will inherit the seed from the main process via environment
    if 'PYTEST_RANDOMLY_SEED' not in os.environ:
        if os.environ.get('PYTEST_XDIST_WORKER') is None:
            # Main process: generate and set seed
            generated_seed = int(time.time() * 1000) % (2**31)
            os.environ['PYTEST_RANDOMLY_SEED'] = str(generated_seed)
    
    seed = int(os.environ.get('PYTEST_RANDOMLY_SEED', '42'))
    random.seed(seed)
    
    # Print the seed so test runs can be reproduced if needed (only in main process)
    if os.environ.get('PYTEST_XDIST_WORKER') is None:
        print(f"\nUsing random seed: {seed} (set PYTEST_RANDOMLY_SEED={seed} to reproduce)")
    
    # Replace secrets.choice with random.choice so it can be seeded
    secrets.choice = random.choice


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
def mocked_azcli_cred_get_token(mocker):
    from unittest.mock import PropertyMock

    patched = mocker.patch(
        "azure.identity._credentials.azure_cli.AzureCliCredential.get_token",
    )
    type(patched()).expires_on = PropertyMock(return_value=sys.maxsize)
    type(patched()).refresh_on = PropertyMock(return_value=sys.maxsize)
    yield patched


@pytest.fixture
def mocked_azcli_profile_get_raw_token(mocker):
    patched = mocker.patch(
        "azure.cli.core._profile.Profile.get_raw_token",
        autospec=True,
    )
    patched.return_value = (("Bearer", "token", None), None, None)
    yield patched


@pytest.fixture
def mocked_cmd(mocker, mocked_get_subscription_id, mocked_azcli_cred_get_token, mocked_azcli_profile_get_raw_token):
    class Stub:
        pass

    cloud = Stub()
    cloud.endpoints = Stub()
    cloud.endpoints.resource_manager = "https://management.azure.com/"
    cloud.endpoints.active_directory = "https://login.microsoftonline.com/"
    cloud.endpoints.active_directory_resource_id = "https://management.azure.com/"

    az_cli_mock = mocker.patch("azure.cli.core.AzCli", autospec=True, **{"data": {"command": "az"}, "cloud": cloud})
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


# Int test fixtures
@pytest.fixture(scope="module")
def tracked_files():
    from .helpers import remove_file

    result = []
    yield result
    for file in result:
        remove_file(file)


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mocked_confirm(mocker):
    mock = mocker.patch(
        "rich.prompt.Confirm",
    )
    mock.ask.return_value = True
    yield mock
