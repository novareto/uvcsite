#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
import uvcsite

from dolmen.security.policies.principalrole import ExtraRoleMap
from zope import interface
from zope.interface import implementer
from zope.schema import Choice
from zope.securitypolicy.interfaces import Allow
from zope.securitypolicy.securitymap import SecurityMap
from zope.securitypolicy.zopepolicy import settingsForObject
from zope.securitypolicy.interfaces import (
     IPrincipalRoleManager, IPrincipalRoleMap, IRolePermissionMap)

from uvcsite.interfaces import IMyHomeFolder
from uvcsite.extranetmembership.interfaces import (
    IUserManagement, IExtranetMember)


class User(dict):
    pass


USERS = [
    User(**{
        'mnr':'0101010001', 'az': '00', 'passwort':'passwort',
        'email':'ck@novareto.de', 'rollen':['Adressbook']}),
    User(**{
        'mnr':'0202020002', 'az': '00', 'passwort':'passwort',
        'email':'test@test.de', 'rollen':[]}),
    User(**{
        'mnr':'0101010001-q', 'az': '-q', 'passwort':'passwort',
        'email':'test@test.de', 'rollen':['Adressbook']}),
    User(**{
        'mnr':'0101010001', 'az': '01', 'passwort':'passwort',
        'email':'ck1@novareto.de', 'rollen':['Adressbook']}),
    User(**{
        'mnr':'0101010001', 'az': '02', 'passwort':'passwort',
        'email':'test@test.de', 'rollen':[]}),
    User(**{
        'mnr':'0101010002', 'az': '02', 'passwort':'passwort',
        'email':'test@test.de'}),
    User(**{
        'mnr':'0101010002', 'az': '03', 'passwort':'passwort',
        'email':'test@test.de'}),
    User(**{
        'mnr':'lars', 'az': '00', 'passwort':'passwort',
        'email':'test@test.de', 'rollen':[]}),
]


class HierarchyUser(IExtranetMember):
    department = Choice(
        title=u'Department',
        required=True,
        values=['IT', 'Human resources'],
        )


@implementer(IUserManagement)
class UserManagement(grok.GlobalUtility):
    """Utility for Usermanagement.
    """

    UserInterface = HierarchyUser

    def updUser(self, **kwargs):
        """Updates a User"""
        cn = '%s-%s' % (kwargs['mnr'], kwargs['az'])
        user = self.getUser(cn)
        user.update(**kwargs)

    def deleteUser(self, cn):
        user = self.getUser(cn)
        USERS.remove(user)

    def addUser(self, **kwargs):
        """Adds a User"""
        mnr, az = kwargs['mnr'].split('-')
        USERS.append(User(mnr=mnr,
                          az=az,
                          roles=kwargs['rollen'],
                          passwort=kwargs.get('passwort')))

    def zerlegUser(self, mnr):
        ll = mnr.split('-')
        if len(ll) == 1:
            return mnr, '00'
        return ll

    def getUser(self, mnr):
        """Return a User"""
        mnr, az = self.zerlegUser(mnr)
        for user in USERS:
            if user.get('mnr') == mnr and user.get('az') == az:
                return user
        return None

    def getUsersByMnr(self, mnr):
        for user in USERS:
            if user['mnr'] == mnr:
                yield user
    
    def getUserByEMail(self, mail):
        for user in USERS:
            if user.get('email') == mail:
                return user
        return None

    def getUserGroups(self, mnr):
        """Return a group of Users"""
        ret = []
        for x in USERS:
            usr = "%s-%s" % (x['mnr'], x['az'])
            ret.append(User(cn=usr, mnr=x['mnr'], rollen=x.get('rollen', []), az=x.get('az')))
        return ret

    def updatePasswort(self, **kwargs):
        """Change a passwort from a user"""

    def checkRule(self, login):
        uvcsite.log(login)
        return True


class ViewPermission(grok.View):
    grok.context(interface.Interface)

    def render(self):
        context = self.context
        print settingsForObject(context)
