# -*- coding: utf-8 -*-

import grok
import megrok.layout

from uvcsite import uvcsiteMF as _
from uvcsite import ApplicationAwareView
from uvcsite.interfaces import IUVCSite
from uvcsite.auth.handler import setup_pau
from zope.app.security.interfaces import IAuthentication
from uvcsite.homefolder.homefolder import PortalMembership
from zope.app.authentication import PluggableAuthentication
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.publisher.interfaces import INotFound
from zope.publisher.interfaces import INotFound
from zope.interface.common.interfaces import IException
from zope.exceptions.interfaces import IUserError

from zope.app.exception.systemerror import SystemErrorView

from dolmen.app.site import Dolmen
from dolmen.app.layout import models, errors


class Uvcsite(Dolmen):
    """ Application Object for uvc.site"""
    grok.implements(IUVCSite)

    title = u"UVC Site by Novareto."

    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       setup=setup_pau)


class PersonalPanelView(models.Page):
    """ Page for Personal Properties """
    title = _(u"Persönliche Einstellungen")
    description = _(u"Hier können Sie Einstellungen zu"
                     " Ihrem Benutzerprofil vornehmen.")
    grok.require('zope.View')


class NotFound(errors.NotFound):
    pass
