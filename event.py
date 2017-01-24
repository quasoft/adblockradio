#!/usr/bin/env python3


class Event(object):
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self._func_name = func.__name__
        self._key = '_myevent_' + func.__name__

    def __get__(self, obj, cls):
        try:
            return obj.__dict__[self._key]
        except KeyError:
            be = obj.__dict__[self._key] = BoundEvent()

            def fire_method(obj, *args, **kargs):
                be(obj, *args, **kargs)

            fire_method.__doc__ = "Fire method for event '%s'" % self._key
            fire_method.__name__ = self._func_name.replace("event_", "fire_", 1)
            setattr(obj, fire_method.__name__, fire_method)

            return be


class BoundEvent(object):
    def __init__(self):
        self._fns = []

    def __iadd__(self, fn):
        self._fns.append(fn)
        return self

    def __isub__(self, fn):
        self._fns.remove(fn)
        return self

    def __call__(self, *args, **kwargs):
        for f in self._fns[:]:
            f(*args, **kwargs)
