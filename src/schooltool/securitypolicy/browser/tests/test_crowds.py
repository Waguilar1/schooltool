#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2005 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Tests for registered security descriptions.

$Id$
"""

import unittest
from zope.testing import doctest

from schooltool.schoolyear.testing import (setUp, tearDown,
                                           provideStubUtility,
                                           provideStubAdapter)
from schooltool.securitypolicy.ftesting import securitypolicy_functional_layer

from schooltool.securitypolicy.metaconfigure import getCrowdsUtility
from schooltool.securitypolicy.metaconfigure import getDescriptionUtility


def collectActionsByDiscriminator():
    util = getDescriptionUtility()
    collected = {}
    for group in util.actions_by_group.values():
        for action in group.values():
            discriminator = (action.permission, action.interface)
            if discriminator not in collected:
                collected[discriminator] = []
            collected[discriminator].append(action)
    for actions in collected.values():
        actions[:] = sorted(actions,
                            key=lambda a: a.__name__ + a.__parent__.__name__)
    return collected


def doctest_described_interfaces():
    r"""This is a crude attempt to list interfaces that are described in the
    security overview pages.

        >>> actions = collectActionsByDiscriminator()
        >>> crowds = getCrowdsUtility().crowds.keys()

        >>> described = set(actions) & set(crowds)
        >>> missing = set(crowds) - set(actions)

        >>> def make_key(disc):
        ...     if disc[1] is None:
        ...         return ('', 'None', disc[0])
        ...     return (str(disc[1].__module__), str(disc[1].__name__), disc[0])

    Interfaces/permission pair represents things the user can do in SchoolTool.

    Each interface/permission pair has a list of object/action pairs.
    The "object" is a rough approximation on SchoolTool object model, from
    the user's perspective.  The "action" is an approximation of things user
    can do on the "object" if he has the required permission.

    Note the descriptions are sorted by modules of interfaces.  Some of the
    descriptions are declared in zcml, residing in other modules than the
    original interface.

    When you notice an "object" seemingly not belonging to the module of the
    interface (say, "Demographics"/"stuff" in schooltool.app.interfaces),
    this usually means one of the following:

    - The "object" has an functional extension on the described interface.

    - The "object" did not define it's own permissions and in reality inherits
      them from the parent.

    - There is a bug in zcml that registers the description.

        >>> last_module = ''
        >>> util = getDescriptionUtility()
        >>> for disc in sorted(described, key=make_key):
        ...     mod, ifc, perm = make_key(disc)
        ...     if mod != last_module:
        ...         last_module = mod
        ...         print '-' * len(last_module)
        ...         print last_module
        ...         print '-' * len(last_module)
        ...
        ...     print '- %s, %s' % (ifc, perm)
        ...     listed = [
        ...         str('%s / %s' % (util.groups[a.__parent__.__name__].title,
        ...                          a.title))
        ...         for a in actions[disc]]
        ...     for act in listed:
        ...         print '-  %s' % act
        ...     print '-'
        -------------------------
        schooltool.app.interfaces
        -------------------------
        - ISchoolToolApplication, schooltool.edit
        -  School Years / Activate current school year
        -  Contacts / Create/Delete an external contact
        -  School Years / Create/Delete
        -  Demographics / Manage
        -  SchoolTool application / Manage school settings and configuration
        -  Contacts / Modify an external contact
        -  School Years / Modify
        -
        - ISchoolToolApplication, schooltool.view
        -  School Years / List
        -  SchoolTool application / Access
        -  School Years / View
        -
        - ISchoolToolCalendar, schooltool.edit
        -  SchoolTool application / Change calendar
        -  Sections / Change calendar
        -  Groups / Change calendar
        -  Users / Change calendar
        -  Reservations / Schedule reservation via calendar
        -
        - ISchoolToolCalendar, schooltool.view
        -  SchoolTool application / View calendar
        -  Sections / View calendar
        -  Groups / View calendar
        -  Users / View calendar
        -  Reservations / View reservation calendar
        -
        ---------------------------------
        schooltool.basicperson.interfaces
        ---------------------------------
        - IFieldDescription, schooltool.edit
        -  Demographics / Edit fields
        -
        ------------------------------
        schooltool.contact.basicperson
        ------------------------------
        - IBoundContact, schooltool.view
        -  Contacts / View user's contact information
        -
        -----------------------------
        schooltool.contact.interfaces
        -----------------------------
        - IContact, schooltool.view
        -  Contacts / View an external contact
        -
        - IContactContainer, schooltool.view
        -  Contacts / List/Search
        -
        ----------------------------
        schooltool.course.interfaces
        ----------------------------
        - ICourse, schooltool.edit
        -  Courses / Modify
        -
        - ICourse, schooltool.view
        -  Courses / View
        -
        - ICourseContainer, schooltool.edit
        -  Courses / Create/Delete
        -
        - ICourseContainer, schooltool.view
        -  Courses / List
        -
        - ISection, schooltool.edit
        -  Sections / Change schedule
        -  Sections / Assign timetables
        -  Sections / Modify
        -
        - ISection, schooltool.view
        -  Sections / View
        -
        - ISectionContainer, schooltool.edit
        -  Sections / Create/Delete
        -
        - ISectionContainer, schooltool.view
        -  Sections / List
        -
        ---------------------------
        schooltool.group.interfaces
        ---------------------------
        - IGroup, schooltool.edit
        -  Groups / Modify
        -
        - IGroup, schooltool.view
        -  Groups / View
        -
        - IGroupContainer, schooltool.edit
        -  Groups / Create/Delete
        -
        - IGroupContainer, schooltool.view
        -  Groups / List
        -
        ----------------------------
        schooltool.person.interfaces
        ----------------------------
        - IPasswordWriter, schooltool.edit
        -  Users / Change password
        -
        - IPerson, schooltool.edit
        -  Demographics / Modify user demographics
        -  Contacts / Manage user's contacts
        -  Contacts / Modify user's contact information
        -  Users / Modify
        -
        - IPerson, schooltool.editCalendarOverlays
        -  Users / Manage visible calendars
        -
        - IPerson, schooltool.view
        -  Demographics / View user demographics
        -  Users / View
        -
        - IPersonContainer, schooltool.edit
        -  Users / Create/Delete
        -
        - IPersonContainer, schooltool.view
        -  Users / List/Search
        -
        - IPersonPreferences, schooltool.edit
        -  Users / Change preferences
        -
        - IPersonPreferences, schooltool.view
        -  Users / View preferences
        -
        ------------------------------
        schooltool.resource.interfaces
        ------------------------------
        - IBaseResource, schooltool.edit
        -  Reservations / Modify a resource
        -
        - IBaseResource, schooltool.view
        -  Reservations / View a resource
        -
        - IResourceContainer, schooltool.edit
        -  Reservations / Add/Remove resources
        -
        - IResourceContainer, schooltool.view
        -  Reservations / List/Search resources
        -
        --------------------------
        schooltool.term.interfaces
        --------------------------
        - ITermContainer, schooltool.edit
        -  Terms / Create/Delete
        -  Terms / Modify
        -
        - ITermContainer, schooltool.view
        -  Terms / List
        -  Terms / View
        -
        -------------------------------
        schooltool.timetable.interfaces
        -------------------------------
        - ITimetableSchemaContainer, schooltool.edit
        -  School timetables / Create/Delete
        -  School timetables / Modify
        -
        - ITimetableSchemaContainer, schooltool.view
        -  School timetables / List/Search
        -  School timetables / View
        -

    Some of the interface/permission pairs are intentionally (or by mistake!)
    not presented to the user.

        >>> for disc in sorted(missing, key=make_key):
        ...     mod, ifc, perm = make_key(disc)
        ...     if mod != last_module:
        ...         last_module = mod
        ...         print '-' * len(last_module)
        ...         print last_module
        ...         print '-' * len(last_module)
        ...     print '%s, %s' % (ifc, perm)
        None, zope.ManageApplication
        None, zope.ManageServices
        None, zope.View
        None, zope.app.dublincore.change
        None, zope.app.dublincore.view
        -------------------------
        schooltool.app.interfaces
        -------------------------
        ISchoolToolApplication, zope.ManageSite
        ----------------------------------
        schooltool.relationship.interfaces
        ----------------------------------
        IRelationshipLink, schooltool.edit
        IRelationshipLink, schooltool.view
        --------------------------
        schooltool.term.interfaces
        --------------------------
        IDateManager, schooltool.edit
        IDateManager, schooltool.view

        >>> print 'Total undescribed interface permissions: %d of %d (%d done)' % (
        ...     len(missing), len(crowds), len(actions))
        Total undescribed interface permissions: 10 of 46 (36 done)

    """


def test_suite():
    optionflags = (doctest.NORMALIZE_WHITESPACE |
                   doctest.ELLIPSIS |
                   doctest.REPORT_NDIFF)
    suite = doctest.DocTestSuite(optionflags=optionflags,
                                 extraglobs={'provideAdapter': provideStubAdapter,
                                             'provideUtility': provideStubUtility},
                                 setUp=setUp, tearDown=tearDown)
    suite.layer = securitypolicy_functional_layer
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')