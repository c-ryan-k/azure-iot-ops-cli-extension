import pytest

from azext_edge.edge.common import OpsServiceType
from azext_edge.edge.providers.base import DEFAULT_NAMESPACE, create_namespaced_custom_objects
from azext_edge.edge.providers.check.common import ResourceOutputDetailLevel
from azext_edge.edge.providers.checks import run_checks
from azext_edge.edge.providers.edge_api.keyvault import KEYVAULT_API_V1, KeyVaultResourceKinds
from azext_edge.edge.providers.orchestration.components import get_kv_secret_store_yaml
from azext_edge.edge.providers.orchestration.work import CLUSTER_SECRET_CLASS_NAME

BOOLEAN = [True, False]

@pytest.mark.parametrize("detail_level", ResourceOutputDetailLevel.list())
@pytest.mark.parametrize("as_list", BOOLEAN)
@pytest.mark.parametrize("pre", BOOLEAN)
@pytest.mark.parametrize("post", BOOLEAN)
def test_mq_checks(setup_secret_provider, detail_level, as_list, pre, post):
    test = run_checks(
        detail_level=detail_level,
        ops_service=OpsServiceType.mq.value,
        pre_deployment=pre,
        post_deployment=post,
        as_list=as_list,
    )

