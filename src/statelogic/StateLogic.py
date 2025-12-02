from __future__ import print_function

from .Attr import Attr  
from .Sh import Sh 
from .AppData import AppData

class StateLogic(AppData, Sh):

    CLASSNAME = "StateLogic"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 0

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
        return f"{StateLogic.CLASSNAME} v{StateLogic.MAJOR_VERSION}.{StateLogic.MINOR_VERSION}.{StateLogic.PATCH_VERSION}"

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

    def __coloredMsg__(self,color=None):
        if color is None :
            if self.__message__() == '':
                return ''
            else:
                return "%s%s%s" % (self.__colorMsgColor__(),\
                    self.__message__(),self.__colorMsgTerm__())
        else:
            if color == '' or not self.useColor():
                self.__colorMsgColor__('')
                self.__colorMsgTerm__('')
            else:
                self.__colorMsgColor__(color)
                self.__colorMsgTerm__(StateLogic.END)
            return self

    def __formattedMsg__(self):
        return "%s %s %s\n  %s" % (self.__timeMsg__(),self.__header__(),\
            self.__tagMsg__(),self.__coloredMsg__())

    def __header__(self,color=None):
        if color is None:
            if self.appName() == 'None':
                return self.__headerTerm__()
            else:
                return "%s%s(v%s) %s" % (self.__headerColor__(),\
                    self.appName(),self.version(),\
                    self.__headerTerm__())
        else:
            if color == '' or not self.useColor():
                self.__headerColor__('')\
                    .__headerTerm__('')
            else:
                self.__headerColor__(color)\
                    .__headerTerm__(StateLogic.END)
        return self

    def __tagMsg__(self,color=None,outterColor=None):
        if color is None:
            if self.__tag__() == '' or not self.useColor():
                return '[%s]: ' % self.__tag__()
            else:
                return "%s[%s%s%s%s%s]:%s " % (self.__tagOutterColor__(),\
                    self.__tagTerm__(),self.__tagColor__(),\
                    self.__tag__(),self.__tagTerm__(),\
                    self.__tagOutterColor__(),self.__tagTerm__())
        else:
            if color == '':
                self.__tagColor__('')\
                    .__tagOutterColor__('')\
                    .__tagTerm__('')
            else:
                self.__tagColor__(color)\
                    .__tagOutterColor__(outterColor)\
                    .__tagTerm__(StateLogic.END)
            return self

    def __timeMsg__(self, color=None):
        if color is None:
            return "%s%s%s" % (self.__timeColor__(),self.now(),\
                self.__timeTerm__())
        else:
            if color == '' or not self.useColor():
                self.__timeColor__('')\
                    .__timeTerm__('')
            else:
                self.__timeColor__(color)\
                    .__timeTerm__(StateLogic.END)
            return self

    def criticalMsg(self,msg,tag=''):
        if self.useColor():
            self.__tag__(tag).__message__(msg) \
                .__timeMsg__(StateLogic.BOLD + StateLogic.ITALICS + \
                StateLogic.DARK_AMBER) \
                .__header__(StateLogic.BOLD + StateLogic.DARK_AMBER) \
                .__coloredMsg__(StateLogic.ITALICS + StateLogic.LIGHT_AMBER) \
                .__tagMsg__(StateLogic.FLASHING + StateLogic.LIGHT_RED,\
                StateLogic.LIGHT_AMBER)
        else:
            self.__tag__(tag).__message__(msg) \
                .__timeMsg__('') \
                .__header__(StateLogic.BOLD + StateLogic.DARK_AMBER) \
                .__coloredMsg__('') \
                .__tagMsg__('')
        self.prn("%s" % (self.__formattedMsg__()))
        return self

    def infoMsg(self,msg,tag=''):
        if self.useColor():
            self.__tag__(tag).__message__(msg) \
                .__timeMsg__(StateLogic.BOLD+StateLogic.ITALICS+StateLogic.DARK_BLUE) \
                .__header__(StateLogic.BOLD+StateLogic.DARK_BLUE) \
                .__coloredMsg__(StateLogic.ITALICS + StateLogic.LIGHT_BLUE) \
                .__tagMsg__(StateLogic.LIGHT_AMBER,StateLogic.LIGHT_BLUE)
        else:
            self.__tag__(tag).__message__(msg) \
                .__timeMsg__('') \
                .__header__('') \
                .__coloredMsg__('') \
                .__tagMsg__('')
        self.prn("%s" % (self.__formattedMsg__()))
        return self

    def safeMsg(self,msg,tag=''):
        if self.useColor():
            self.__tag__(tag).__message__(msg).__timeMsg__(StateLogic.BOLD + StateLogic.ITALICS + \
                StateLogic.DARK_TURQUOISE) \
                .__header__(StateLogic.BOLD + StateLogic.DARK_TURQUOISE) \
                .__coloredMsg__(StateLogic.ITALICS + StateLogic.LIGHT_TURQUOISE) \
                .__tagMsg__(StateLogic.LIGHT_GREEN,StateLogic.LIGHT_TURQUOISE)
        else:
            self.__tag__(tag).__message__(msg).__timeMsg__('') \
                .__header__('') \
                .__coloredMsg__('') \
                .__tagMsg__('')
        self.prn("%s" % (self.__formattedMsg__()))
        return self
