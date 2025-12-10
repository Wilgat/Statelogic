from __future__ import print_function, division, absolute_import  # NEW: Enhanced for Py2 compat

from .Attr import Attr  # if you split it out, otherwise remove this line

class Transition(object):

    CLASSNAME = "Transition"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 3

    @staticmethod
    def class_version():
        # NEW: Replace f-string with .format() for Py2 compat
        return "{classname} v{ver.major}.{ver.minor}.{ver.patch}".format(classname=Transition.CLASSNAME, ver=Transition)

    def __init__(self, name, fromState, toState):
        Attr(self, attrName="name", value = name, readonly=True)
        Attr(self, attrName="fromState", value = fromState, readonly=True)
        Attr(self, attrName="toState", value = toState, readonly=True)