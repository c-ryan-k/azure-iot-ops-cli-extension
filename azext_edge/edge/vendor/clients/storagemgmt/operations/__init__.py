# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._operations import BlobServicesOperations
from ._operations import BlobContainersOperations
from ._operations import Operations
from ._operations import SkusOperations
from ._operations import StorageAccountsOperations
from ._operations import DeletedAccountsOperations
from ._operations import UsagesOperations
from ._operations import ManagementPoliciesOperations
from ._operations import BlobInventoryPoliciesOperations
from ._operations import PrivateEndpointConnectionsOperations
from ._operations import PrivateLinkResourcesOperations
from ._operations import ObjectReplicationPoliciesOperations
from ._operations import LocalUsersOperations
from ._operations import EncryptionScopesOperations

from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "BlobServicesOperations",
    "BlobContainersOperations",
    "Operations",
    "SkusOperations",
    "StorageAccountsOperations",
    "DeletedAccountsOperations",
    "UsagesOperations",
    "ManagementPoliciesOperations",
    "BlobInventoryPoliciesOperations",
    "PrivateEndpointConnectionsOperations",
    "PrivateLinkResourcesOperations",
    "ObjectReplicationPoliciesOperations",
    "LocalUsersOperations",
    "EncryptionScopesOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()