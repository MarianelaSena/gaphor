from gaphor.tests import TestCase
from gaphor import UML
from gaphor.diagram.classes import AssociationItem, ClassItem
from gaphas.aspect import ConnectionSink


class GaphasTest(TestCase):

    services = TestCase.services + ["sanitizer_service", "undo_manager"]

    def test_remove_class_with_association(self):
        c1 = self.create(ClassItem, UML.Class)
        c1.name = "klassitem1"
        c2 = self.create(ClassItem, UML.Class)
        c2.name = "klassitem2"

        a = self.create(AssociationItem)

        assert 3 == len(self.diagram.canvas.get_all_items())

        self.connect(a, a.head, c1)
        self.connect(a, a.tail, c2)

        assert a.subject
        assert (
            self.element_factory.lselect(lambda e: e.isKindOf(UML.Association))[0]
            is a.subject
        )

        c1.unlink()

        self.diagram.canvas.update_now()
