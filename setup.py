# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**/csl_styles/*.csl', 'csl', None),
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
    entry_points='''
        [ckan.plugins]
        citeproc=ckanext.citeproc.plugin:CiteProcPlugin

        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
        csl = ckanext.citeproc.extract:extract_csl_info
    ''',
)
