"""
Metaclass item for Metaclass UML metaclass :) from profiles.
"""

from gaphor.diagrams.classes.klass import ClassItem
from gaphor.diagrams import uml
from gaphor import UML


@uml(UML.Component, stereotype="metaclass")
class MetaclassItem(ClassItem):
    pass
