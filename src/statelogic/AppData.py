from __future__ import print_function
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
    PATCH_VERSION = 1

    @staticmethod
    def class_version():
        return f"{AppData.CLASSNAME} v{AppData.MAJOR_VERSION}.{AppData.MINOR_VERSION}.{AppData.PATCH_VERSION}"

    def __init__(self, fromClass=None, this=None):
        if fromClass is None:
            fromClass=self
        try:
            super().__init__(fromClass=fromClass)
        except:
            super(AppData, self).__init__(fromClass=fromClass)
        self.__ini_appdata__(fromClass, this)

    def __ini_appdata__(self, fromClass, this):
        if not hasattr(self, "__appdata_inited__"):
            self.__appdata_inited__ = True
            Attr(fromClass, "author")
            Attr(fromClass, "appName")
            Attr(fromClass, "downloadUrl")
            Attr(fromClass, "homepage")
            Attr(fromClass, "lastUpdate")
            Attr(fromClass, "majorVersion", 0)
            Attr(fromClass, "minorVersion", 0)
            Attr(fromClass, "patchVersion", 0)
            Attr(fromClass, "thisFile", "<stdin>")
            if this is None:
                fromClass.this(__file__)
            else:
                fromClass.this(this)

    def downloadHost(self):
        if self.downloadUrl() == '':
            return ''
        x = re.search("https:..([^/]+)", self.downloadUrl())
        if x:
            return x.group(1)
        else:
            ''

    def fromPipe(self):
        if not hasattr(self,"__fromPipe__"):
            if hasattr(self,"thisFile") and callable(self.thisFile):
                self.__fromPipe__ = self.thisFile() == '<stdin>'
            else:
                self.__fromPipe__ = False
        return self.__fromPipe__ 

    def this(self, this = None):
        reg = re.compile(r"/\./")
        if this is None:
            if not hasattr(self, '__this__'):
                self.__this__=reg.sub("/",self.appPath())
                self.thisFile(this)
            return self.__this__
        else:
            if isinstance(this,basestring):
                this = reg.sub("/",this)
                self.__this__ = this
                if this != '<stdin>' and  this != 'built-in':
                    self.thisFile(this)
            else:
                self.__this__ = ''
            return self

    def version(self):
        return "%s.%s.%s" % (self.majorVersion(),self.minorVersion(),self.patchVersion())
