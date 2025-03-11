from ckan.types import DataDict

import ckan.plugins.interfaces as interfaces


class ICiteProcStyles(interfaces.Interface):
    """Load CSL Style files for use with citeproc-py"""
    citation_styles = []

    def load_citation_styles(self):
        """
        Save a dict of citation_id: citeproc.CitationStylesStyle
        into class citation_styles variable.
        """
        pass


class ICiteProcMappings(interfaces.Interface):
    """Map Dataset and Resource fields to CSL"""

    def dataset_citation_map(self, cite_data: DataDict,
                             pkg_dict: DataDict) -> bool:
        """
        Return a boolean for continue through other plugins,
        modify the cite_data dictionary of CSL fields and values via the pkg_dict
        """
        raise NotImplementedError

    def resource_citation_map(self, cite_data: DataDict,
                              pkg_dict: DataDict,
                              res_dict: DataDict) -> bool:
        """
        Return a boolean for continue through other plugins,
        modify the cite_data dictionary of CSL fields and values via the
        pkg_dict and res_dict
        """
        raise NotImplementedError
