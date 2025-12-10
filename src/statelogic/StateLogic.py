from __future__ import print_function, division, absolute_import  # NEW: Enhanced for Py2 compat

from .Attr import Attr  
from .Sh import Sh 
from .AppData import AppData

class StateLogic(AppData, Sh):

    CLASSNAME = "StateLogic"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 2

    BOLD='\033[1m'
    DARK_AMBER='\033[33m'
    DARK_BLUE='\033[34m'
    DARK_TURQUOISE='\033[36m'
    END='\033[0m'
    FLASHING='\033[5m'
    ITALICS='\033[3m'
    LIGHT_RED='\033[91m'
    LIGHT_AMBER='\033[93m'
    LIGHT_BLUE='\033[94m'
    LIGHT_GREEN='\033[92m'
    LIGHT_TURQUOISE='\033[96m'

    @staticmethod
    def class_version():
        # NEW: Replace f-string with .format() for Py2 compat
        return "{classname} v{ver.major}.{ver.minor}.{ver.patch}".format(classname=StateLogic.CLASSNAME, ver=StateLogic)

    def __init__(self, fromClass=None, this=None):
        isSelf = False
        if fromClass is None:
            isSelf = True
            fromClass = self
        try:
            super().__init__(fromClass=fromClass, this=this)
        except:
            super(StateLogic, self).__init__(fromClass=fromClass,this=this)
        self.__init_signal__()
        self.__init__msgbase__(fromClass)
        if not isSelf:
            fromClass.__dict__['infoMsg'] = self.infoMsg.__get__(fromClass)
            fromClass.__dict__['criticalMsg'] = self.criticalMsg.__get__(fromClass)
            fromClass.__dict__['safeMsg'] = self.safeMsg.__get__(fromClass)
            fromClass.__dict__['__timeMsg__'] = self.__timeMsg__.__get__(fromClass)
            fromClass.__dict__['__header__'] = self.__header__.__get__(fromClass)
            fromClass.__dict__['__coloredMsg__'] = self.__coloredMsg__.__get__(fromClass)
            fromClass.__dict__['__tagMsg__'] = self.__tagMsg__.__get__(fromClass)
            fromClass.__dict__['__formattedMsg__'] = self.__formattedMsg__.__get__(fromClass)
            fromClass.__dict__['prn'] = self.prn.__get__(fromClass)
            fromClass.__dict__['now'] = self.now.__get__(fromClass)
            fromClass.__dict__['version'] = self.version.__get__(fromClass)
        self.fromClass=fromClass

    def __init__msgbase__(self, fromClass):
        if not hasattr(fromClass, "__msgbase_inited__"):
            fromClass.__msgbase_inited__ = True
            Attr(fromClass,"__colorMsgColor__", "")
            Attr(fromClass,"__colorMsgTerm__","")
            Attr(fromClass,"__headerColor__","")
            Attr(fromClass,"__headerTerm__","")
            Attr(fromClass,"__message__","")
            Attr(fromClass,"__tag__","")
            Attr(fromClass,"__tagColor__","")
            Attr(fromClass,"__tagOutterColor__","")
            Attr(fromClass,"__tagTerm__","")
            Attr(fromClass,"__timeColor__","")
            Attr(fromClass,"__timeTerm__","")
            Attr(fromClass,"useColor", not self.isGitBash())
            fromClass.useColor()

    def __coloredMsg__(self,color=None):
        fromClass = self.fromClass
        if color is None :
            if fromClass.__message__() == '':
                return ''
            else:
                return "%s%s%s" % (fromClass.__colorMsgColor__(),\
                    fromClass.__message__(),fromClass.__colorMsgTerm__())
        else:
            if color == '' or not fromClass.useColor():
                fromClass.__colorMsgColor__('')
                fromClass.__colorMsgTerm__('')
            else:
                fromClass.__colorMsgColor__(color)
                fromClass.__colorMsgTerm__(StateLogic.END)
            return self

    def __formattedMsg__(self):
        fromClass = self.fromClass
        return "%s %s %s\n  %s" % (fromClass.__timeMsg__(),fromClass.__header__(),\
            fromClass.__tagMsg__(),fromClass.__coloredMsg__())

    def __header__(self,color=None):
        fromClass = self.fromClass
        if color is None:
            if fromClass.appName() == 'None':
                return fromClass.__headerTerm__()
            else:
                return "%s%s(v%s) %s" % (fromClass.__headerColor__(),\
                    fromClass.appName(),fromClass.version(),\
                    fromClass.__headerTerm__())
        else:
            if color == '' or not fromClass.useColor():
                fromClass.__headerColor__('')\
                    .__headerTerm__('')
            else:
                fromClass.__headerColor__(color)\
                    .__headerTerm__(StateLogic.END)
        return self

    def __tagMsg__(self,color=None,outterColor=None):
        fromClass = self.fromClass
        if color is None:
            if fromClass.__tag__() == '' or not fromClass.useColor():
                return '[%s]: ' % fromClass.__tag__()
            else:
                return "%s[%s%s%s%s%s]:%s " % (fromClass.__tagOutterColor__(),\
                    fromClass.__tagTerm__(),fromClass.__tagColor__(),\
                    fromClass.__tag__(),fromClass.__tagTerm__(),\
                    fromClass.__tagOutterColor__(),fromClass.__tagTerm__())
        else:
            if color == '':
                fromClass.__tagColor__('')\
                    .__tagOutterColor__('')\
                    .__tagTerm__('')
            else:
                fromClass.__tagColor__(color)\
                    .__tagOutterColor__(outterColor)\
                    .__tagTerm__(StateLogic.END)
            return self

    def __timeMsg__(self, color=None):
        fromClass = self.fromClass
        if color is None:
            return "%s%s%s" % (fromClass.__timeColor__(),fromClass.now(),\
                fromClass.__timeTerm__())
        else:
            if color == '' or not fromClass.useColor():
                fromClass.__timeColor__('')\
                    .__timeTerm__('')
            else:
                fromClass.__timeColor__(color)\
                    .__timeTerm__(StateLogic.END)
            return self

    def criticalMsg(self,msg,tag=''):
        fromClass = self.fromClass
        if fromClass.useColor():
            fromClass.__tag__(tag).__message__(msg) \
                .__timeMsg__(StateLogic.BOLD + StateLogic.ITALICS + \
                StateLogic.DARK_AMBER) \
                .__header__(StateLogic.BOLD + StateLogic.DARK_AMBER) \
                .__coloredMsg__(StateLogic.ITALICS + StateLogic.LIGHT_AMBER) \
                .__tagMsg__(StateLogic.FLASHING + StateLogic.LIGHT_RED,\
                StateLogic.LIGHT_AMBER)
        else:
            fromClass.__tag__(tag).__message__(msg) \
                .__timeMsg__('') \
                .__header__(StateLogic.BOLD + StateLogic.DARK_AMBER) \
                .__coloredMsg__('') \
                .__tagMsg__('')
        fromClass.prn("%s" % (fromClass.__formattedMsg__()))
        return self

    def infoMsg(self,msg,tag=''):
        fromClass = self.fromClass
        if fromClass.useColor():
            fromClass.__tag__(tag).__message__(msg) \
                .__timeMsg__(StateLogic.BOLD+StateLogic.ITALICS+StateLogic.DARK_BLUE) \
                .__header__(StateLogic.BOLD+StateLogic.DARK_BLUE) \
                .__coloredMsg__(StateLogic.ITALICS + StateLogic.LIGHT_BLUE) \
                .__tagMsg__(StateLogic.LIGHT_AMBER,StateLogic.LIGHT_BLUE)
        else:
            fromClass.__tag__(tag).__message__(msg) \
                .__timeMsg__('') \
                .__header__('') \
                .__coloredMsg__('') \
                .__tagMsg__('')
        fromClass.prn("%s" % (fromClass.__formattedMsg__()))
        return self

    def safeMsg(self,msg,tag=''):
        fromClass = self.fromClass
        if fromClass.useColor():
            fromClass.__tag__(tag).__message__(msg).__timeMsg__(StateLogic.BOLD + StateLogic.ITALICS + \
                StateLogic.DARK_TURQUOISE) \
                .__header__(StateLogic.BOLD + StateLogic.DARK_TURQUOISE) \
                .__coloredMsg__(StateLogic.ITALICS + StateLogic.LIGHT_TURQUOISE) \
                .__tagMsg__(StateLogic.LIGHT_GREEN,StateLogic.LIGHT_TURQUOISE)
        else:
            fromClass.__tag__(tag).__message__(msg).__timeMsg__('') \
                .__header__('') \
                .__coloredMsg__('') \
                .__tagMsg__('')
        fromClass.prn("%s" % (fromClass.__formattedMsg__()))
        return self