import pytest
from gaphor.UML.elementfactory import ElementFactory
from gaphor.services.eventmanager import EventManager
from gaphor.storage.storage import load_elements
from gaphor.storage.parser import element, canvas, canvasitem
from gaphor.storage import diagramitems


@pytest.fixture
def element_factory():
    return ElementFactory(EventManager())


@pytest.fixture
def loader(element_factory):
    def _loader(*parsed_items):
        parsed_data = {
            "1": element(
                id="1", type="Diagram", canvas=canvas(canvasitems=parsed_items)
            ),
            **{p.id: p for p in parsed_items},
        }
        load_elements(parsed_data, element_factory)
        return element_factory.lselect()[0].canvas.get_root_items()[0]

    return _loader


def test_upgrade_metaclass_item_to_class_item(loader):
    item = loader(canvasitem(id="2", type="MetaclassItem"))

    assert type(item) == diagramitems.ClassItem


def test_upgrade_subsystem_item_to_class_item(loader):
    item = loader(canvasitem(id="2", type="SubsystemItem"))

    assert type(item) == diagramitems.ComponentItem


def test_rename_stereotype_attrs_field(loader):
    parsed_item = canvasitem(id="2", type="ClassItem")
    parsed_item.values["show_stereotypes_attrs"] = "1"
    item = loader(parsed_item)

    assert not hasattr(item, "show_stereotypes_attrs")
    assert item.show_stereotypes


def test_rename_show_attributes_and_operations_field(loader):
    parsed_item = canvasitem(id="2", type="ClassItem")
    parsed_item.values["show-attributes"] = "0"
    parsed_item.values["show-operations"] = "0"
    item = loader(parsed_item)

    assert not item.show_attributes
    assert not item.show_operations


def test_interface_drawing_style_normal(loader):
    parsed_item = canvasitem(id="2", type="InterfaceItem")
    parsed_item.values["drawing-style"] = "0"  # DRAW_NONE
    item = loader(parsed_item)

    assert item.folded.name == "NONE"


def test_interface_drawing_style_folded(loader):
    parsed_item = canvasitem(id="2", type="InterfaceItem")
    parsed_item.values["drawing-style"] = "3"  # DRAW_ICON
    item = loader(parsed_item)

    assert item.folded.name == "PROVIDED"
