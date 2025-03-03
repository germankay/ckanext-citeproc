from ckan.plugins.toolkit import config, asbool


def show_citations_for(object_type: str):
    return asbool(config.get(f'ckanext.citeproc.{object_type}_show_citations', True))
