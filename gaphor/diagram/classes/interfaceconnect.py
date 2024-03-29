"""
Interface item related connections.

The connectors implemented in this module check if connection is possible
to folded interface, see `gaphor.diagram.classes.interface` documentation
for details.
"""

from gaphor import UML

from gaphor.diagram.connectors import IConnect
from gaphor.diagram.classes.classconnect import DependencyConnect, ImplementationConnect
from gaphor.diagram.classes.interface import InterfaceItem, Folded
from gaphor.diagram.classes.implementation import ImplementationItem
from gaphor.diagram.classes.dependency import DependencyItem


@IConnect.register(InterfaceItem, ImplementationItem)
class ImplementationInterfaceConnect(ImplementationConnect):
    """Connect interface item and a behaviored classifier using an
    implementation.
    """

    def connect(self, handle, port):
        """
        Implementation item can be changed to draw in solid mode, when
        connected to folded interface.
        """
        super().connect(handle, port)
        if handle is self.line.head:
            self.line.request_update()

    def disconnect(self, handle):
        """
        If implementation item is no longer connected to an interface, then
        draw it in non-solid mode.
        """
        super().disconnect(handle)
        if handle is self.line.head:
            self.line.request_update()


@IConnect.register(InterfaceItem, DependencyItem)
class DependencyInterfaceConnect(DependencyConnect):
    """Connect interface item with dependency item."""

    def connect(self, handle, port):
        """
        Dependency item is changed to draw in solid mode, when connected to
        folded interface.
        """
        super().connect(handle, port)
        line = self.line
        # connecting to the interface, which is supplier - assuming usage
        # dependency
        if handle is line.head:
            if self.element.folded != Folded.NONE:
                self.element.folded = Folded.REQUIRED
            # change interface angle even when it is unfolded, this way
            # required interface will be rotated properly when folded by
            # user
            self.element.angle = port.angle
            self.line.request_update()

    def disconnect(self, handle):
        """
        If dependency item is no longer connected to an interface, then
        draw it in non-solid mode. Interface's folded mode changes to
        provided (ball) notation.
        """
        super().disconnect(handle)
        if handle is self.line.head:
            iface = self.element
            # don't change folding notation when interface is unfolded, see
            # test_unfolded_interface_disconnection as well
            if iface.folded:
                iface.folded = Folded.PROVIDED
            self.line.request_update()
