##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, schema
from zope.security import checkPermission
from zope.component import \
    getAdapters, getMultiAdapter, queryMultiAdapter, queryAdapter, getUtilitiesFor
from zope.traversing.browser import absoluteURL
from z3c.breadcrumb.interfaces import IBreadcrumb

from zojax.layoutform import Fields, PageletEditForm
from zojax.content.forms.interfaces import IContentWizard
from zojax.content.type.interfaces import IPortalType

from zojax.neighborhood.interfaces import INeighborhoodWorkspace
from interfaces import INeighborhoodType



class NeighborhoodLayout(object):

    types = ()
    type = None

    def update(self):
        super(NeighborhoodLayout, self).update()

        wsname = u''
        ws = self.mainview
        while not INeighborhoodWorkspace.providedBy(ws):
            if INeighborhoodType.providedBy(ws):
                wsname = ws.__name__
                break
            ws = ws.__parent__

        if not wsname:
            wsname = self.mainview.__name__
            
        self.type = ws

        context = self.context
        request = self.request

        self.title = getMultiAdapter((context, request), IBreadcrumb).name
        
        types = []
        for name, type in getUtilitiesFor(IPortalType):
            types.append(
                 {'name': name,
                  'title': type.title,
                  'description': type.description,
                  'selected': name == wsname,
                  'icon': queryMultiAdapter((type, request), name='zmi_icon'),
                  })
        self.types = types

        