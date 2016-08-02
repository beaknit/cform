# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
"""Build snippets from documentation from AWS."""
import requests
from templating import build_with_template
from lxml import html


BASE_HREF = 'http://docs.aws.amazon.com/pt_br/AWSCloudFormation/latest/UserGuide/'


def build_index():
    """Build the main index with key and url for the services."""
    toc_uri = BASE_HREF + 'aws-template-resource-type-ref.html'
    elem_expr = '//*[@id="main-col-body"]/div[2]/div[2]/ul/li/a'
    page = requests.get(toc_uri)
    doc = html.fromstring(page.content)
    tree = doc.xpath(elem_expr)
    index = {}

    for e in tree:
            arn = e.text_content()
            title = e.text_content().replace('::', '-').replace('AWS-', "").lower()
            href = e.get('href')
            full_href = BASE_HREF + href
            index[arn] = (arn, title, href, full_href)
    return index

def generate(index):
    """Will traverse index and generate all the snippets."""
    default_suffix = '.sublime-snippet'
    for k, v in index.iteritems():
        (arn, title, href, full_href) = v
        snippet = createSnippet(arn, title, href, full_href)

def createSnippet(arn, title, href, full_href):
    """Create a snippet with the args."""
    print build_with_template(arn, title, '')

def main():
    """Main doc generation."""
    index = build_index()
    generate(index)

if __name__ == "__main__":
    main()
