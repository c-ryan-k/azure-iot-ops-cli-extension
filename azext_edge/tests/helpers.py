# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from typing import Dict, List, Tuple


def parse_rest_command(rest_command: str) -> Dict[str, str]:
    """Simple az rest command parsing."""
    assert rest_command.startswith("rest")
    rest_list = rest_command.split("--")[1:]
    result = {}
    for rest_input in rest_list:
        key, value = rest_input.split(maxsplit=1)
        result[key] = value.strip()
    return result

def create_spc_yaml(
    name: str,
    namespace: str,
    keyvault_name: str,
    secrets: List[Tuple[str, str]],
    tenantId: str,
) -> dict:
    from yaml import safe_load

    return safe_load(
        f"""
    apiVersion: secrets-store.csi.x-k8s.io/v1
    kind: SecretProviderClass
    metadata:
      name: {name}
      namespace: {namespace}
    spec:
      provider: "azure"
      parameters:
        usePodIdentity: "false"
        keyvaultName: "{keyvault_name}"
        tenantId: {tenantId}
        objects: |
          array:"""
        + "".join(
            [
              f"""
              - |
              objectName: {s_name}
              objectType: {s_type}
              objectVersion: ''
              """
              for (s_name, s_type) in secrets
            ]
        )
    )