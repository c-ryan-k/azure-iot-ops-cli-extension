from enum import Enum
from typing import Any, Callable, List
from azext_edge.edge.common import CheckTaskStatus
from azext_edge.edge.providers.check.base.check_manager import CheckManager
from azext_edge.edge.providers.check.base.resource import get_resources_by_name, get_resources_grouped_by_namespace
from azext_edge.edge.providers.edge_api.base import EdgeResourceApi
from azext_edge.edge.providers.edge_api.mq import MQ_ACTIVE_API, MqResourceKinds
from azure.cli.core.azclierror import CLIInternalError

# TODO - not sure
class TargetNames(Enum):
    broker = "brokers.mq.iotoperations.azure.com"
    brokerlistner = "brokerlisteners.mq.iotoperations.azure.com"


class MQCheckManager(CheckManager):

    # When initializing the MQCheckManager, we know the targets already
    # No need to define them per check function
    def __init__(self, check_name: str, check_desc: str):
        self.resource_target = MQ_ACTIVE_API.as_str()
        super().__init__(check_name, check_desc)
        super().add_target(target_name=TargetNames.broker)
        super().add_target(target_name=TargetNames.brokerlistner)

    def eval_brokers(self, brokers: List[Any]):
        all_brokers: dict = get_resources_by_name(
            api_info=MQ_ACTIVE_API,
            kind=MqResourceKinds.BROKER,
        )
        if not all_brokers:
            # determine evals and return
            return
        for (namespace, brokers) in get_resources_grouped_by_namespace(all_brokers):
            namespace_evals = [
                {
                    'condition_str': "len(brokers)==1",
                    'value': len(brokers),
                    'eval': lambda value: value == 1,
                },
            ]
            for broker in brokers:
                broker_evals = [
                    {
                        'condition_str': "status",
                        'value': broker.status,
                        'eval': lambda val: CheckTaskStatus.success if val is not None else CheckTaskStatus.error,
                    },
                    {
                        'condition_str': "spec.mode",
                        'value': broker.spec.mode,
                        'eval': lambda val: CheckTaskStatus.success if val is not None else CheckTaskStatus.error,
                    },
                ]
                for eval in broker_evals:
                    self.add_conditional_eval(
                        target=TargetNames.broker,
                        condition_str=eval['condition_str'],
                        value=eval['value'],
                        eval=eval['eval']
                    )

        

    def add_display(self, display: Any) -> None:
        return super().add_display(target=self.target, display=display)
    
    def add_conditional_eval(self, target: str, condition_str: str, value: Any, eval: Callable[[Any], CheckTaskStatus]):
        super().add_target_conditions(target_name=target, conditions=[condition_str])
        status = None
        try:
            status = eval(value).value
        except Exception as ex:
            raise CLIInternalError(ex)

        super().add_target_eval(target_name=target, value=value, status=status)