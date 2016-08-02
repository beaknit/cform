# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
"""Templating operations for the snippets created by the build script."""


def build_with_template(trigger, title, body):
    template = """
    <snippet>
        <content><![CDATA[{}]]></content>
        <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
        <tabTrigger>{}</tabTrigger>
        <!-- Optional: Set a scope to limit where the snippet will trigger -->
        <scope>source.cloudformation</scope>
    </snippet>
    """.format(body, title)

    return template
