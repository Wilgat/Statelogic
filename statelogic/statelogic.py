from __future__ import print_function
try:
    input
except NameError:
    input = raw_input
try:
    basestring
except NameError:
    basestring=str
try: 
    __file__
except NameError: 
    __file__ = ''
try:
    import pwd
except:
    pwd = None
from datetime import date, datetime
import os
import re
import signal
import time

class Attr(object):
    RESERVED = ['False', 'def', 'if', 'raise', 'None', 'del', 'import', 
        'return', 'True', 'elif', 'in', 'try', 'and', 'else', 'is', 'while', 
        'as', 'except', 'lambda', 'with', 'assert', 'finally', 'nonlocal', 
        'yield', 'break', 'for', 'not', 'class', 'form', 'or', 'continue',
        'global', 'pass', 'attrList', 'hasattr']

    def lists(self,x=None):
        if x is None:
            if self._["sorting"]:
                return sorted(self._["list"])
            else:
                return self._["list"]
        elif self._["list"] is None:
            return None
        elif x not in self._["list"] and not self._["readonly"]:
            if isinstance(x,list):
                for l in x:
                    if isinstance(l,basestring) and self._["autostrip"]:
                        l=l.strip()
                    self._["list"].append(l)
            else:
                if isinstance(x,basestring) and self._["autostrip"]:
                    x=x.strip()
                if x not in self._["list"]:
                    self._["list"].append(x)
        return self._["class"]

    def value(self,x=None):
        if x is None:
            return self._["value"]
        elif self._["value"] is None:
            return None
        elif isinstance(x,list):
            return self._["class"]
        if not self._["readonly"] or self._["value"] is None or self._["value"]=="":
            if isinstance(x,basestring) and self._["autostrip"]:
                x=x.strip()
            if self._["value"] is None or self._["value"]!=x:
                self._["value"]=x
                if self._["onChange"] is not None:
                    self._["onChange"]()
        return self._["class"]

    def __init__(self,fromClass=None,attrName='',value=None, readonly=False, autostrip=True, sorting=True, onChange=None):
        if isinstance(attrName, basestring):
            attrName=attrName.strip()
            if attrName=="" or attrName in Attr.RESERVED:
                return None
            if fromClass is None:
                fromClass=self
            if not hasattr(fromClass,"_"):
                fromClass._={'attrList': [] }
                if not hasattr(fromClass, "attrList"):
                    def attrList(self):
                        return sorted(self._['attrList'])
                    fromClass.__dict__['attrList'] = attrList.__get__(fromClass)
            if not hasattr(fromClass._, attrName):
                fromClass._['attrList'].append( attrName )
            if isinstance(value, list):
                self._ ={"class":fromClass,"name":attrName, "value":None,"list":value, "readonly":readonly, "autostrip": autostrip, "sorting": sorting, "onChange": onChange}
            else:
                if isinstance(value,basestring) and autostrip:
                    value = value.strip()
                self._ ={"class":fromClass,"name":attrName, "value":value, "list":None, "readonly":readonly, "autostrip": autostrip, "sorting": False, "onChange": onChange}
            fromClass._[attrName]=self
            if not hasattr(fromClass,attrName):
                if isinstance(value, list):
                    def lists(self, value=None):
                        return fromClass._[attrName].lists(value)
                    fromClass.__dict__[attrName] = lists.__get__(fromClass)
                else:
                    def attr(self, value=None):
                        return fromClass._[attrName].value(value)
                    fromClass.__dict__[attrName] = attr.__get__(fromClass)

class Transition(object):
    def __init__(self, name, fromState, toState):
        Attr(self, attrName="name", value = name, readonly=True)
        Attr(self, attrName="fromState", value = fromState, readonly=True)
        Attr(self, attrName="toState", value = toState, readonly=True)

class Reflection(object):
    def hasFunc(self, func):
        if hasattr(self, 'fromClass'):
            return hasattr(self.fromClass, func) and callable(getattr(self.fromClass, func))
        else:
            return hasattr(self, func) and callable(getattr(self, func))

    def func(self, func):
        if hasattr(self, 'fromClass'):
            self.fromClass.__dict__[func]()
        else:
            self.__dict__[func]()

class FSM(Reflection):

    def __name_convert__(self, input_string):
        split_parts = input_string.split('_')
        converted_parts = [part.capitalize() for part in split_parts]
        converted_string = ''.join(converted_parts)
        return converted_string

    def after(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self
        name = name.strip()
        if name in fromClass.transitions():
            newname="after" +name[0].upper() + name[1:]
            if newname not in fromClass.methods():
                fromClass.__dict__[newname] = foo.__get__(self)
                fromClass.methods(newname)
        return fromClass

    def on(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self
        name = name.strip()
        if name in fromClass.transitions():
            newname= "on" +name[0].upper() + name[1:]
            if newname not in fromClass.methods():
                fromClass.__dict__[newname] = foo.__get__(self)
                fromClass.methods(newname)
        elif name in fromClass.states():
            newname= "on" + name.upper()
            newname2= "on" + self.__name_convert__(name.upper())
            if newname not in fromClass.methods():
                if newname in fromClass.__dict__:
                    fromClass.methods(newname)
                else:
                    fromClass.__dict__[newname] = foo.__get__(self)
                    fromClass.methods(newname)
            elif newname2 not in fromClass.methods():
                if newname2 in fromClass.__dict__:
                    fromClass.methods(newname2)
                else:
                    fromClass.__dict__[newname2] = foo.__get__(self)
                    fromClass.methods(newname2)
        return fromClass

    def stateChanged(self, func=""):
        if ('STATE' in os.environ and os.environ['STATE'].lower() == 'show') \
            or ('state' in os.environ and os.environ['state'].lower() == 'show') \
            or (self.hasFunc('logTo') and self.logTo()!=''):
            if func!="":
                func = " in %s" % func
            name = self._["transitionName"]
            fromState = self._["fromState"]
            toState = self._["toState"]
            if self.hasFunc('infoMsg'):
                self.infoMsg("Transition (%s%s) : [%s] -> [%s]" % ( name, func, fromState, toState), "STATE CHANGED")
        return self

    def before(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self
        name = name.strip()
        if name in fromClass.transitions():
            newname= "before" +name[0].upper() + name[1:]
            if newname not in fromClass.methods():
                fromClass.__dict__[newname] = foo.__get__(self)
                fromClass.methods(newname)
        return fromClass

    def method(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self
        name = name.strip()
        if name not in fromClass.methods():
            fromClass.__dict__[name] = foo.__get__(self)
            fromClass.methods(name)
        return fromClass
    
    def transition(self, name, fromState, toState):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self
        if name not in fromClass.transitions():
            def t(self):
                if fromClass.state() == fromState:
                    before= "before" +name[0].upper() + name[1:]
                    next = True
                    fromClass._["transitionName"]=name
                    fromClass._["fromState"]=fromState
                    fromClass._["toState"]=toState
                    fromClass._["nextState"]=""
                    if before in fromClass.methods():
                        next = fromClass.__dict__[before]()
                    if next:
                        fromClass._["nextState"]=toState
                        on= "on" +name[0].upper() + name[1:]
                        if on in fromClass.methods():
                            fromClass.__dict__[on]()
                        fromClass.stateChanged()
                        fromClass._["state"]._["value"] = toState
                        fromClass._["nextState"]=""
                        after= "after" +name[0].upper() + name[1:]
                        if after in fromClass.methods():
                            fromClass.__dict__[after]()
                        self.onState(toState)
                    fromClass._["transitionName"]=""
                    fromClass._["fromState"]=""
                    fromClass._["toState"]=""
                    fromClass._["nextState"]=""
                return fromClass
            fromClass.__dict__[name] = t.__get__(self)
            fromClass.transitions(name)
            fromClass.methods(name)
        fromClass.states(fromState)
        fromClass.states(toState)
        return fromClass

    def onState(self, state=None):
        if state is None:
            state = self.state()
        newname= "on" + state.upper()
        if newname in self.fromClass.methods():
            self.fromClass.__dict__[newname]()

    def __init__(self, fromClass=None):
        isSelf = False
        if fromClass is None:
            isSelf = True
            fromClass = self
        self.fromClass = fromClass
        Attr(fromClass, "state", readonly=True)
        Attr(fromClass, "nextState", "", readonly=True)
        Attr(fromClass, attrName="methods", value = [])
        Attr(fromClass, attrName="transitions", value = [])
        Attr(fromClass, attrName="states", value = [])
        fromClass.__dict__['onState'] = self.onState.__get__(fromClass)
        if not isSelf:
            fromClass.__dict__['fromClass'] = fromClass
            fromClass.__dict__['transition'] = self.transition.__get__(fromClass)
            fromClass.__dict__['after'] = self.after.__get__(fromClass)
            fromClass.__dict__['on'] = self.on.__get__(fromClass)   
            fromClass.__dict__['before'] = self.before.__get__(fromClass)
            fromClass.__dict__['method'] = self.method.__get__(fromClass)

class AppData(FSM):

    def __init__(self, this=None, fromClass=None):
        if fromClass is None:
            fromClass=self
        try:
            super().__init__(fromClass=fromClass)
        except:
            super(AppData, self).__init__(fromClass=fromClass)
        self.__ini_appdata__(fromClass)
        if this is None:
            self.this(__file__)
        else:
            self.this(this)

    def __ini_appdata__(self, fromClass):
        if not hasattr(self, "__appdata_inited__"):
            self.__appdata_inited__ = True
            Attr(fromClass, "author")
            Attr(fromClass, "appName")
            Attr(fromClass, "downloadUrl")
            Attr(fromClass, "homepage")
            Attr(fromClass, "lastUpdate")
            Attr(fromClass, "majorVersion", 0)
            Attr(fromClass, "minorVersion", 0)
            Attr(fromClass, "thisFile", "<stdin>")

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
            this = reg.sub("/",this)
            self.__this__ = this
            if this != '<stdin>':
                self.thisFile(this)
            return self

    def version(self):
        return "%s.%s" % (self.majorVersion(),self.minorVersion())

class Signal(Reflection):
    def __init__(self):
        self.__init_signal__()

    def __init_signal__(self):
        if not hasattr(self, '__signal_inited__'):
            self.__signal_inited__=True
            Attr(self, 'signal', 0)
            self.errorState = FSM()
            self.errorState.transition("hasError","normal","error") \
                .transition("ignoreError","normal","errorIgnored") \
                .transition("resetNormal","errorIgnored","normal") \
                .state("normal")
            signal.signal(signal.SIGINT, self.signal_handler)

    def hasError(self):
        self.errorState.hasError()
        return self

    def ignoreError(self):
        self.errorState.ignoreError()
        return self

    def resetNormal(self):
        self.errorState.resetNormal()
        return self

    def testIgnoredResetNormal(self):
        state = self.errorState.state() 
        self.errorState.resetNormal()
        return state=="errorIgnored"

    def signal_handler(self, sig, frame):
        self.signal(sig)
        if sig == 2:
            self.prn('\nYou pressed Ctrl + c!\n')
        if sig == 3:
            self.prn('\nYou pressed Ctrl + Back Slash!')
        exit()

class Sh(Signal):

    def __init__(self):
        try:
            super().__init__()
        except:
            super(Sh, self).__init__()

    def isGitBash(self):
        if not hasattr(self, '__is_gitbash__'):
            if not hasattr(self, '__shell_cmd__'):
                self.shellCmd()
            self.__is_gitbash__ = self.__shell_cmd__.split('\\')[-1] == 'bash.exe' 
        return self.__is_gitbash__

    def now(self):
        return str(datetime.now())

    def pid(self):
        return os.getpid()

    def prn(self, val):
        if self.hasFunc('logTo') and self.logTo() != '':
            try:
                with open(self.logTo(), 'a') as f:
                    f.write(val + '\n')
            except:
                pass
        print(val)
        return self

    def shellCmd(self, cmd=None):
        if cmd is not None:
            self.__shell_cmd__=cmd
            return self
        elif not hasattr(self,'__shell_cmd__'):
            if 'SHELL' in os.environ:
                self.__shell_cmd__ = os.environ['SHELL']
                # cannot use self.pathexists to avoid recursive call
            elif os.path.exists('/usr/bin/fish'):
                self.__shell_cmd__ = '/usr/bin/fish'
            elif os.path.exists('/bin/bash'):
                self.__shell_cmd__ = '/bin/bash'
            elif os.path.exists('/bin/ash'):
                self.__shell_cmd__ = '/bin/ash'
            elif os.path.exists('/bin/zsh'):
                self.__shell_cmd__ = '/bin/zsh'
            elif os.path.exists('/bin/sh'):
                self.__shell_cmd__ = '/bin/sh'
            elif os.path.exists('C:\\Windows\\System32\\cmd.exe'):
                self.__shell_cmd__ = 'C:\\Windows\\System32\\cmd.exe'
            elif os.path.exists('C:\\Program Files\\Git\\usr\\bin\\bash.exe'):
                self.__shell_cmd__ = 'C:\\Program Files\\Git\\usr\\bin\\bash.exe'
            else:
                self.__shell_cmd__=''
        return self.__shell_cmd__

    def today(self):
        return date.today()

    def timestamp(self):
        return "%s" % (int(time.time()))

    def userID(self):
        return os.getuid()

    def username(self):
        if pwd is None:
            return os.getlogin()
        return pwd.getpwuid(self.userID())[0]

class StateLogic(AppData, Sh):
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

    def __init__(self, this=None, fromClass=None):
        if fromClass is None:
            fromClass=self
        try:
            super().__init__(this=this, fromClass=fromClass)
        except:
            super(StateLogic, self).__init__(this=this, fromClass=fromClass)
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

