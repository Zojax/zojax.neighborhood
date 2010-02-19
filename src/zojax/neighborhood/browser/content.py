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
import cgi
import sys
import logging
import pytz

import transaction

from zope import interface, schema, component

from zojax.content.browser.table import ContainerListing
from zojax.catalog.interfaces import ICatalog

from zojax.neighborhood.interfaces import _

from interfaces import INeighborhoodType


class NeighborhoodContentsTable(ContainerListing):
    component.adapts(interface.Interface, interface.Interface, interface.Interface)
    
    msgEmptyTable = _(u'There are no neighborhood recent items.')
    
    enabledColumns = ('modified', 'icon', 'title')
    
    def initDataset(self):
        catalog = component.getUtility(ICatalog)
        self.dataset = catalog.searchResults(typeType={'any_of': ('Portal type',)},
                                             isDraft={'any_of': (False,)},
                                             sort_order='reverse', 
                                             sort_on='modified')
        
    def records(self):
        if self.batch is not None:
            for content in self.batch:
                yield self.RecordClass(self, content)
        else:
            for content in self.dataset:
                yield self.RecordClass(self, content)
                

class NeighborhoodTypeContentsTable(NeighborhoodContentsTable):
    
    component.adapts(INeighborhoodType, interface.Interface, interface.Interface)
    
    msgEmptyTable = _(u'There are no neighborhood recent items of this content type.')
    
    def initDataset(self):
        catalog = component.getUtility(ICatalog)
        self.dataset = catalog.searchResults(type={'any_of': (self.context.contenttype.name,)},
                                             isDraft={'any_of': (False,)},
                                             sort_order='reverse', 
                                             sort_on='modified')
