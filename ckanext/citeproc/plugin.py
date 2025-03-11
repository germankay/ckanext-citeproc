import os
from datetime import datetime
import xmltodict
from lxml.etree import tostring
from citeproc import CitationStylesStyle
from logging import getLogger

import ckan.plugins as plugins
from ckan.common import CKANConfig

from typing import Dict, Union, Callable, Any
from ckan.types import (
    Action,
    ChainedAction,
    AuthFunction,
    ChainedAuthFunction,
    DataDict
)

from ckan.lib.plugins import DefaultTranslation

from ckanext.citeproc.interfaces import ICiteProcStyles, ICiteProcMappings
from ckanext.citeproc.logic import action, auth
from ckanext.citeproc import helpers


log = getLogger(__name__)


@plugins.toolkit.blanket.config_declarations
class CiteProcPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(ICiteProcStyles, inherit=True)
    plugins.implements(ICiteProcMappings)
    plugins.implements(plugins.ITranslation, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    citation_styles = []

    # ICiteProcStyles
    def load_citation_styles(self):
        citation_styles_dir = plugins.toolkit.config.get(
            'ckanext.citeproc.citation_styles_path')
        if not citation_styles_dir:
            raise Exception('ckanext.citeproc.citation_styles_path'
                            'is not defined but required by ckanext-citeproc')
        if not os.path.isdir(citation_styles_dir):
            raise Exception('%s is not a directory' % citation_styles_dir)
        for f in os.listdir(citation_styles_dir):
            if f.endswith('.csl'):
                bib_style = CitationStylesStyle(os.path.join(citation_styles_dir, f),
                                                validate=False)
                style_info = xmltodict.parse(tostring(bib_style.xml))
                style_info = style_info.get(
                    'style', {}).get('info', {}) if style_info else {}
                self.citation_styles.append({
                    'type': style_info.get('title'),
                    'type_acronym': style_info.get('title-short'),
                    'type_summary': style_info.get('summary'),
                    'class': bib_style})
        log.debug('Loaded %s citation styles from %s' %
                  (len(self.citation_styles), citation_styles_dir))

    # ICiteProcMappings
    def dataset_citation_map(self, cite_data: DataDict,
                             pkg_dict: DataDict) -> bool:
        cite_data['title'] = plugins.toolkit.h.get_translated(pkg_dict, 'title')
        cite_data['container_title'] = plugins.toolkit.config.get('ckan.site_title')
        if pkg_dict.get('owner_org'):
            org_dict = plugins.toolkit.get_action('organization_show')(
                {'ignore_auth': True}, {'id': pkg_dict.get('owner_org')})
            cite_data['publisher'] = plugins.toolkit.h.get_translated(
                org_dict, 'title')
        created_date = datetime.fromisoformat(pkg_dict['metadata_created'])
        cite_data['issued'] = {
            'date-parts': [[created_date.year, created_date.month, created_date.month]]
        }
        cite_data['URL'] = plugins.toolkit.h.url_for('%s.read' % pkg_dict['type'],
                                                     _external=True,
                                                     id=pkg_dict['id'])
        return True

    def resource_citation_map(self, cite_data: DataDict,
                              pkg_dict: DataDict,
                              res_dict: DataDict) -> bool:
        cite_data['title'] = plugins.toolkit.h.get_translated(pkg_dict, 'title') + \
            ' - ' + plugins.toolkit.h.get_translated(res_dict, 'name')
        cite_data['container_title'] = plugins.toolkit.config.get('ckan.site_title')
        if pkg_dict.get('owner_org'):
            org_dict = plugins.toolkit.get_action('organization_show')(
                {'ignore_auth': True}, {'id': pkg_dict.get('owner_org')})
            cite_data['publisher'] = plugins.toolkit.h.get_translated(
                org_dict, 'title')
        created_date = datetime.fromisoformat(res_dict['created'])
        cite_data['issued'] = {
            'date-parts': [[created_date.year, created_date.month, created_date.month]]
        }
        cite_data['URL'] = plugins.toolkit.h.url_for('%s_resource.read' %
                                                     pkg_dict['type'],
                                                     _external=True,
                                                     package_type=pkg_dict['type'],
                                                     id=pkg_dict['id'],
                                                     resource_id=res_dict['id'])
        return True

    # DefaultTranslation, ITranslation
    def i18n_domain(self) -> str:
        return 'ckanext-citeproc'

    # IConfigurer
    def update_config(self, config: 'CKANConfig'):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_resource('assets', 'ckanext-citeproc')
        self.load_citation_styles()

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
