[![Tests](https://github.com/open-data/ckanext-citeproc/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data/ckanext-citeproc/actions)

# CKANEXT CiteProc

CKAN plugin to add citations to datasets and resources. This plugin uses https://github.com/citeproc-py/citeproc-py to generate citations in different formats.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | no    |
| 2.7             | no    |
| 2.8             | no    |
| 2.9             | no    |
| 2.10             | yes    |
| 2.11             | yes    |

Compatibility with Python versions:

| Python version    | Compatible?   |
| --------------- | ------------- |
| 2.7 and earlier | no    |
| 3.7 and later            | yes    |

## Installation

To install ckanext-citeproc:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv:
  ```
  git clone https://github.com/open-data/ckanext-citeproc.git
  cd ckanext-citeproc
  pip install -e .
	pip install -r requirements.txt
  ```
3. Add `citeproc` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload

## Config settings

**ckanext.citeproc.dataset_citations** controls citations showing for datasets:

	# (optional, default: true).
	ckanext.citeproc.dataset_citations = false

**ckanext.citeproc.resource_citations** controls citations showing for resources:

	# (optional, default: true).
	ckanext.citeproc.resource_citations = false
