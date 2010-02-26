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
from zope.location import LocationProxy, ILocation, Location
from zope.publisher.interfaces import NotFound, IPublishTraverse

from zojax.content.type.interfaces import IPortalType
from zojax.layoutform import Fields, PageletEditSubForm

from zojax.neighborhood.interfaces import _, INeighborhoodWorkspace

from interfaces import INeighborhoodType


class NeighborhoodWorkspaceView(object):
        
    def publishTraverse(self, request, name):
        ctype = component.queryUtility(IPortalType, name=name)
        if ctype is not None:
            return LocationProxy(NeighborhoodType(ctype), self, name)
        view = component.queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view
        raise NotFound(self, name, request)
    
    def browserDefault(self, request):
        return self, ('index.html',)
        
    
class NeighborhoodType(Location):
    
    interface.implements(INeighborhoodType)
    
    def __init__(self, contenttype):
        self.contenttype = contenttype
        
        