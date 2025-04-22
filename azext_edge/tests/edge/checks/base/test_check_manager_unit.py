# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------


from azext_edge.edge.common import CheckTaskStatus
from azext_edge.edge.providers.check.base import CheckManager

from ....generators import generate_random_string


def test_check_manager():
    name = generate_random_string()
    desc = f"{generate_random_string()} {generate_random_string()}"
    namespace = generate_random_string()
    target_1 = generate_random_string()
    target_1_condition_1 = generate_random_string()
    target_1_conditions = [target_1_condition_1]
    target_1_eval_1_value = {generate_random_string(): generate_random_string()}
    target_1_display_1 = generate_random_string()
    check_manager = CheckManager(check_name=name, check_desc=desc, target=target_1)
    assert_check_manager_dict(
        check_manager=check_manager,
        expected_name=name,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_status=CheckTaskStatus.skipped.value,
    )

    check_manager.add_check(namespace=namespace, conditions=target_1_conditions)
    check_manager.add_check_eval(
        namespace=namespace,
        status=CheckTaskStatus.success.value,
        value=target_1_eval_1_value,
    )
    check_manager.add_display(namespace=namespace, display=target_1_display_1)
    expected_targets = {
        target_1: {
            "conditions": target_1_conditions,
            "evaluations": [
                {
                    "status": CheckTaskStatus.success.value,
                    "value": target_1_eval_1_value,
                }
            ],
            "status": CheckTaskStatus.success.value,
        }
    }
    assert_check_manager_dict(
        check_manager=check_manager,
        expected_name=name,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_targets=expected_targets,
        expected_target_displays={target_1: [target_1_display_1]},
    )
    check_manager.add_check_eval(namespace=namespace, status=CheckTaskStatus.warning.value)
    expected_targets = {
        target_1: {
            "conditions": target_1_conditions,
            "evaluations": [
                {
                    "status": CheckTaskStatus.success.value,
                    "value": target_1_eval_1_value,
                },
                {"status": CheckTaskStatus.warning.value},
            ],
            "status": CheckTaskStatus.warning.value,
        }
    }
    assert_check_manager_dict(
        check_manager=check_manager,
        expected_name=name,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_targets=expected_targets,
        expected_status=CheckTaskStatus.warning.value,
    )

    # Re-create check manager with target 1 kpis and assert skipped status
    check_manager = CheckManager(check_name=name, check_desc=desc, target=target_1)
    check_manager.add_check(namespace=namespace, conditions=target_1_conditions)
    check_manager.add_check_eval(namespace=namespace, status=CheckTaskStatus.skipped.value, value=None)
    expected_targets = {
        target_1: {
            "conditions": target_1_conditions,
            "evaluations": [{"status": CheckTaskStatus.skipped.value}],
            "status": CheckTaskStatus.skipped.value,
        }
    }
    assert_check_manager_dict(
        check_manager=check_manager,
        expected_name=name,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_targets=expected_targets,
        expected_status=CheckTaskStatus.skipped.value,
    )


def assert_check_manager_dict(
    check_manager: CheckManager,
    expected_name: str,
    expected_namespace: str,
    expected_desc: str,
    expected_targets: dict = None,
    expected_status: str = CheckTaskStatus.success.value,
    expected_target_displays: dict = None,
):
    result_check_dict = check_manager.as_dict()
    if not expected_targets:
        expected_targets = {}

    assert "name" in result_check_dict
    assert result_check_dict["name"] == expected_name

    assert "description" in result_check_dict
    assert expected_desc in result_check_dict["description"]

    assert "targets" in result_check_dict
    for target in expected_targets:
        assert target in result_check_dict["targets"]

    assert "status" in result_check_dict
    assert result_check_dict["status"] == expected_status

    if expected_target_displays:
        result_check_dict_displays = check_manager.as_dict(as_list=True)
        for target in expected_target_displays:
            assert (
                expected_target_displays[target]
                == result_check_dict_displays["targets"][target][expected_namespace]["displays"]
            )
