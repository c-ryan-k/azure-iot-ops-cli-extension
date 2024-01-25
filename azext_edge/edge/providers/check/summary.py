from base64 import b64decode
from datetime import timedelta, timezone, datetime
from typing import Any, Dict, Tuple, TypedDict
from azext_edge.edge.common import CheckTaskStatus
from azext_edge.edge.util.x509 import get_certificate_expiry
from .base import left_pad

from rich.padding import Padding

from azext_edge.edge.providers.check.common import PADDING_SIZE

from ..base import DEFAULT_NAMESPACE, get_namespaced_secret
from .akri import evaluate_summary as eval_akri_summary
from .base import CheckManager
from .dataprocessor import evaluate_summary as eval_dataprocessor_summary
from .lnm import evaluate_summary as eval_lnm_summary
from .mq import evaluate_summary as eval_mq_summary
from .opcua import evaluate_summary as eval_opcua_summary


def run_summary_checks(as_list: bool):
    return [
        func(as_list=as_list)
        for func in [
            eval_aio_summary,
            eval_mq_summary,
            eval_dataprocessor_summary,
            eval_lnm_summary,
            eval_opcua_summary,
            eval_akri_summary,
        ]
    ]


def eval_aio_summary(
    as_list: bool = False,
) -> Dict[str, Any]:
    desc = "Evaluate AIO summary items"
    check_manager = CheckManager(
        check_name="evalAIOSummary",
        check_desc=desc,
    )

    padding = (0, 0, 0, PADDING_SIZE)
    eval_nodes(check_manager=check_manager, padding=padding)
    eval_secrets(check_manager=check_manager, padding=padding)
    return check_manager.as_dict(as_list=as_list)


def eval_nodes(
    check_manager: CheckManager, padding: Tuple[int, int, int, int] = (0, 0, 0, 8)
) -> None:
    target = "summary/nodes"
    check_manager.add_target(target_name=target)
    # check_manager.add_display(target_name=target, display=Padding("nodes", padding))
    return


def eval_secrets(
    check_manager: CheckManager, padding: Tuple[int, int, int, int] = (0, 0, 0, 8)
) -> None:
    target = "summary/secrets"
    secret_prefix = "aio-ca-key-pair"
    # cm_prefix = "aio-ca-trust-bundle"
    check_manager.add_target(target_name=target)
    # check_manager.add_display(target_name=target, display=Padding("secrets", padding))

    # try to get secret expiration time

    # try to find non-test certificates
    secret = get_namespaced_secret(namespace=DEFAULT_NAMESPACE, secret_name=secret_prefix)
    if not secret:
        secret_prefix = f"{secret_prefix}-test-only"
        secret = get_namespaced_secret(namespace=DEFAULT_NAMESPACE, secret_name=secret_prefix)
    secret_crt = b64decode(secret['data']['tls.crt'])
    # print(secret_crt)
    expiry = get_certificate_expiry(secret_crt)
    expiry_delta = expiry - datetime.utcnow()
    expiry_delta_days = expiry_delta.days

    # green if > 15 days
    status = CheckTaskStatus.success.value
    # yellow if 3-14 days
    warning_limit = 14
    # red if < 3 days
    error_limit = 3
    if expiry_delta_days <= error_limit:
        status = CheckTaskStatus.error.value
    elif expiry_delta_days <= warning_limit:
        status = CheckTaskStatus.warning.value

    print(f"expiry: {expiry}")
    print(f"expires in: {expiry_delta.days} days at {expiry.time()}")
    print(f"status: {status}")
    check_manager.add_target_eval(target_name=target, status=status)
    check_manager.add_display(target_name=target, display=Padding(
        f"Secret {secret_prefix} expires in: {expiry_delta.days} days at {expiry.time()}",
        padding
    ))
    return
