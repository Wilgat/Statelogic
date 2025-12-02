from __future__ import print_function
from datetime import date, datetime
import os
import re
import time
from .Signal import Signal

class Sh(Signal):

    CLASSNAME = "Sh"
    MAJOR_VERSION = 1
    MINOR_VERSION = 2
    PATCH_VERSION = 0

    @staticmethod
    def class_version():
        return f"{Sh.CLASSNAME} v{Sh.MAJOR_VERSION}.{Sh.MINOR_VERSION}.{Sh.PATCH_VERSION}"

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


    def determine_shell(self):
        # Check if SHELL environment variable exists
        shell = os.environ.get('SHELL')
        
        # If SHELL is not set, check for known shell paths
        if shell is None:
            possible_shells = [
                '/usr/bin/fish',
                '/bin/ash',
                '/bin/bash',
                '/bin/cash',
                '/bin/dash',
                '/bin/ksh',
                '/bin/pwsh',
                '/bin/tcsh',
                '/bin/zsh',
                '/bin/sh',
                'C:\\Windows\\System32\\cmd.exe',
                'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',
                'C:\\Program Files\\Git\\usr\\bin\\bash.exe'
            ]
            for shell_path in possible_shells:
                if os.path.exists(shell_path):
                    shell = shell_path
                    break
        return shell

    def shellCmd(self, cmd=None):
        if cmd is not None:
            self.__shell_cmd__=cmd
            return self
        elif not hasattr(self,'__shell_cmd__'):
                self.__shell_cmd__=self.determine_shell()
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
