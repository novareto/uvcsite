# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from grokcore.rest.interfaces import IRESTLayer
from megrok.pagetemplate import PageTemplate
from megrok.z3ctable import Values
from uvc.layout import interfaces, TablePage
from uvcsite import uvcsiteMF as _
from uvcsite.content.productregistration import getAllProductRegistrations
from uvcsite.homefolder.homefolder import Members
from uvcsite.interfaces import IMyHomeFolder, IFolderListingTable
from zope.component import getMultiAdapter
from zope.interface import Interface, implementer
from zope.pagetemplate.interfaces import IPageTemplate
from zope.traversing.browser import absoluteURL


grok.templatedir('templates')


@implementer(IFolderListingTable)
class Index(TablePage):
    grok.title(u'Mein Ordner')
    grok.context(IMyHomeFolder)
    grok.require('uvc.AccessHomeFolder')
    # uvcsite.sectionmenu(uvcsite.IExtraViews)

    cssClasses = {
        'table': ('tablesorter table table-striped '
                  + 'table-bordered table-condensed')}
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    startBachtAt = 15
    bachtSize = 15
    sortOn = "table-modified-5"

    @property
    def title(self):
        name = self.request.principal.title
        return u"Ordner von %s" % name

    description = _(u"Hier werden Ihre Dokumente abgelegt")

    def getContentTypes(self):
        interaction = self.request.interaction
        for key, value in self.context.items():
            if (interaction.checkPermission('uvc.ViewContent', value)
                and not getattr(value, 'excludeFromNav', False)):
                yield dict(
                    href=absoluteURL(value, self.request), name=key)

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def update(self):
        items = self.request.form.get('table-checkBox-0-selectedItems')
        if items and 'form.button.delete' in self.request:
            if isinstance(items, (str, unicode)):
                items = [items]
            for key in items:
                for pf in self.context.values():
                    if key in pf:
                        self.executeDelete(pf[key])
        super(Index, self).update()

    def renderCell(self, item, column, colspan=0):
        from z3c.table import interfaces
        if interfaces.INoneCell.providedBy(column):
            return u''
        cssClass = column.cssClasses.get('td')
        cssClass = self.getCSSHighlightClass(column, item, cssClass)
        cssClass = self.getCSSSortClass(column, cssClass)
        cssClass = self.getCSSClass('td', cssClass)
        colspanStr = colspan and ' colspan="%s"' % colspan or ''
        dt = ' data-title="%s" ' % column.header
        return u'\n      <td%s%s%s>%s</td>' % (
            cssClass, colspanStr, dt, column.renderCell(item))


class DirectAccessViewlet(grok.Viewlet):
    grok.view(IFolderListingTable)
    grok.order(25)
    grok.context(Interface)
    grok.viewletmanager(interfaces.ITabs)

    def getContentTypes(self):
        interaction = self.request.interaction
        hf = uvcsite.getHomeFolder(self.request)
        for key, value in getAllProductRegistrations():
            if getattr(value, 'inNav', True):
                pf = hf[value.folderURI]
                if interaction.checkPermission('uvc.ViewContent', pf):
                    yield dict(href=absoluteURL(pf, self.request),
                               name=value.title)

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class DirectAccess(PageTemplate):
    grok.view(DirectAccessViewlet)


class HomeFolderValues(Values):
    """This Adapter returns IContent Objects form child folders.
    """
    grok.adapts(IMyHomeFolder, None, Index)

    @property
    def values(self):
        results = []
        interaction = self.request.interaction
        for productfolder in self.context.values():
            if interaction.checkPermission('uvc.ViewContent', productfolder):
                if not productfolder.__name__.startswith('__'):
                    for obj in productfolder.values():
                        if interaction.checkPermission('uvc.ViewContent', obj):
                            results.append(obj)
        return results


class RedirectIndexMembers(grok.View):
    grok.context(Members)
    grok.name('index')

    def render(self):
        url = uvcsite.IGetHomeFolderUrl(self.request).getURL()
        self.redirect(url)


class RestHomeFolderTraverser(grok.Traverser):
    grok.context(Members)
    grok.layer(IRESTLayer)
    # grok.baseclass()

    def traverse(self, name):
        return uvcsite.getHomeFolder(self.request).get(name)
