

from typing import TypedDict
from ..base import DEFAULT_NAMESPACE
from .base import CheckManager
from rich.padding import Padding
from .mq import evaluate_summary as get_mq_summary
from .dataprocessor import evaluate_summary as get_dataprocessor_summary
from .lnm import evaluate_summary as get_lnm_summary
from .opcua import evaluate_summary as get_opcua_summary
# from akri import evaluate_summary as get_akri_summary


def check_service_summary(as_list: bool):
    # check_manager = CheckManager(check_name="summary", check_desc="Service Summary Checks")
    summaries = []
    for (key, func) in [
        # ("aio", get_aio_summary),
        ("mq", get_mq_summary),
        ("dataprocessor", get_dataprocessor_summary),
        ("lnm", get_lnm_summary),
        ("opcua", get_opcua_summary),
        # ("akri", get_akri_summary),
    ]:
        summaries.append(func(as_list=as_list))
    return summaries
