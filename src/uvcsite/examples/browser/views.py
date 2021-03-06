# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope.interface import Interface
from uvcsite.interfaces import IMyHomeFolder, IUVCSite, IDocumentActions
from megrok.z3ctable import TablePage, Column, table
import uvcsite
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from uvc.layout.slots.interfaces import IRenderable
from grokcore.chameleon.components import ChameleonPageTemplateFile




class LogoutMenu(uvcsite.MenuItem):
    grok.name('Logout')
    grok.title('Logout')
    grok.require('zope.View')
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    action = "logout"


class Logout(grok.View):
    """ Logout View
    """
    grok.name('Logout')
    grok.title('Logout')
    grok.require('zope.View')
    grok.context(uvcsite.IUVCSite)
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    KEYS = ("beaker.session", "dolmen.authcookie")

    def update(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            for key in self.KEYS:
                self.request.response.expireCookie(key, path='/')

    def render(self):
        return self.redirect(self.application_url())




class Index(uvcsite.Page):
    grok.title('Startseite')
    grok.context(IUVCSite)
    grok.require('zope.View')

    def update(self):
        self.flash('Fehlermeldung KLAUSi ERNST', 'error')
        self.flash('Warnung...', 'warning')

