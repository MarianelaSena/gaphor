"""
Unnit tests for AssociationItem.
"""

from gaphor.tests import TestCase
from gaphor import UML
from gaphor.diagram.usecases.usecase import UseCaseItem
from gaphor.diagram.usecases.actor import ActorItem
from gaphor.diagram.classes.klass import ClassItem
from gaphor.diagram.classes.interface import InterfaceItem
from gaphor.diagram.classes.association import AssociationItem


class AssociationItemTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.assoc = self.create(AssociationItem)
        self.class1 = self.create(ClassItem, UML.Class)
        self.class2 = self.create(ClassItem, UML.Class)

    def test_create(self):
        """Test association creation and its basic properties
        """
        self.connect(self.assoc, self.assoc.head, self.class1)
        self.connect(self.assoc, self.assoc.tail, self.class2)

        assert isinstance(self.assoc.subject, UML.Association)
        assert self.assoc.head_end.subject is not None
        assert self.assoc.tail_end.subject is not None

        assert not self.assoc.show_direction

        self.assoc.show_direction = True
        assert self.assoc.show_direction

    def test_invert_direction(self):
        """Test association direction inverting
        """
        self.connect(self.assoc, self.assoc.head, self.class1)
        self.connect(self.assoc, self.assoc.tail, self.class2)

        head_subject = self.assoc.subject.memberEnd[0]
        tail_subject = self.assoc.subject.memberEnd[1]

        self.assoc.invert_direction()

        assert head_subject is self.assoc.subject.memberEnd[1]
        assert tail_subject is self.assoc.subject.memberEnd[0]

    def test_association_end_updates(self):
        """Test association end navigability connected to a class"""
        from gaphas.canvas import Canvas

        canvas = Canvas()
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)
        a = self.create(AssociationItem)

        self.connect(a, a.head, c1)
        c = self.get_connected(a.head)
        assert c is c1

        self.connect(a, a.tail, c2)
        c = self.get_connected(a.tail)
        assert c is c2

        assert a.subject.memberEnd, a.subject.memberEnd

        assert a.subject.memberEnd[0] is a.head_end.subject
        assert a.subject.memberEnd[1] is a.tail_end.subject
        assert a.subject.memberEnd[0].name is None

        a.subject.memberEnd[0].name = "blah"
        self.diagram.canvas.update()

        assert a.head_end._name == "+ blah", a.head_end.get_name()

    def test_association_orthogonal(self):
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)
        a = self.create(AssociationItem)

        self.connect(a, a.head, c1)
        c = self.get_connected(a.head)
        assert c is c1

        a.matrix.translate(100, 100)
        self.connect(a, a.tail, c2)
        c = self.get_connected(a.tail)
        assert c is c2

        try:
            a.orthogonal = True
        except ValueError:
            pass  # Expected, hanve only 2 handles, need 3 or more
        else:
            assert False, "Can not set line to orthogonal with less than 3 handles"
