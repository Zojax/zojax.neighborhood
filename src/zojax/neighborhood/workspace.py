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
from zope.location import Location

from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory
from zojax.geotargeting.interfaces import IGeotargetingPreference
from zojax.authentication.utils import getPrincipal
from zojax.content.type.container import ContentContainer

from interfaces import _, INeighborhoodWorkspace, INeighborhoodWorkspaceFactory


class NeighborhoodWorkspace(ContentContainer):
    interface.implements(INeighborhoodWorkspace)

    __name__ = 'neighborhood'
    title = _(u'My neighborhood')


class NeighborhoodWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(INeighborhoodWorkspaceFactory)

    name = 'neighborhood'
    title = _(u'My neighborhood')
    description = _(u'My neighborhood workspace')
    weight = 123
    
    factory = NeighborhoodWorkspace

    def isAvailable(self):
        preference = IGeotargetingPreference(getPrincipal(), None)
        if preference is not None:
            return preference.enabled