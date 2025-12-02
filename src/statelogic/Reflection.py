from __future__ import print_function

class Reflection(object):

    CLASSNAME = "Reflection"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 0

    @staticmethod
    def class_version():
        return f"{Reflection.CLASSNAME} v{Reflection.MAJOR_VERSION}.{Reflection.MINOR_VERSION}.{Reflection.PATCH_VERSION}"

    def hasFunc(self, func):
        if hasattr(self, 'fromClass'):
            return hasattr(self.fromClass, func) and callable(getattr(self.fromClass, func))
        else:
            return hasattr(self, func) and callable(getattr(self, func))

    def func(self, func):
        if hasattr(self, 'fromClass'):
            if func in self.fromClass.__dict__:
                self.fromClass.__dict__[func]()
        else:
            if func in self.__dict:
                self.__dict__[func]()