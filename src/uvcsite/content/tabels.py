# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite import uvcsiteMF as _
from megrok.z3ctable import (table,
    Column, GetAttrColumn, CheckBoxColumn, LinkColumn, ModifiedColumn)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState
from uvcsite.interfaces import IFolderColumnTable
from zope.traversing.browser import absoluteURL
from uvcsite.homefolder.views import Index

class CheckBox(CheckBoxColumn):
    grok.name('checkBox')
    grok.context(IFolderColumnTable)
    #table(Index)
    weight = 0
    cssClasses = {'th': 'checkBox'}
    header = u""
    
    def renderCell(self, item):
        state = IWorkflowState(item).getState()
        if state != None:
            state = titleForState(state)
        if state == "Entwurf":
            return CheckBoxColumn.renderCell(self, item)
        return ''    


class Link(LinkColumn):
    grok.name('link')
    grok.context(IFolderColumnTable)
    weight = 1
    #table(Index)
    header = _(u"Titel")
    linkName = u"edit"

    def getLinkURL(self, item):
        """Setup link url."""
        state = IWorkflowState(item).getState()
        if state != None:
            state = titleForState(state)
        if self.linkName is not None and state == "Entwurf":
            return '%s/%s' % (absoluteURL(item, self.request), self.linkName)
        return absoluteURL(item, self.request)

    def getLinkContent(self, item):
        return item.title


class MetaTypeColumn(GetAttrColumn):
    grok.name('meta_type')
    grok.context(IFolderColumnTable)
    header = _(u'Objekt')
    attrName = 'meta_type'
    weight = 2
    #table(Index)


class CreatorColumn(Column):
    grok.name('creator')
    grok.context(IFolderColumnTable)
    header = _(u"Autor")
    weight = 99
    #table(Index)

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(ModifiedColumn):
    grok.name('modified')
    grok.context(IFolderColumnTable)
    header = _(u"Datum")
    weight = 100
    #table(Index)


class StateColumn(GetAttrColumn):
    grok.name('state')
    grok.context(IFolderColumnTable)
    header = _(u'Status')
    attrName = 'status'
    weight = 3
    #table(Index)

    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state != None:
            return titleForState(state)
        return self.defaultValue
