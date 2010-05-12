"""
.. :doctest:
.. :layer: uvcsite.tests.FunctionalLayer


Events which set all the ProductFolders
=======================================

Setup
-----

  >>> import grok
  >>> from zope.app.testing.functional import getRootFolder
  >>> from zope.app.publication.zopepublication import ZopePublication
  >>> from grok.testing import grok_component

Before we fire up the DatabaseOpendEvent we have to prepare a ZODB

  >>> from ZODB.tests.util import DB
  >>> from zope.app.appsetup import bootstrap
  >>> import zope.processlifetime
  >>> from zope.app.component.hooks import getSite, setSite

  >>> db = DB()
  >>> bootstrap.bootStrapSubscriber(zope.processlifetime.DatabaseOpened(db))
  >>> conn = db.open()
  >>> root = conn.root()

Let's put our app in the ZODB

  >>> from uvcsite.app import Uvcsite
  >>> app = Uvcsite() 
  >>> app
  <uvcsite.app.Uvcsite object at ...>

  >>> root[ZopePublication.root_name]['app'] = app
  >>> setSite(root[ZopePublication.root_name]['app'])

We need an empty HomeFolder for checking if the assigment of
our Product folders work. This means i add the user lars to
the HomeFolderManager

  >>> from zope.component import getUtility
  >>> from zope.app.homefolder.interfaces import IHomeFolderManager
  >>> utility = getUtility(IHomeFolderManager)
  >>> utility
  <uvcsite.homefolder.homefolder.PortalMembership object at ...>

Creating product folders in a new home folder
---------------------------------------------

We create a HomeFolder for lars:

  >>> utility.assignHomeFolder('lars')
  >>> 'lars' in utility.homeFolderBase
  True

All known product folder types have been instantiated and added to the home
folder in the process:

  >>> lars = utility.homeFolderBase['lars']
  >>> list(lars)
  [u'adressbook']

Creating product folders when opening the DB
--------------------------------------------

In order to see the effect, we need to empty the home folder first:

  >>> for name in list(lars.keys()): del lars[name]
  >>> list(lars)
  []

  >>> import zope.app.appsetup.interfaces
  >>> grok.notify(zope.app.appsetup.interfaces.DatabaseOpenedWithRoot(db))

After firing the event, all the product folders should be there again in the
home folder:

  >>> list(lars)
  [u'adressbook']

"""
