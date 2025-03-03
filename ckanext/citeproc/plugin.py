import ckan.plugins as plugins
from ckan.common import CKANConfig

from typing import Dict, Union, Callable, Any
from ckan.types import (
    Action,
    ChainedAction,
    AuthFunction,
    ChainedAuthFunction
)

from ckan.lib.plugins import DefaultTranslation

from ckanext.citeproc.logic import action, auth
from ckanext.citeproc import helpers


@plugins.toolkit.blanket.config_declarations
class CiteProcPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    # DefaultTranslation, ITranslation
    def i18n_domain(self) -> str:
        return 'ckanext-citeproc'

    # IConfigurer
    def update_config(self, config: 'CKANConfig'):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_resource('assets', 'ckanext-citeproc')

    # IActions
    def get_actions(self) -> Dict[str, Union[Action, ChainedAction]]:
        return {
            'dataset_citation_show': action.dataset_citation_show,
            'resource_citation_show': action.resource_citation_show,
        }

    # IAuthFunctions
    def get_auth_functions(self) -> Dict[str, Union[AuthFunction,
                                                    ChainedAuthFunction]]:
        return {
            'dataset_citation_show': auth.dataset_citation_show,
            'resource_citation_show': auth.resource_citation_show,
        }

    # ITemplateHelpers
    def get_helpers(self) -> Dict[str, Callable[..., Any]]:
        return {'show_citations_for': helpers.show_citations_for}
