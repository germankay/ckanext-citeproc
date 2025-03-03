from typing import Dict, Any
from ckan.types import (
    Context,
    DataDict
)

from ckan.plugins.toolkit import (
    side_effect_free,
    check_access
)


@side_effect_free
def dataset_citation_show(context: Context,
                          data_dict: DataDict) -> Dict[str, Any]:
    # TODO: write schemas
    check_access('dataset_citation_show', context, data_dict)
    return {}


@side_effect_free
def resource_citation_show(context: Context,
                           data_dict: DataDict) -> Dict[str, Any]:
    # TODO: write schemas
    check_access('resource_citation_show', context, data_dict)
    return {}
