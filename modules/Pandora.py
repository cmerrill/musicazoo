from musicazooTemplates import MusicazooShellCommandModule
from subprocess import Popen, PIPE
import time
import re

class Pandora(MusicazooShellCommandModule):
    resources = ("audio",)
    presistent = True
    keywords = ("pandora","pd")
    command = ("pianobar",)
    title = "Pandora"
    email = "musicazoo@mit.edu"
    password = "musicazoo"
    
    def __init__(self,json):
        self._initialize(json)
        
    def pause(self, cb):
        self.message({"command":"p"})
        cb()
    
    def unpause(self, cb):
        self.message({"comand":"p"})
        cb();

    def message(self,json):
        if self.subprocess:
            self.subprocess.stdin.write(json["command"])

    def _run(self,cb):
        command = self.command
        self.subprocess = Popen(command, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        
        # Loop continuously, getting output and setting titles
        while self.subprocess.poll() == None:
            out = self.subprocess.stdout.readline();
            match = re.search(r'[|]>\s(".*)$', out)
            if match: self.title = "Pandora: %s" % match.group(1)

        cb()
        