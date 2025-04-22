# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from typing import Any, Dict, List, Optional

from knack.log import get_logger

from ....common import CheckTaskStatus
from ..common import ALL_NAMESPACES_TARGET

logger = get_logger(__name__)


class CheckManager:
    """
    {
        "name":"evaluateBrokerListeners",
        "description": "Evaluate MQ broker listeners",
        "status": "warning",
        "target": "brokerlisteners.mq.iotoperations.azure.com",
        "checks": {
            "mq.iotoperations.azure.com/v1": {
                "_all_": {
                    "conditions": null,
                    "evaluations": [
                        {
                            "status": "success"
                            ...
                        }
                    ],
                }
            },
        }
    }
    """

    def __init__(self, target: str, check_name: str, check_desc: str):
        self.target = target
        self.check_name = check_name
        self.check_desc = check_desc
        self.checks = {}
        self.displays = {}
        self.worst_status = CheckTaskStatus.skipped.value

    def add_check(
        self,
        namespace: str = ALL_NAMESPACES_TARGET,
        conditions: List[str] = None,
        description: str = None,
    ) -> None:
        # TODO: maybe make a singular taget into a class for consistent structure?
        if namespace not in self.checks:
            self.checks[namespace] = {}
        self.checks[namespace]["conditions"] = conditions
        self.checks[namespace]["evaluations"] = []
        self.checks[namespace]["status"] = CheckTaskStatus.skipped.value
        if description:
            self.checks[namespace]["description"] = description

    def add_conditions(self, conditions: List[str], namespace: str = ALL_NAMESPACES_TARGET) -> None:
        if self.checks[namespace]["conditions"] is None:
            self.checks[namespace]["conditions"] = []
        self.checks[namespace]["conditions"].extend(conditions)

    def set_check_status(self, status: str, namespace: str = ALL_NAMESPACES_TARGET) -> None:
        self._process_status(namespace=namespace, status=status)

    def add_check_eval(
        self,
        status: str,
        value: Optional[Any] = None,
        namespace: str = ALL_NAMESPACES_TARGET,
        resource_name: Optional[str] = None,
        resource_kind: Optional[str] = None,
    ) -> None:
        eval_dict = {"status": status}
        if resource_name:
            eval_dict["name"] = resource_name
        if value:
            eval_dict["value"] = value
        if resource_kind:
            eval_dict["kind"] = resource_kind
        self.checks[namespace]["evaluations"].append(eval_dict)
        self._process_status(status, namespace)

    def _process_status(self, status: str, namespace: str = ALL_NAMESPACES_TARGET) -> None:
        namespace_status = self.checks[namespace].get("status")
        # success only overrides skipped status (default)
        if status == CheckTaskStatus.success.value:
            if namespace_status == CheckTaskStatus.skipped.value:
                self.checks[namespace]["status"] = status
            if self.worst_status == CheckTaskStatus.skipped.value:
                self.worst_status = status
        # warning overrides any state that is not "error"
        elif status == CheckTaskStatus.warning.value:
            if namespace_status != CheckTaskStatus.error.value:
                self.checks[namespace]["status"] = status
            if self.worst_status != CheckTaskStatus.error.value:
                self.worst_status = status
        # error overrides any state
        elif status == CheckTaskStatus.error.value:
            self.checks[namespace]["status"] = status
            self.worst_status = status

    def add_display(self, display: Any, namespace: str = ALL_NAMESPACES_TARGET) -> None:
        if namespace not in self.displays:
            self.displays[namespace] = []
        self.displays[namespace].append(display)

    def as_dict(self, as_list: bool = False) -> Dict[str, Any]:
        from copy import deepcopy

        result = {
            "name": self.check_name,
            "description": self.check_desc,
            "target": self.target,
            "checks": {},
            "status": self.worst_status,
        }
        result["checks"] = deepcopy(self.checks)
        if as_list:
            for namespace in self.displays:
                result["checks"][namespace]["displays"] = deepcopy(self.displays[namespace])

        return result
