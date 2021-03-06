# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import transaction
import zope.schema
import zope.interface
import zope.component
import zope.security

from StringIO import StringIO
from hurry.workflow.interfaces import IWorkflowInfo
from uvc.validation import validation
from uvcsite.content.directive import productfolder
from uvcsite.content.productregistration import ProductMenuItem
from uvcsite.content.productregistration import ProductRegistration
from xml.dom.minidom import parseString


desc_name = (
    u"""Wie ist Ihr <a rel="tooltip" href="#" """ +
    u"""data-original-title="Default tooltip">Name</a>""")


class IContact(uvcsite.IContent):

    name = zope.schema.TextLine(
        title=u"Name",
        description=desc_name,
    )

    alter = zope.schema.TextLine(
        title=u"Alter",
        description=u"Wie ist ihr Alter",
        required=False,
        constraint=validation.validateZahl,
    )


class IAdressBook(uvcsite.IProductFolder):
    """ Marker Interface """


@zope.interface.implementer(IContact)
class Contact(uvcsite.Content):
    grok.name(u'Kontakt')
    uvcsite.schema(IContact)


@zope.interface.implementer(IAdressBook)
class AdressBook(uvcsite.ProductFolder):
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Adressbuch ...')
    uvcsite.contenttype(Contact)

    @property
    def excludeFromNav(self):
        interaction = zope.security.management.getInteraction()
        principal = interaction.participations[0].principal
        if principal.id == "0202020002":
            return True
        return False


class Stat(uvcsite.Page):
    grok.name('stat')
    grok.title('Statistik LONG LONG LONG')
    grok.context(AdressBook)
    viewName = "stat"
    title = "title"

    def render(self):
        return "<div> <h1>Statistiks</h1> </div>"


@grok.subscribe(Contact, uvcsite.IAfterSaveEvent)
def handle_save(obj, event):
    sp = transaction.savepoint()
    wf = IWorkflowInfo(obj)
    try:
        1 / 0
        if True:
            wf.fireTransition('review')
            uvcsite.log('add Document in state review')
        else:
            pdf = zope.component.getMultiAdapter((obj, event.request), name=u"pdf")
            pdf.create(fn="/tmp/kk/%s.pdf" % (obj.__name__))
            wf.fireTransition('publish')
    except StandardError, e:
        sp.rollback()
        wf.fireTransition('progress')
        uvcsite.logger.exception("ES IST EIN FEHLER AUFGETRETEN")
        uvcsite.log('simpleaddon', e.__doc__)
    print "AfterSaveEvent"


class AddMenuEntry(ProductMenuItem):
    grok.name('Buddy erstellen')
    grok.title('Buddy erstellen')
    grok.context(zope.interface.Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)

    @property
    def reg_name(self):
        return "adressbook"


class Addressbook(ProductRegistration):
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Beschreibung Entgeltnachweis')
    productfolder('uvcsite.examples.simpleaddon.AdressBook')


def kopf(c):
    c.drawString(200, 200, u"Ich bin der KOPF")


class KontaktPdf(uvcsite.BasePDF):
    grok.context(IContact)
    grok.name('pdf')

    def generate(self):
        c = self.c
        kopf(c)
        c.drawString(100, 100, "Hello World")
        c.drawString(300, 300, self.request.principal.id)
        c.drawString(400, 400, self.context.name)
        c.showPage()


class KontaktXML(uvcsite.BaseXML):
    grok.context(IContact)
    grok.name('xml')
    grok.title('kontakt.xml')

    def generate(self):
        io = StringIO()
        #w = XMLWriter(io, encoding="utf-8")
        #kon = w.start('kontakt')
        #w.start('basis')
        #w.element('creator', self.request.principal.id)
        #w.element('name', self.context.name)
        #w.end()
        #w.close(kon)
        #io.seek(0)
        self.xml_file.write(parseString(io.read()).toprettyxml(indent="  "))
