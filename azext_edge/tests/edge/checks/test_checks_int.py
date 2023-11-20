import pytest

from azext_edge.edge.common import OpsServiceType
from azext_edge.edge.providers.check.common import ResourceOutputDetailLevel
from azext_edge.edge.providers.checks import run_checks

BOOLEAN = [True, False]

pytest.mark.parametrize("detail_level", ResourceOutputDetailLevel.list())
pytest.mark.parametrize("as_list", BOOLEAN)
pytest.mark.parametrize("pre", BOOLEAN)
pytest.mark.parametrize("post", BOOLEAN)
def test_mq_checks(detail_level, as_list, pre, post):
   test = run_checks(detail_level=detail_level, ops_service=OpsServiceType.mq.value, pre_deployment=pre, post_deployment=post, as_list=as_list)
   print(test)
