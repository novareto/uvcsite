#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import grok
import uvcsite

from dolmen.content import IContent
from hurry.workflow.interfaces import IWorkflowState
from uvc.layout.forms.event import AfterSaveEvent
from uvcsite.content import IProductFolder
from uvcsite.workflow.basic_workflow import titleForState
from z3c.schema2json import serialize
from z3c.schema2json.tools import deserialize
from zope.interface import Invalid, Interface, implementer


class JSONRestLayer(grok.IRESTLayer):
    """ Layer for Rest Access"""
    grok.restskin('jsonapi')


class ProductFolderRest(grok.REST):
    grok.layer(JSONRestLayer)
    grok.context(IProductFolder)
    grok.require('zope.View')

    def GET(self):
        context = self.context
        container = dict(id=context.__name__, items=[])
        for id, obj in self.context.items():
            state = titleForState(IWorkflowState(obj).getState())
            container['items'].append(
                    {'meta_type': obj.meta_type,
                        '@url': 'http://www.google.de',
                        'id': obj.__name__,
                        'titel': obj.title,
                        'author': obj.principal.id,
                        'datum': obj.modtime.strftime('%d.%m.%Y'),
                        'status': state}
            )
        self.request.response.setHeader('Access-Control-Allow-Origin', '*')
        return json.dumps(container)

    def PUT(self):
        errors = []
        content = self.context.getContentType()()
        interface = content.schema[0]
        serializer = IJSONSerializer(content)
        serializer.work(self.body, interface, errors)
        if not errors:
            self.context.add(content)
            result = dict(
                result='success',
                name=content.meta_type,
                id=content.__name__
            )
            grok.notify(AfterSaveEvent(content, self.request))
        else:
            result = errors
        return json.dumps(result) 


class ContentRest(grok.REST):
    grok.layer(JSONRestLayer)
    grok.context(uvcsite.IContent)
    grok.require('zope.View')

    def GET(self):
        context = self.context
        schema = context.schema[0]
        return serialize(schema, context)


class IJSONSerializer(Interface):
    """ Base Serialzer for IContent Objects
    """

    def work(payload, interface, errors):
        """ Worker which populates self.context
            with the contents of the payload and
            with the help of interface
        """


@implementer(IJSONSerializer)
class DefaultSerializer(grok.Adapter):
    """ Default Serializer for IContent
    """
    grok.context(IContent)

    def work(self, payload, interface, errors):
        try:
            deserialize(payload, interface, self.context)
        except Exception, e:  # Here should be a DeserializeError
            for field, (exception, element) in e.field_errors.items():
                error = dict(
                    field=field.__name__,
                    message=exception.__doc__,
                )
                errors.append(error)
        try:
            interface.validateInvariants(self.context)
        except Invalid, e:
            errors.append(dict(text="Invariant: %s" % e))
