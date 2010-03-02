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
from zope import interface, component
from zope.location import LocationProxy
from zope.component import getUtility, queryMultiAdapter
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from z3c.traverser.interfaces import ITraverserPlugin

from zojax.content.type.interfaces import IPortalType

from zojax.neighborhood.interfaces import INeighborhoodWorkspace
from neighborhood import NeighborhoodType


class NeighborhoodPublisher(object):
    interface.implements(ITraverserPlugin)
    component.adapts(INeighborhoodWorkspace, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context
        ctype = component.queryUtility(IPortalType, name=name)
        if ctype is not None:
            return LocationProxy(NeighborhoodType(ctype), context, name)
        view = queryMultiAdapter((context, request), name=name)
        if view is not None:
            return view

        raise NotFound(context, name, request)

    def browserDefault(self, request):
        return self, ('index.html',)
