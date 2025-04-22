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
    target_1 = generate_random_string()
    check_manager = CheckManager(check_name=name, check_desc=desc, target=target_1)

    namespace = generate_random_string()
    target_1_conditions = [generate_random_string()]
    target_1_eval_1_value = {generate_random_string(): generate_random_string()}
    target_1_display_1 = generate_random_string()

    # Assert check manager dict with no checks and skipped status
    assert_check_manager_dict(
        check_manager=check_manager,
        expected_name=name,
        expected_target=target_1,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_status=CheckTaskStatus.skipped.value,
    )

    # Add check and assert check manager dict with success status, one display
    check_manager.add_check(namespace=namespace, conditions=target_1_conditions)
    check_manager.add_check_eval(
        namespace=namespace,
        status=CheckTaskStatus.success.value,
        value=target_1_eval_1_value,
    )
    check_manager.add_display(namespace=namespace, display=target_1_display_1)
    expected_checks = {
        namespace: {
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
        expected_target=target_1,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_checks=expected_checks,
        expected_displays={namespace: [target_1_display_1]},
    )
    check_manager.add_check_eval(namespace=namespace, status=CheckTaskStatus.warning.value)
    expected_checks = {
        namespace: {
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
        expected_target=target_1,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_checks=expected_checks,
        expected_status=CheckTaskStatus.warning.value,
    )

    # Re-create check manager with target 1 kpis and assert skipped status
    check_manager = CheckManager(check_name=name, check_desc=desc, target=target_1)
    check_manager.add_check(namespace=namespace, conditions=target_1_conditions)
    check_manager.add_check_eval(namespace=namespace, status=CheckTaskStatus.skipped.value, value=None)
    expected_checks = {
        namespace: {
            "conditions": target_1_conditions,
            "evaluations": [{"status": CheckTaskStatus.skipped.value}],
            "status": CheckTaskStatus.skipped.value,
        }
    }
    assert_check_manager_dict(
        check_manager=check_manager,
        expected_name=name,
        expected_target=target_1,
        expected_namespace=namespace,
        expected_desc=desc,
        expected_checks=expected_checks,
        expected_status=CheckTaskStatus.skipped.value,
    )


def assert_check_manager_dict(
    check_manager: CheckManager,
    expected_name: str,
    expected_namespace: str,
    expected_target: str,
    expected_desc: str,
    expected_checks: dict = None,
    expected_status: str = CheckTaskStatus.success.value,
    expected_displays: dict = None,
):
    result_check_dict = check_manager.as_dict()
    if not expected_checks:
        expected_checks = {}

    assert "name" in result_check_dict
    assert result_check_dict["name"] == expected_name

    assert "target" in result_check_dict
    assert result_check_dict["target"] == expected_target

    assert "description" in result_check_dict
    assert expected_desc in result_check_dict["description"]

    assert "checks" in result_check_dict
    for namespace in expected_checks:
        assert namespace in result_check_dict["checks"]

    assert "status" in result_check_dict
    assert result_check_dict["status"] == expected_status

    if expected_displays:
        result_check_dict_displays = check_manager.as_dict(as_list=True)
        for namespace in expected_displays:
            assert expected_displays[expected_namespace] == result_check_dict_displays["checks"][namespace]["displays"]
