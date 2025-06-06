# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from azure.cli.core.commands.parameters import (
    get_enum_type,
    get_three_state_flag,
    tags_type,
)
from ....common import (
    AEPAuthModes,
    FileType,
    SecurityModes,
    SecurityPolicies,
    TopicRetain,
)


def load_adr_arguments(self, _):
    """
    Load ADR (Asset + Asset Endpoint Profile) CLI Args for Knack parser
    """

    with self.argument_context("iot ops asset") as context:
        context.argument(
            "asset_name",
            options_list=["--name", "-n"],
            help="Asset name.",
        )
        context.argument(
            "endpoint_profile",
            options_list=["--endpoint-profile", "--ep"],
            help="Asset endpoint profile name.",
        )
        context.argument(
            "instance_name", options_list=["--instance"], help="Instance name to associate the created asset with."
        )
        context.argument(
            "instance_resource_group",
            options_list=["--instance-resource-group", "--ig"],
            help="Instance resource group. If not provided, asset resource group will be used.",
        )
        context.argument(
            "instance_subscription",
            options_list=["--instance-subscription", "--is"],
            help="Instance subscription id. If not provided, asset subscription id will be used.",
            deprecate_info=context.deprecate(hide=True),
        )
        context.argument(
            "custom_attributes",
            options_list=["--custom-attribute", "--attr"],
            help="Space-separated key=value pairs corresponding to additional custom attributes for the asset. "
            "This parameter can be used more than once.",
            nargs="+",
            arg_group="Additional Info",
            action="extend",
        )
        context.argument(
            "data_points",
            options_list=["--data"],
            nargs="+",
            action="append",
            help="Space-separated key=value pairs corresponding to properties of the data-point to create. "
            "The following key values are supported: `data_source` (required), `name` (required), "
            "`observability_mode` (None, Gauge, Counter, Histogram, or Log), `sampling_interval` (int), "
            "`queue_size` (int). "
            "--data can be used 1 or more times. Review help examples for full parameter usage",
            arg_group="Data-point",
        )
        context.argument(
            "data_points_file_path",
            options_list=["--data-file", "--df"],
            help="File path for the file containing the data-points. The following file types are supported: "
            f"{', '.join(FileType.list())}.",
            arg_group="Data-point",
        )
        context.argument(
            "description",
            options_list=["--description", "-d"],
            help="Description.",
        )
        context.argument(
            "display_name",
            options_list=["--display-name", "--dn"],
            help="Display name.",
        )
        context.argument(
            "disabled",
            options_list=["--disable"],
            help="Disable an asset.",
            arg_type=get_three_state_flag(),
        )
        context.argument(
            "documentation_uri",
            options_list=["--documentation-uri", "--du"],
            help="Documentation URI.",
            arg_group="Additional Info",
        )
        context.argument(
            "events",
            options_list=["--event"],
            nargs="+",
            action="append",
            help="Space-separated key=value pairs corresponding to properties of the event to create. "
            "The following key values are supported: `event_notifier` (required), "
            "`name` (required), `observability_mode` (none or log), `sampling_interval` "
            "(int), `queue_size` (int). "
            "--event can be used 1 or more times. Review help examples for full parameter usage",
            arg_group="Event",
        )
        context.argument(
            "events_file_path",
            options_list=["--event-file", "--ef"],
            help="File path for the file containing the events. The following file types are supported: "
            f"{', '.join(FileType.list())}.",
            arg_group="Event",
        )
        context.argument(
            "external_asset_id",
            options_list=["--external-asset-id", "--eai"],
            help="External asset Id.",
            arg_group="Additional Info",
        )
        context.argument(
            "hardware_revision",
            options_list=["--hardware-revision", "--hr"],
            help="Hardware revision.",
            arg_group="Additional Info",
        )
        context.argument(
            "manufacturer",
            options_list=["--manufacturer"],
            help="Manufacturer.",
            arg_group="Additional Info",
        )
        context.argument(
            "manufacturer_uri",
            options_list=["--manufacturer-uri", "--mu"],
            help="Manufacturer URI.",
            arg_group="Additional Info",
        )
        context.argument(
            "model",
            options_list=["--model"],
            help="Model.",
            arg_group="Additional Info",
        )
        context.argument(
            "product_code",
            options_list=["--product-code", "--pc"],
            help="Product code.",
            arg_group="Additional Info",
        )
        context.argument(
            "serial_number",
            options_list=["--serial-number", "--sn"],
            help="Serial number.",
            arg_group="Additional Info",
        )
        context.argument(
            "software_revision",
            options_list=["--software-revision", "--sr"],
            help="Software revision.",
            arg_group="Additional Info",
        )
        context.argument(
            "ds_publishing_interval",
            options_list=["--dataset-publish-int", "--dpi"],
            help="Default publishing interval for datasets.",
            arg_group="Dataset Default",
        )
        context.argument(
            "ds_sampling_interval",
            options_list=["--dataset-sample-int", "--dsi"],
            help="Default sampling interval (in milliseconds) for datasets.",
            arg_group="Dataset Default",
        )
        context.argument(
            "ds_queue_size",
            options_list=["--dataset-queue-size", "--dqs"],
            help="Default queue size for datasets.",
            arg_group="Dataset Default",
        )
        context.argument(
            "ev_publishing_interval",
            options_list=["--event-publish-int", "--epi"],
            help="Default publishing interval for events.",
            arg_group="Event Default",
        )
        context.argument(
            "ev_sampling_interval",
            options_list=["--event-sample-int", "--esi"],
            help="Default sampling interval (in milliseconds) for events.",
            arg_group="Event Default",
        )
        context.argument(
            "ev_queue_size",
            options_list=["--event-queue-size", "--eqs"],
            help="Default queue size for events.",
            arg_group="Event Default",
        )
        context.argument(
            "default_topic_path",
            options_list=["--topic-path", "--tp"],
            help="Default topic path.",
            arg_group="MQTT Topic Default",
        )
        context.argument(
            "default_topic_retain",
            options_list=["--topic-retain", "--tr"],
            help="Default topic retain policy.",
            arg_group="MQTT Topic Default",
            arg_type=get_enum_type(TopicRetain),
        )
        context.argument(
            "tags",
            options_list=["--tags"],
            help="Asset resource tags. Property bag in key-value pairs with the following format: a=b c=d",
            arg_type=tags_type,
        )
        context.argument(
            "queue_size",
            options_list=["--queue-size", "--qs"],
            help="Custom queue size.",
        )
        context.argument(
            "publishing_interval",
            options_list=["--publishing-interval", "--pi"],
            help="Custom publishing interval (in milliseconds).",
        )
        context.argument(
            "sampling_interval",
            options_list=["--sampling-interval", "--si"],
            help="Custom sampling interval (in milliseconds).",
        )
        context.argument(
            "extension",
            options_list=["--format", "-f"],
            help="File format.",
            choices=FileType.list(),
            arg_type=get_enum_type(FileType),
        )
        context.argument(
            "output_dir",
            options_list=["--output-dir", "--od"],
            help="Output directory for exported file.",
        )
        context.argument(
            "custom_query",
            options_list=["--custom-query", "--cq"],
            help="Custom query to use. All other query arguments will be ignored.",
        )

    with self.argument_context("iot ops asset query") as context:
        context.argument(
            "disabled",
            options_list=["--disabled"],
            help="State of asset.",
            arg_group="Additional Info",
            arg_type=get_three_state_flag(),
        )

    with self.argument_context("iot ops asset update") as context:
        context.argument(
            "custom_attributes",
            options_list=["--custom-attribute", "--attr"],
            help="Space-separated key=value pairs corresponding to additional custom attributes for the asset. "
            "This parameter can be used more than once."
            'To remove a custom attribute, please set the attribute\'s value to "".',
            nargs="+",
            arg_group="Additional Info",
            action="extend",
        )

    with self.argument_context("iot ops asset dataset") as context:
        context.argument(
            "asset_name",
            options_list=["--asset", "-a"],
            help="Asset name.",
        )
        context.argument(
            "dataset_name",
            options_list=["--name", "-n"],
            help="Dataset name.",
        )

    with self.argument_context("iot ops asset dataset point") as context:
        context.argument(
            "capability_id",
            options_list=["--capability-id", "--ci"],
            help="Capability Id. If not provided, data-point name will be used.",
        )
        context.argument(
            "dataset_name",
            options_list=["--dataset", "-d"],
            help="Dataset name.",
        )
        context.argument(
            "data_point_name",
            options_list=["--name", "-n"],
            help="Data point name.",
        )
        context.argument(
            "data_source",
            options_list=["--data-source", "--ds"],
            help="Data source.",
        )
        context.argument(
            "observability_mode",
            options_list=["--observability-mode", "--om"],
            help="Observability mode. Must be none, gauge, counter, histogram, or log.",
        )

    with self.argument_context("iot ops asset dataset point add") as context:
        context.argument(
            "replace",
            options_list=["--replace"],
            help="Replace the data-point if another data-point with the same name is present already.",
            arg_type=get_three_state_flag(),
        )

    with self.argument_context("iot ops asset dataset point export") as context:
        context.argument(
            "replace",
            options_list=["--replace"],
            help="Replace the local file if present.",
            arg_type=get_three_state_flag(),
        )

    with self.argument_context("iot ops asset dataset point import") as context:
        context.argument(
            "replace",
            options_list=["--replace"],
            help="Replace duplicate asset data-points with those from the file. If false, the file data-points "
            "will be ignored. Duplicate asset data-points will be determined by name.",
            arg_type=get_three_state_flag(),
        )
        context.argument(
            "file_path",
            options_list=["--input-file", "--if"],
            help="File path for the file containing the data-points. The following file types are supported: "
            f"{', '.join(FileType.list())}.",
        )

    with self.argument_context("iot ops asset event") as context:
        context.argument(
            "asset_name",
            options_list=["--asset", "-a"],
            help="Asset name.",
        )
        context.argument(
            "capability_id",
            options_list=["--capability-id", "--ci"],
            help="Capability Id. If not provided, event name will be used.",
        )
        context.argument(
            "event_name",
            options_list=["--name", "-n"],
            help="Event name.",
        )
        context.argument(
            "event_notifier",
            options_list=["--event-notifier", "--en"],
            help="Event notifier.",
        )
        context.argument(
            "observability_mode",
            options_list=["--observability-mode", "--om"],
            help="Observability mode. Must be none or log.",
        )

    with self.argument_context("iot ops asset event add") as context:
        context.argument(
            "replace",
            options_list=["--replace"],
            help="Replace the event if another event with the same name is already present.",
            arg_type=get_three_state_flag(),
        )

    with self.argument_context("iot ops asset event export") as context:
        context.argument(
            "replace",
            options_list=["--replace"],
            help="Replace the local file if present.",
            arg_type=get_three_state_flag(),
        )

    with self.argument_context("iot ops asset event import") as context:
        context.argument(
            "replace",
            options_list=["--replace"],
            help="Replace duplicate asset events with those from the file. If false, the file events "
            "will be ignored. Duplicate asset events will be determined by name.",
            arg_type=get_three_state_flag(),
        )
        context.argument(
            "file_path",
            options_list=["--input-file", "--if"],
            help="File path for the file containing the events. The following file types are supported: "
            f"{', '.join(FileType.list())}.",
        )

    with self.argument_context("iot ops asset endpoint") as context:
        context.argument(
            "asset_endpoint_profile_name",
            options_list=["--name", "-n"],
            help="Asset Endpoint Profile name.",
        )
        context.argument(
            "instance_resource_group",
            options_list=["--instance-resource-group", "--ig"],
            help="Instance resource group. If not provided, asset endpoint profile resource group will be used.",
        )
        context.argument(
            "instance_subscription",
            options_list=["--instance-subscription", "--is"],
            help="Instance subscription id. If not provided, asset endpoint profile subscription id will be used.",
            deprecate_info=context.deprecate(hide=True),
        )
        context.argument(
            "target_address",
            options_list=["--target-address", "--ta"],
            help="Target Address. Must be a valid local address that follows the opc.tcp protocol.",
        )
        context.argument(
            "endpoint_profile_type",
            options_list=["--endpoint-profile-type", "--ept"],
            help="Connector type for the endpoint profile.",
        )
        context.argument(
            "auth_mode",
            options_list=["--authentication-mode", "--am"],
            help="Authentication Mode.",
            arg_group="Authentication",
            arg_type=get_enum_type(AEPAuthModes),
        )
        context.argument(
            "certificate_reference",
            options_list=["--certificate-ref", "--cert-ref", context.deprecate(target="--cr", redirect="--cert-ref")],
            help="Reference for the certificate used in authentication. This method of user authentication is not "
            "supported yet.",
            arg_group="Authentication",
        )
        context.argument(
            "password_reference",
            options_list=["--password-ref", "--pass-ref", context.deprecate(target="--pr", redirect="--pass-ref")],
            help="Reference for the password used in authentication.",
            arg_group="Authentication",
        )
        context.argument(
            "username_reference",
            options_list=[
                context.deprecate(target="--username-reference", redirect="--user-ref"),
                "--username-ref",
                "--user-ref",
                context.deprecate(target="--ur", redirect="--user-ref")
            ],
            help="Reference for the username used in authentication.",
            arg_group="Authentication",
        )
        context.argument(
            "tags",
            options_list=["--tags"],
            help="Asset Endpoint Profile resource tags. Property bag in key-value pairs with the following "
            "format: a=b c=d",
            arg_type=tags_type,
        )

    with self.argument_context("iot ops asset endpoint create custom") as context:
        context.argument(
            "endpoint_profile_type",
            options_list=["--endpoint-type", "--et"],
            help="Endpoint Profile Type for the Connector.",
            arg_group="Connector",
        )
        context.argument(
            "additional_configuration",
            options_list=["--additional-config", "--ac"],
            help="File path containing or inline json for the additional configuration.",
            arg_group="Connector",
        )

    with self.argument_context("iot ops asset endpoint create opcua") as context:
        context.argument(
            "application_name",
            options_list=["--application", "--app"],
            help="Application name. Will be used as the subject for any certificates generated by the connector.",
            arg_group="Connector",
        )
        context.argument(
            "auto_accept_untrusted_server_certs",
            options_list=["--accept-untrusted-certs", "--auc"],
            help="Flag to enable auto accept untrusted server certificates.",
            arg_type=get_three_state_flag(),
            arg_group="Connector",
        )
        context.argument(
            "default_publishing_interval",
            options_list=["--default-publishing-int", "--dpi"],
            help="Default publishing interval in milliseconds. Minimum: -1. Recommended: 1000",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "default_sampling_interval",
            options_list=["--default-sampling-int", "--dsi"],
            help="Default sampling interval in milliseconds. Minimum: -1. Recommended: 1000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "default_queue_size",
            options_list=["--default-queue-size", "--dqs"],
            help="Default queue size. Minimum: 0. Recommended: 1.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "keep_alive",
            options_list=["--keep-alive", "--ka"],
            help="Time in milliseconds after which a keep alive publish response is sent. Minimum: 0. "
            "Recommended: 10000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "run_asset_discovery",
            options_list=["--run-asset-discovery", "--rad"],
            help="Flag to determine if asset discovery should be run.",
            arg_type=get_three_state_flag(),
            arg_group="Connector",
        )
        context.argument(
            "session_timeout",
            options_list=["--session-timeout", "--st"],
            help="Session timeout in milliseconds. Minimum: 0. Recommended: 60000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "session_keep_alive",
            options_list=["--session-keep-alive", "--ska"],
            help="Time in milliseconds after which a session keep alive challenge is sent to detect "
            "connection issues. Minimum: 0. Recommended: 10000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "session_reconnect_period",
            options_list=["--session-reconnect-period", "--srp"],
            help="Session reconnect period in milliseconds. Minimum: 0. Recommended: 2000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "session_reconnect_exponential_back_off",
            options_list=["--session-reconnect-backoff", "--srb"],
            help="Session reconnect exponential back off in milliseconds. Minimum: -1. Recommended: 10000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "security_policy",
            options_list=["--security-policy", "--sp"],
            help="Security policy.",
            arg_group="Connector",
            arg_type=get_enum_type(SecurityPolicies),
        )
        context.argument(
            "security_mode",
            options_list=["--security-mode", "--sm"],
            help="Security mode.",
            arg_group="Connector",
            arg_type=get_enum_type(SecurityModes),
        )
        context.argument(
            "sub_max_items",
            options_list=["--subscription-max-items", "--smi"],
            help="Maximum number of items that the connector can create for the subscription. "
            "Minimum: 1. Recommended: 1000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "sub_life_time",
            options_list=["--subscription-life-time", "--slt"],
            help="Life time in milliseconds of the items created by the connector for the subscription. "
            "Minimum: 0. Recommended: 60000.",
            type=int,
            arg_group="Connector",
        )
        context.argument(
            "certificate_reference",
            options_list=["--certificate-ref", "--cert-ref", "--cr", "--cert-ref"],
            help="Reference for the certificate used in authentication. This method of user authentication is not "
            "supported yet.",
            arg_group="Authentication",
            deprecate_info=context.deprecate(hide=True)
        )
