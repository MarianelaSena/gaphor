from gaphor import UML
from gaphor.diagram.general import CommentItem
from gaphor.diagram.classes import AssociationItem, ClassItem
from gaphor.services.copyservice import CopyService
from gaphor.application import Application
from gaphor.tests.testcase import TestCase
from gaphor.storage.verify import orphan_references


class CopyServiceTestCase(TestCase):

    services = TestCase.services + [
        "main_window",
        "action_manager",
        "properties",
        "undo_manager",
    ]

    def setUp(self):
        super().setUp()
        self.service = CopyService(
            self.get_service("event_manager"),
            self.get_service("element_factory"),
            self.get_service("main_window"),
        )

    def test_copy(self):
        service = self.service

        ef = self.element_factory
        diagram = ef.create(UML.Diagram)
        ci = diagram.create(CommentItem, subject=ef.create(UML.Comment))

        service.copy([ci])
        assert diagram.canvas.get_all_items() == [ci]

        service.paste(diagram)

        assert len(diagram.canvas.get_all_items()) == 2, diagram.canvas.get_all_items()

    def _skip_test_copy_paste_undo(self):
        """
        Test if copied data is undoable.
        """

        service = self.service

        # Setting the stage:
        ci1 = self.create(ClassItem, UML.Class)
        ci2 = self.create(ClassItem, UML.Class)
        a = self.create(AssociationItem)

        self.connect(a, a.head, ci1)
        self.connect(a, a.tail, ci2)

        assert a.subject
        assert a.head_end.subject
        assert a.tail_end.subject

        # The act: copy and paste, perform undo afterwards
        service.copy([ci1, ci2, a])

        service.paste(self.diagram)

        all_items = list(self.diagram.canvas.get_all_items())

        assert 6 == len(all_items)
        assert not orphan_references(self.element_factory)

        assert all_items[0].subject is all_items[3].subject
        assert all_items[1].subject is all_items[4].subject
        assert all_items[2].subject is all_items[5].subject

        undo_manager = self.get_service("undo_manager")

        undo_manager.undo_transaction()

        assert 3 == len(self.diagram.canvas.get_all_items())
        assert not orphan_references(self.element_factory)
