# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from grok.interfaces import IContainer
from uvcsite import IContent
from zope.interface import Interface
from zope.schema import TextLine, Text
from uvcsite.interfaces import IFolderColumnTable


class IHelpFolder(IFolderColumnTable):
    pass


class IHelpPage(IContent):
    name = TextLine(title=u"Name")
    title = TextLine(title=u"title")
    text = Text(title=u"text")
