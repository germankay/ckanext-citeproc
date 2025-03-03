from ckan.types import Context, DataDict, AuthResult

from ckan.authz import is_authorized


def dataset_citation_show(context: Context,
                          data_dict: DataDict) -> AuthResult:
    return is_authorized('package_show', context, data_dict)


def resource_citation_show(context: Context,
                           data_dict: DataDict) -> AuthResult:
    return is_authorized('resource_show', context, data_dict)
