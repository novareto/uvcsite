#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import grok

from hurry.workflow.interfaces import IWorkflowState
from uvcsite.content import IProductFolder
from uvcsite.workflow.basic_workflow import titleForState


class ArchiveLayer(grok.IRESTLayer):
    """ Layer for Archive Access"""
    grok.restskin('archive')


class ArchiveProductFolderRest(grok.REST):
    grok.layer(JSONRestLayer)
    grok.context(IProductFolder)
    grok.require('zope.Public')

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
