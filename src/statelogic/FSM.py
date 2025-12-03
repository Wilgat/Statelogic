from __future__ import print_function

import os
from .Attr import Attr  
from .Transition import Transition 
from .Reflection import Reflection 

class FSM(Reflection):

    CLASSNAME = "FSM"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 1

    @staticmethod
    def class_version():
        return f"{FSM.CLASSNAME} v{FSM.MAJOR_VERSION}.{FSM.MINOR_VERSION}.{FSM.PATCH_VERSION}"

    def __name_convert__(self, input_string):
        split_parts = input_string.split('_')
        converted_parts = [part.capitalize() for part in split_parts]
        converted_string = ''.join(converted_parts)
        return converted_string

    def fire(self, transition_name):
        fromClass = self.fromClass if hasattr(self, 'fromClass') else self
        
        # First, try direct method call (backward compat)
        if transition_name in fromClass.methods():
            fromClass.__dict__[transition_name]()
            return fromClass
        
        # Second, search through registered transitions
        for trans in fromClass.transitions():
            if trans.name() == transition_name:
                current = fromClass.state()
                if current == trans.fromState():
                    # Simulate the transition
                    getattr(fromClass, transition_name)()  # will exist or be created dynamically
                return fromClass
                
        # If not found, maybe warn?
        if hasattr(fromClass, 'infoMsg'):
            fromClass.infoMsg(f"No transition named '{transition_name}' found from state '{fromClass.state()}'", "FSM")
        return fromClass

    def after(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        name = name.strip()
        if name in fromClass.events():
            newname="after" +name[0].upper() + name[1:]
            if newname not in fromClass.methods():
                fromClass.__dict__[newname] = foo.__get__(self)
                fromClass.methods(newname)
        return fromClass

    def fromState(self):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        return fromClass._["toState"]

    def nextState(self):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        return fromClass._["nextState"]

    def toState(self):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        return fromClass._["fromState"]

    def transitionName(self):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        return fromClass._["transitionName"]

    def on(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        name = name.strip()
        if name in fromClass.events():
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
            fromClass = self.fromClass
        name = name.strip()
        if name in fromClass.events():
            newname= "before" +name[0].upper() + name[1:]
            if newname not in fromClass.methods():
                fromClass.__dict__[newname] = foo.__get__(self)
                fromClass.methods(newname)
        return fromClass

    def method(self, name, foo):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        name = name.strip()
        if name not in fromClass.methods():
            fromClass.__dict__[name] = foo.__get__(self)
            fromClass.methods(name)
        return fromClass
    
    def transition(self, name, fromState, toState):
        fromClass = self
        if hasattr(self, 'fromClass'):
            fromClass = self.fromClass
        if name not in fromClass.events() and name not in Attr.RESERVED:
            
            for t in fromClass.transitions():
                if t.fromState()==fromState and t.toState()==toState:
                    return fromClass
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
            fromClass.events(name)
            transition = Transition(name, fromState, toState)
            fromClass.transitions(transition)
            fromClass.methods(name)
        fromClass.states(fromState)
        fromClass.states(toState)
        fromClass.stateChoice(fromClass.states())
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
        Attr(fromClass, "state", readonly=True, useChoiceOnly=True)
        Attr(fromClass, "nextState", "", readonly=True)
        Attr(fromClass, attrName="methods", value = [])
        Attr(fromClass, attrName="events", value = [])
        Attr(fromClass, attrName="transitions", sorting=False, value = [])
        Attr(fromClass, attrName="states", value = [])
        fromClass.__dict__['onState'] = self.onState.__get__(fromClass)
        if not isSelf:
            fromClass.__dict__['fromClass'] = fromClass
            fromClass.__dict__['transition'] = self.transition.__get__(fromClass)
            fromClass.__dict__['after'] = self.after.__get__(fromClass)
            fromClass.__dict__['on'] = self.on.__get__(fromClass)   
            fromClass.__dict__['before'] = self.before.__get__(fromClass)
            fromClass.__dict__['method'] = self.method.__get__(fromClass)
            fromClass.__dict__['fire'] = self.fire.__get__(fromClass)
            fromClass.__dict__['stateChanged'] = self.stateChanged.__get__(fromClass)
            fromClass.__dict__['hasFunc'] = self.hasFunc.__get__(fromClass)
            fromClass.__dict__['transitionName'] = self.transitionName.__get__(fromClass)
