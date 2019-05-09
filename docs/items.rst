Gaphor Diagram Items
====================
The diagram items (or in short `items`) represent UML metamodel on a diagram.
The following sections present the basic items.

DiagramItem
-----------
Basic diagram item supporting item style, text elements and stereotypes.

.. autoclass:: gaphor.diagrams.diagramitem.DiagramItem
   :members:

ElementItem
-----------
Rectangular canvas item.

.. autoclass:: gaphor.diagrams.elementitem.ElementItem

NamedItem
---------
NamedElement (UML metamodel) representation using rectangular canvas item.

.. autoclass:: gaphor.diagrams.nameditem.NamedItem

CompartmentItem
---------------
An item with compartments (i.e. Class or State)

.. autoclass:: gaphor.diagrams.compartment.CompartmentItem

ClassifierItem
--------------
Classifer (UML metamodel) representation.

.. autoclass:: gaphor.diagrams.classifier.ClassifierItem

DiagramLine
-----------
Line canvas item.

.. autoclass:: gaphor.diagrams.diagramline.DiagramLine

NamedLine
---------
NamedElement (UML metamodel) representation using line canvas item.

.. autoclass:: gaphor.diagrams.diagramline.NamedLine

FeatureItem
-----------
Diagram representation of UML metamodel classes like property, operation,
stereotype attribute, etc.

.. autoclass:: gaphor.diagrams.compartment.FeatureItem


