# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
"""Build snippets from documentation from AWS."""
import requests
from collections import OrderedDict
from templating import build_with_template
from lxml import html


BASE_HREF = 'http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/'


def build_index():
    """Build the main index with key and url for the services."""
    toc_uri = BASE_HREF + 'aws-template-resource-type-ref.html'
    elem_expr = '//*[@id="main-col-body"]/div[2]/div/ul/li/a'
    page = requests.get(toc_uri)
    doc = html.fromstring(page.text.decode('utf-8'))
    tree = doc.xpath(elem_expr)
    index = OrderedDict()

    for e in tree:
            arn = e.text_content()
            title = e.text_content().replace('::', '-') \
                .replace('AWS-', "") \
                .lower()
            href = e.get('href')
            full_href = BASE_HREF + href
            index[arn] = (arn, title, href, full_href)

    return index


def generate(index):
    """Will traverse index and generate all the snippets."""
    for k, v in index.iteritems():
        (arn, title, href, full_href) = v
        snippet = createSnippet(arn, title, href, full_href)
        writeToOutput(arn, snippet)


def createSnippet(arn, title, href, full_href):
    """Create a snippet with the args."""
    elem_expr = '//*[@id="main-col-body"]/div/div/pre/code'

    # uses an old documentation format
    if (arn == 'AWS::SDB::Domain'):
        elem_expr = '//*[@id="main-col-body"]/div/pre'

    page = requests.get(full_href)
    doc = html.fromstring(page.text)
    tree = doc.xpath(elem_expr)
    print 'creating {} => {}'.format(arn, title)
    return build_with_template(arn, title, tree, full_href)


def safedebug(index, k):
    """Debug helper for scrapping problems."""
    (arn, title, href, full_href) = index[k]
    snippet = createSnippet(arn, title, href, full_href)
    print snippet


def writeToOutput(arn, snippet):
    """Write the snippet to the output folder."""
    default_suffix = ".sublime-snippet"


def main():
    """Main doc generation."""
    index = build_index()
    # generate(index)
    safedebug(index, 'AWS::SSM::Document')

if __name__ == "__main__":
    main()
