import os
import xmltodict
from lxml.etree import tostring
from citeproc import CitationStylesStyle

from typing import BinaryIO, List, Dict, Tuple, Generator, Any


def extract_csl_info(
        fileobj: BinaryIO,
        keywords: List[str],
        comment_tags: List[str],
        options: Dict[str, Any]) -> Generator[
            Tuple[int, str, str, List[str]], None, None]:
    """Extract messages from XXX files.

    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: a list of keywords (i.e. function names) that should
                     be recognized as translation functions
    :param comment_tags: a list of translator tags to search for and
                         include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``
    """
    bib_style = CitationStylesStyle(fileobj,
                                    validate=False)
    style_info = xmltodict.parse(tostring(bib_style.xml))
    style_info = style_info.get(
        'style', {}).get('info', {}) if style_info else {}
    title = style_info.get('title')
    _dir, filename = os.path.split(fileobj.name)
    if title:
        yield (0, '', title, ['Title for CSL Style: %s' % filename])
    acronym = style_info.get('title-short')
    if acronym:
        yield (0, '', title, ['Acronym for CSL Style: %s' % filename])
    summary = style_info.get('summary')
    if summary:
        yield (0, '', title, ['Summary for CSL Style: %s' % filename])
