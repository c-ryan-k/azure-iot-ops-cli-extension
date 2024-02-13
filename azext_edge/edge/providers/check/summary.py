from base64 import b64decode
from datetime import datetime
from typing import Any, Dict, Tuple
from azext_edge.edge.common import CheckTaskStatus
from azext_edge.edge.util.x509 import get_certificate_expiry

from .base import left_pad

from rich.padding import Padding

from azext_edge.edge.providers.check.common import PADDING_SIZE

from ..base import DEFAULT_NAMESPACE, get_namespaced_secret
from .akri import evaluate_summary as eval_akri_summary
from .base import CheckManager, process_nodes
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
    namespace = DEFAULT_NAMESPACE
    check_manager.add_target(target_name=target, namespace=namespace)
    check_manager.add_display(
        target_name=target,
        namespace=namespace,
        display=Padding("Nodes", padding),
    )
    padding = left_pad(padding, 4)
    process_nodes(check_manager=check_manager, namespace=namespace, target=target, padding=padding)


def eval_secrets(
    check_manager: CheckManager, padding: Tuple[int, int, int, int] = (0, 0, 0, 8)
) -> None:
    target = "summary/secrets"
    check_manager.add_target(target_name=target, namespace=DEFAULT_NAMESPACE)
    check_manager.add_display(
        namespace=DEFAULT_NAMESPACE,
        target_name=target,
        display=Padding("CA keypair secret checks", padding),
    )
    padding = left_pad(padding, 4)
    # try to get secret expiration time

    # try to find non-test certificates
    secret: dict = None
    secret_name = ""
    for _ in ["aio-ca-key-pair", "aio-ca-key-pair-test-only"]:
        secret_name = _
        secret = get_namespaced_secret(namespace=DEFAULT_NAMESPACE, secret_name=_)
        if secret:
            break
    if not secret or not secret.get("data", {}).get("tls.crt", None):
        warning_val = f"No aio-ca-key-pair value found in {DEFAULT_NAMESPACE}"
        check_manager.add_target_eval(
            namespace=DEFAULT_NAMESPACE,
            target_name=target,
            status=CheckTaskStatus.warning.value,
            value=warning_val,
        )
        check_manager.add_display(
            namespace=DEFAULT_NAMESPACE, target_name=target, display=Padding(warning_val, padding)
        )
        return

    secret_crt = b64decode(secret["data"]["tls.crt"])

    expiry = get_certificate_expiry(secret_crt)
    expiry_delta = expiry - datetime.utcnow()
    expiry_delta_days = expiry_delta.days

    # TODO - determine if we should show warnings/errors based on percentages or actual days remaining
    status = CheckTaskStatus.success.value
    warning_limit = 10
    error_limit = 3
    if expiry_delta_days <= error_limit:
        status = CheckTaskStatus.error.value
    elif expiry_delta_days <= warning_limit:
        status = CheckTaskStatus.warning.value

    check_manager.add_target_eval(
        namespace=DEFAULT_NAMESPACE, target_name=target, status=status
    )
    check_manager.add_display(
        namespace=DEFAULT_NAMESPACE,
        target_name=target,
        display=Padding(
            f"- Secret {secret_name} expires in: {expiry_delta.days} days at {expiry.time()}",
            padding,
        ),
    )
    return
