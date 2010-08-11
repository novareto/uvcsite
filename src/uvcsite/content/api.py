#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok

from lxml import etree
from uvcsite.content import IProductFolder
from z3c.schema2xml import serialize_to_tree, deserialize
from zope.component import getMultiAdapter
from zope.interface import Invalid
from zope.pagetemplate.interfaces import IPageTemplate


class RestLayer(grok.IRESTLayer):
    """ Layer for Rest Access"""
    grok.restskin('api')


class ProductFolderRest(grok.REST):
    grok.layer(RestLayer)
    grok.context(IProductFolder)

    def GET(self):
        context = self.context
        container = etree.Element('container', id=context.__name__)
        for id, obj in self.context.items():
            schema = obj.schema[0]
            element = etree.SubElement(container, obj.meta_type, id=id)
            serialize_to_tree(element, schema, obj)
        return etree.tostring(container, encoding='UTF-8', pretty_print=True)

    def POST(self):
        return "POST"

    def PUT(self):
        errors = []
        content = self.context.getContentType()()
        interface = content.schema[0]
        try:
            deserialize(self.body, interface, content)
        except Exception, e: # Here should be a DeserializeError
            for field, (exception, element) in e.field_errors.items():
                error = etree.Element('error', field=field.__name__,
                    message=exception.__doc__)
                error.append(element)
                errors.append(error)
        try:
            interface.validateInvariants(content)
        except Invalid, e:
            errors.append(etree.Element('error', text="Invariant: %s" % e))

        if not errors:
            id = "%s-%s" %(content.meta_type, str(len(self.context)))
            self.context[id] = content
            result = etree.Element('success', name=content.meta_type, id=id)
        else:
            result = etree.Element('failure')
            result.extend(errors)
        return etree.tostring(result, encoding='UTF-8', pretty_print=True)
