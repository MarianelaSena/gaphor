""" Event management system.

This module provides API for event management. There are two APIs provided:

* Global event management API: subscribe, unsubscribe, handle.
* Local event management API: Manager

If you run only one instance of your application per Python
interpreter you can stick with global API, but if you want to have
more than one application instances running inside one interpreter and
to have different configurations for them -- you should use local API
and have one instance of Manager object per application instance.
"""

from collections import namedtuple

from gaphor.misc.generic.registry import Registry, TypeAxis


__all__ = "Manager"


class Manager:
    """ Event manager

    Provides API for subscribing for and firing events. There's also global
    event manager instantiated at module level with functions
    :func:`.subscribe`, :func:`.handle` and decorator :func:`.subscriber` aliased
    to corresponding methods of class.
    """

    def __init__(self):
        axes = (("event_type", TypeAxis()),)
        self.registry = Registry(*axes)

    def subscribe(self, handler, event_type):
        """ Subscribe ``handler`` to specified ``event_type``"""
        handler_set = self.registry.get_registration(event_type)
        if handler_set is None:
            handler_set = self._register_handler_set(event_type)
        handler_set.add(handler)

    def unsubscribe(self, handler, event_type):
        """ Unsubscribe ``handler`` from ``event_type``"""
        handler_set = self.registry.get_registration(event_type)
        if handler_set and handler in handler_set:
            handler_set.remove(handler)

    def handle(self, event):
        """ Fire ``event``

        All subscribers will be executed with no determined order.
        """
        handler_sets = self.registry.query(event)
        for handler_set in handler_sets:
            for handler in set(handler_set):
                handler(event)

    def _register_handler_set(self, event_type):
        """ Register new handler set for ``event_type``.
        """
        handler_set = set()
        self.registry.register(handler_set, event_type)
        return handler_set

    def subscriber(self, event_type):
        """ Decorator for subscribing handlers

        Works like this:

            >>> mymanager = Manager()
            >>> class MyEvent():
            ...     pass
            >>> @mymanager.subscriber(MyEvent)
            ... def mysubscriber(evt):
            ...     # handle event
            ...     return

            >>> mymanager.handle(MyEvent())

        """

        def registrator(func):
            self.subscribe(func, event_type)
            return func

        return registrator
