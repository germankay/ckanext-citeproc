from typing import cast
from ckan.types import Schema, Validator, ValidatorFactory

from ckan.logic.schema import validator_args


@validator_args
def dataset_citation_show_schema(
        not_missing: Validator,
        not_empty: Validator,
        unicode_safe: Validator,
        package_id_exists: Validator,
        default: ValidatorFactory,
        one_of: ValidatorFactory) -> Schema:
    return cast(Schema, {
        'id': [not_missing, not_empty,
               unicode_safe, package_id_exists],
        'format': [default('plain'), unicode_safe,
                   one_of(['html', 'plain', 'rst'])]})


@validator_args
def resource_citation_show_schema(
        not_missing: Validator,
        not_empty: Validator,
        unicode_safe: Validator,
        resource_id_exists: Validator,
        default: ValidatorFactory,
        one_of: ValidatorFactory) -> Schema:
    return cast(Schema, {
        'id': [not_missing, not_empty,
               unicode_safe, resource_id_exists],
        'format': [default('plain'), unicode_safe,
                   one_of(['html', 'plain', 'rst'])]})
