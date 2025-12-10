from __future__ import print_function, division, absolute_import  # NEW: Enhanced for Py2 compat
try:
    basestring
except NameError:
    basestring=str  # Already Py2/3 compat shim

class Attr(object):

    CLASSNAME = "Attr"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 2

    @staticmethod
    def class_version():
        # NEW: Replace f-string with .format() for Py2 compat
        return "{classname} v{ver.major}.{ver.minor}.{ver.patch}".format(classname=Attr.CLASSNAME, ver=Attr)

    RESERVED = ['False', 'def', 'if', 'raise', 'None', 'del', 'import', 
        'return', 'True', 'elif', 'in', 'try', 'and', 'else', 'is', 'while', 
        'as', 'except', 'lambda', 'with', 'assert', 'finally', 'nonlocal', 
        'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue',
        'global', 'pass', 'attrList', 'hasattr']

    def lists(self,x=None):
        if x is None:
            if self._["sorting"]:
                return sorted(self._["list"])
            elif self._["list"] is None:
                return None
            else:
                return self._["list"]
        elif x not in self._["list"] and (not self._["readonly"] or self._["list"] is None):
            if self._["list"] is None:
                self._["list"]=[]
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
        elif isinstance(x,list):
            return self._["class"]
        if not self._["readonly"] or self._["value"] is None or self._["value"]=="":
            changed = False
            if isinstance(x,basestring) and self._["autostrip"]:
                x=x.strip()
            if self._["value"] is None or self._["value"]!=x:
                if self._["valueChoice"] is not None and len(self._["valueChoice"]) > 0:
                    for y in self._["valueChoice"]:
                        if x==y:
                            self._["value"]=x
                            changed = True
                            break
                elif not self._["useChoiceOnly"]:
                    self._["value"]=x
                    changed = True
                if changed and self._["onChange"] is not None:
                    self._["onChange"]()
        return self._["class"]
    
    def valueChoice(self,x=None):
        if x is None:
            return self._["valueChoice"]
        elif isinstance(x,list):
            if self._["valueChoice"] is None:
                self._["valueChoice"]=[]
            if isinstance(x,list):
                for l in x:
                    if isinstance(l,basestring):
                        l=l.strip()
                    if l not in self._["valueChoice"]:
                        self._["valueChoice"].append(l)
        return self._["class"]

    def __init__(self,fromClass=None,attrName='',value=None, readonly=False, autostrip=True, sorting=True, onChange=None, valueChoice=None, useChoiceOnly=False):
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
                self._ ={"class":fromClass,"name":attrName, "value":None,"list":value, "readonly":readonly, "autostrip": autostrip, "sorting": sorting, "onChange": onChange, "valueChoice": None, "useChoiceOnly": useChoiceOnly }
            else:
                if isinstance(value,basestring) and autostrip:
                    value = value.strip()
                self._ ={"class":fromClass,"name":attrName, "value":value, "list":None, "readonly":readonly, "autostrip": autostrip, "sorting": False, "onChange": onChange, "valueChoice": None, "useChoiceOnly": useChoiceOnly}
            if valueChoice is not None:
                self.valueChoice(valueChoice)
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
                    def choice(self, choice=None):
                        return fromClass._[attrName].valueChoice(choice)
                    fromClass.__dict__[attrName+'Choice']=choice.__get__(fromClass)