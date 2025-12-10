from __future__ import print_function, division, absolute_import  # NEW: Enhanced for Py2 compat
try: 
    __file__
except NameError: 
    __file__ = ''

import re
from .Attr import Attr  
from .FSM import FSM 

class AppData(FSM):

    CLASSNAME = "AppData"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 3

    @staticmethod
    def class_version():
        # NEW: Replace f-string with .format() for Py2 compat
        return "{classname} v{ver.major}.{ver.minor}.{ver.patch}".format(classname=AppData.CLASSNAME, ver=AppData)

    def __init__(self, fromClass=None, this=None):
        if fromClass is None:
            fromClass=self
        try:
            super().__init__(fromClass=fromClass)
        except:
            super(AppData, self).__init__(fromClass=fromClass)
        self.__ini_appdata__(fromClass, this)

    def __ini_appdata__(self, fromClass, this):
        self.fromClass = fromClass
        if not hasattr(fromClass, "__appdata_inited__"):
            fromClass.__appdata_inited__ = True
            Attr(fromClass, "author")
            Attr(fromClass, "appName")
            Attr(fromClass, "downloadUrl")
            Attr(fromClass, "homepage")
            Attr(fromClass, "lastUpdate")
            Attr(fromClass, "majorVersion", 0)
            Attr(fromClass, "minorVersion", 0)
            Attr(fromClass, "patchVersion", 0)
            Attr(fromClass, "thisFile", "<stdin>")
            if fromClass.hasFunc('this'):
                if this is None:
                    fromClass.this(__file__)
                else:
                    fromClass.this(this)

    def downloadHost(self):
        fromClass = self.fromClass
        if fromClass.downloadUrl() == '':
            return ''
        x = re.search("https:..([^/]+)", fromClass.downloadUrl())
        if x:
            return x.group(1)
        else:
            ''

    def fromPipe(self):
        fromClass = self.fromClass
        if not hasattr(fromClass,"__fromPipe__"):
            if hasattr(fromClass,"thisFile") and callable(fromClass.thisFile):
                fromClass.__fromPipe__ = fromClass.thisFile() == '<stdin>'
            else:
                fromClass.__fromPipe__ = False
        return fromClass.__fromPipe__ 

    def this(self, this = None):
        fromClass = self.fromClass
        reg = re.compile(r"/\./")
        if this is None:
            if not hasattr(fromClass, '__this__'):
                # NEW: appPath() undefined; stub as '' for compat (fix if method exists elsewhere)
                fromClass.__this__=reg.sub("/", fromClass.appPath() if fromClass.hasFunc('appPath') else '')
                fromClass.thisFile(this)
            return fromClass.__this__
        else:
            if isinstance(this,basestring):
                this = reg.sub("/",this)
                fromClass.__this__ = this
                if this != '<stdin>' and  this != 'built-in':
                    fromClass.thisFile(this)
            else:
                fromClass.__this__ = ''
            return self

    def version(self):
        fromClass = self.fromClass
        return "%s.%s.%s" % (fromClass.majorVersion(),fromClass.minorVersion(),fromClass.patchVersion())