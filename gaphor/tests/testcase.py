"""
Basic test case for Gaphor tests.

Everything is about services so the TestCase can define it's required
services and start off.
"""

import logging
import unittest
from io import StringIO

from gaphas.aspect import ConnectionSink, Connector

from gaphor import UML
from gaphor.application import Application
from gaphor.diagram.connectors import IConnect
from gaphor.diagram.grouping import Group

# For DiagramItemConnector aspect:
import gaphor.ui.diagramtools

log = logging.getLogger("Gaphor")
log.setLevel(logging.WARNING)


class TestCase(unittest.TestCase):

    services = ["event_manager", "component_registry", "element_factory", "sanitizer"]

    def setUp(self):
        Application.init(services=self.services)
        self.element_factory = Application.get_service("element_factory")
        assert len(list(self.element_factory.select())) == 0, list(
            self.element_factory.select()
        )
        self.diagram = self.element_factory.create(UML.Diagram)
        assert len(list(self.element_factory.select())) == 1, list(
            self.element_factory.select()
        )

    def tearDown(self):
        self.element_factory.shutdown()
        Application.shutdown()

    def get_service(self, name):
        return Application.get_service(name)

    def create(self, item_cls, subject_cls=None, subject=None):
        """
        Create an item with specified subject.
        """
        if subject_cls is not None:
            subject = self.element_factory.create(subject_cls)
        item = self.diagram.create(item_cls, subject=subject)
        self.diagram.canvas.update()
        return item

    def allow(self, line, handle, item, port=None):
        """
        Glue line's handle to an item.

        If port is not provided, then first port is used.
        """
        if port is None and len(item.ports()) > 0:
            port = item.ports()[0]

        adapter = IConnect(item, line)
        return adapter.allow(handle, port)

    def connect(self, line, handle, item, port=None):
        """
        Connect line's handle to an item.

        If port is not provided, then first port is used.
        """
        canvas = line.canvas
        assert line.canvas is item.canvas

        if port is None and len(item.ports()) > 0:
            port = item.ports()[0]

        sink = ConnectionSink(item, port)
        connector = Connector(line, handle)

        connector.connect(sink)

        cinfo = canvas.get_connection(handle)
        assert cinfo.connected is item
        assert cinfo.port is port

    def disconnect(self, line, handle):
        """
        Disconnect line's handle.
        """
        canvas = self.diagram.canvas
        # disconnection on adapter level is performed due to callback, so
        # no adapter look up here
        canvas.disconnect_item(line, handle)
        assert not canvas.get_connection(handle)

    def get_connected(self, handle):
        """
        Get item connected to line via handle.
        """
        cinfo = self.diagram.canvas.get_connection(handle)
        if cinfo:
            return cinfo.connected
        return None

    def get_connection(self, handle):
        """
        Get connection information.
        """
        return self.diagram.canvas.get_connection(handle)

    def can_group(self, parent, item):
        """
        Check if an item can be grouped by parent.
        """
        adapter = Group(parent, item)
        return adapter.can_contain()

    def group(self, parent, item):
        """
        Group item within a parent.
        """
        self.diagram.canvas.reparent(item, parent)
        adapter = Group(parent, item)
        adapter.group()

    def ungroup(self, parent, item):
        """
        Remove item from a parent.
        """
        adapter = Group(parent, item)
        adapter.ungroup()
        self.diagram.canvas.reparent(item, None)

    def kindof(self, cls):
        """
        Find UML metaclass instances using element factory.
        """
        return self.element_factory.lselect(lambda e: e.isKindOf(cls))

    def save(self):
        """
        Save diagram into string.
        """
        from gaphor.storage import storage
        from gaphor.misc.xmlwriter import XMLWriter

        f = StringIO()
        storage.save(XMLWriter(f), factory=self.element_factory)
        data = f.getvalue()
        f.close()

        self.element_factory.flush()
        assert not list(self.element_factory.select())
        assert not list(self.element_factory.lselect())
        return data

    def load(self, data):
        """
        Load data from specified string. Update ``TestCase.diagram``
        attribute to hold new loaded diagram.
        """
        from gaphor.storage import storage

        f = StringIO(data)
        storage.load(f, factory=self.element_factory)
        f.close()

        self.diagram = self.element_factory.lselect(lambda e: e.isKindOf(UML.Diagram))[
            0
        ]
