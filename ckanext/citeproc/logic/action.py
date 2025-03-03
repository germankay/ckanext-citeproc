import os
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from logging import getLogger

from typing import Dict, Any, List, Optional
from ckan.types import (
    Context,
    DataDict
)

from ckan.plugins.toolkit import (
    side_effect_free,
    check_access,
    config
)


log = getLogger(__name__)


def _get_citation_styles(limit_styles: Optional[List[str]] = None) -> Dict[str, Any]:
    if not limit_styles:
        limit_styles = []
    citation_styles_dir = config.get('ckanext.citeproc.citation_styles_path')
    if not citation_styles_dir:
        log.warning(
            'ckanext.citeproc.citation_styles_path is not defined but required')
        return
    if not os.path.isdir(citation_styles_dir):
        log.warning('%s is not a directory' % citation_styles_dir)
        return
    citation_styles = {}
    for f in os.listdir(citation_styles_dir):
        if f.endswith('.csl'):
            style_name = f.replace('.csl', '')
            if limit_styles and style_name not in limit_styles:
                continue
            citation_styles[style_name] = os.path.join(citation_styles_dir, f)
    return citation_styles


def _generate_citations(cite_data: List[Dict[str, Any]],
                        citation_styles: Dict[str, Any]) -> Dict[str, str]:
    citations = {}
    bib_source = CiteProcJSON(cite_data)
    for style, style_path in citation_styles.items():
        try:
            bib_style = CitationStylesStyle(style_path, validate=False)
            bibliography = CitationStylesBibliography(bib_style,
                                                      bib_source,
                                                      formatter.html)
            citation = Citation([CitationItem('thisistheidofthedataset')])
            bibliography.register(citation)
            bibliography.cite(citation, lambda x: log.debug(
                'Reference with key {} not found in the bibliography.'.format(x.key)))
            citations[style] = str(bibliography.bibliography()[0])
        except Exception:
            log.warning('Could not generate citation for dataset %s in the style %s' %
                        ('', style))
            pass
    return citations


@side_effect_free
def dataset_citation_show(context: Context,
                          data_dict: DataDict) -> Dict[str, Any]:
    # TODO: write schemas
    check_access('dataset_citation_show', context, data_dict)
    available_citation_styles = _get_citation_styles()
    # FIXME: apa style not working...missing something??
    dev = [{
        "id": "thisistheidofthedataset",
        "issued": {
            "date-parts": [[1987,  8,  3],
                           [2003, 10, 23]]
        },
        "title": "Developer Testing",
        "type": "website"
    }]
    return _generate_citations(dev, available_citation_styles)


@side_effect_free
def resource_citation_show(context: Context,
                           data_dict: DataDict) -> Dict[str, Any]:
    # TODO: write schemas
    check_access('resource_citation_show', context, data_dict)
    available_citation_styles = _get_citation_styles()
    return {}
