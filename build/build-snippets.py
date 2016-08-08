# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
"""Build snippets from documentation from AWS."""
from __future__ import unicode_literals

import requests
import os
from collections import OrderedDict
from templating import build_with_template
from lxml import html
from colorama import init
from colorama import Fore
from fabulous.widget import ProgressBar

BASE_HREF = 'http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/'


def print_header(snippets_found, headers):
    """Header print function."""
    print('\033c' + Fore.GREEN +
    """
     _                _          _ _       __   __
    | |              | |        (_) |     / /  / _|
    | |__   ___  __ _| | ___ __  _| |_   / /__| |_ ___  _ __ _ __ ___
    | '_ \ / _ \/ _` | |/ / '_ \| | __| / / __|  _/ _ \| '__| '_ ` _ `
    | |_) |  __/ (_| |   <| | | | | |_ / / (__| || (_) | |  | | | | | |
    |_.__/ \___|\__,_|_|\_\_| |_|_|\__/_/ \___|_| \___/|_|  |_| |_| |_|""")

    print('    Updated: ' + Fore.GREEN + '{}'.format(headers['last-modified']))
    print('    Snippets founds: ' + Fore.GREEN + '{}\n'.format(snippets_found))


def build_index(toc_uri, elem_expr):
    """Build the main index with key and url for the services."""
    page = requests.get(toc_uri)
    doc = html.fromstring(page.text.decode('utf-8'))
    tree = doc.xpath(elem_expr)
    index = OrderedDict()

    print_header(len(tree), page.headers)

    for e in tree:
            arn = e.text_content()
            title = e.text_content().replace('::', '-') \
                .replace('AWS-', "") \
                .replace('Fn-', "") \
                .lower()
            href = e.get('href')
            full_href = BASE_HREF + href
            index[arn] = (arn, title, href, full_href)

    return index


def generate(index):
    """Will traverse index and generate all the snippets."""
    total = len(index)
    i = 0
    percent = 0
    progress = ProgressBar()
    progress.update(i, 'Generating snippets')
    for k, v in index.iteritems():
        (arn, title, href, full_href) = v
        # snippet = createSnippet(arn, title, href, full_href)
        i += 1
        percent = i * 100 / total
        progress.update(percent, 'Creating ' + Fore.GREEN + arn)
        # writeToOutput(title, snippet)
    progress.update(percent, 'Snippets completed')


def createSnippet(arn, title, href, full_href):
    """Create a snippet with the args."""
    elem_expr = '//*[@id="main-col-body"]/div/div/pre/code'

    # uses an old documentation format
    if (arn == 'AWS::SDB::Domain'):
        elem_expr = '//*[@id="main-col-body"]/div/pre'

    page = requests.get(full_href)
    doc = html.fromstring(page.text)
    tree = doc.xpath(elem_expr)
    # print 'creating {} => {}'.format(arn, title)
    return build_with_template(arn, title, tree, full_href)


def safedebug(index, k):
    """Debug helper for scrapping problems."""
    (arn, title, href, full_href) = index[k]
    snippet = createSnippet(arn, title, href, full_href)
    print snippet


def writeToOutput(title, snippet):
    """Write the snippet to the output folder."""
    default_folder = "./output/"
    default_suffix = ".sublime-snippet"

    if (not os.path.exists(default_folder)):
        os.makedirs(default_folder)

    filename = default_folder + title + default_suffix
    out = file(filename, 'w')
    out.write(snippet.encode('utf8', 'replace'))
    out.close()


def generate_functions():
    """Function are a special cases, they're scaterred all over the docs."""
    toc_functions = [
                        ('Fn::Select', 'fn-select', '{ "Fn::Select" : [ index, listOfObjects ] }', 'intrinsic-function-reference-select.html', BASE_HREF + 'intrinsic-function-reference-select.html'),
                        ('Ref', 'ref', '"Ref" : "logicalName"', 'intrinsic-function-reference-ref.html', BASE_HREF + 'intrinsic-function-reference-ref.html'),
                        ('Fn::Join', 'fn-join', '"Fn::Join" : [ "delimiter", [ comma-delimited list of values ] ]', 'intrinsic-function-reference-join.html', BASE_HREF + 'intrinsic-function-reference-join.html'),
                        ('Fn::GetAZs', 'fn-getAZs', '"Fn::GetAZs" : "region"', 'intrinsic-function-reference-getavailabilityzones.html', BASE_HREF + 'intrinsic-function-reference-getavailabilityzones.html'),
                        ('Fn::GetAtt', 'fn-getatt', '"Fn::GetAtt" : [ "logicalNameOfResource", "attributeName" ]', 'intrinsic-function-reference-getatt.html', BASE_HREF + 'intrinsic-function-reference-getatt.html'),
                        ('Fn::FindInMap', 'fn-findInMap', '"Fn::FindInMap" : [ "MapName", "TopLevelKey", "SecondLevelKey"]', 'intrinsic-function-reference-findinmap.html', BASE_HREF + 'intrinsic-function-reference-findinmap.html')
                    ]
    i = 0
    percent = 0
    total = len(toc_functions)
    print('    Functions found: ' + Fore.GREEN + str(total))

    progress = ProgressBar()
    progress.update(i, 'Generating functions')

    for v in toc_functions:
        (arn, title, body, href, full_href) = v
        writeToOutput(title, build_with_template(arn, title, body, full_href))
        i += 1
        percent = i * 100 / total
        progress.update(percent, 'Creating ' + Fore.GREEN + arn)

    progress.update(percent, 'Functions generated.')


def main():
    """Main doc generation."""
    init(autoreset=True)  # colorama

    # build topics
    toc_uri = BASE_HREF + 'aws-template-resource-type-ref.html'
    elem_expr = '//*[@id="main-col-body"]/div[2]/div/ul/li/a'
    index = build_index(toc_uri, elem_expr)
    generate(index)

    # build functions
    generate_functions()
    print('\n    Snippets generated, have fun.')
    print('    Got questions or want something on this? '
          + '    https://github.com/beaknit/cform')


if __name__ == "__main__":
    main()
