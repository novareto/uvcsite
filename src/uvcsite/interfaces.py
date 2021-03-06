# -*- coding: utf-8 -*-

from grok.interfaces import IContainer
from grokcore.site import IApplication
from uvc.layout.interfaces import *  # BBB Exposing interfaces
from uvcsite.content.interfaces import IUVCApplication, IFolderColumnTable
from zope.interface import Interface


class IHomeFolderManager(Interface):
    """FIX ME
    """


class IGetHomeFolderUrl(Interface):
    """Marker Interface for getting HomeFolderUrls
    """


class IFolderListingTable(Interface):
    """Marker Interface for tables with a listing interface
       for contenttypes
    """


class IMyRoles(Interface):
    """Return all allowed Roles in various forms
    """


class IStammdaten(Interface):
    """Marker Interface for Stammdaten
    """


class IUVCSite(IApplication, IUVCApplication):
    """UVC-Site site object
    """


class IMyHomeFolder(IContainer, IFolderColumnTable):
    """Marker Interface for HomeFolder
    """


class IHomeFolder(IMyHomeFolder):
    """FIXME
    """
