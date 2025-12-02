from __future__ import print_function
from .Attr import Attr  # if you split it out, otherwise remove this line

class Transition(object):

    CLASSNAME = "Transition"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 0

    @staticmethod
    def class_version():
        return f"{Transition.CLASSNAME} v{Transition.MAJOR_VERSION}.{Transition.MINOR_VERSION}.{Transition.PATCH_VERSION}"

    def __init__(self, name, fromState, toState):
        Attr(self, attrName="name", value = name, readonly=True)
        Attr(self, attrName="fromState", value = fromState, readonly=True)
        Attr(self, attrName="toState", value = toState, readonly=True)