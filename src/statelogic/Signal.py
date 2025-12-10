from __future__ import print_function, division, absolute_import  # NEW: Enhanced for Py2 compat

import signal
import sys  # NEW: For sys.exit() compat across versions
from .Attr import Attr 
from .Reflection import Reflection 
from .FSM import FSM

class Signal(Reflection):

    CLASSNAME = "Signal"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 2

    @staticmethod
    def class_version():
        # NEW: Replace f-string with .format() for Py2 compat
        return "{classname} v{ver.major}.{ver.minor}.{ver.patch}".format(classname=Signal.CLASSNAME, ver=Signal)

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
        # NEW: Use sys.exit for reliable exit in scripts (avoids REPL dependency in Py2)
        sys.exit(1)