import subprocess
import threading

class DezzerPlayer():
    
    def __init__(self):
        self._process = None
        self._callback = None
        self._thread = None
    
    def stop(self):
        print("stopping thread now ...")
        if self._process:
            line, err = self._process.communicate('h')
            print("result from process: " + str(line))

    def play(self, dz_track_uri, callback):
        self.stop()
        self._callback = callback
        #command = "./NanoPlayer dz_track dzmedia:///track/85509044"
        command = "./Player/NanoPlayer dz_track dzmedia:///track/" + dz_track_uri
        self.popenAndCall(self._callback, command)

    def popenAndCall(self, onExit, command):
        """
        Runs the given args in a subprocess.Popen, and then calls the function
        onExit when the subprocess completes.
        onExit is a callable object, and popenArgs is a list/tuple of args that 
        would give to subprocess.Popen.
        """
        def runInThread(onExit, command):
            self._process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None, shell=True)
            self._process.wait()
            if onExit:
                onExit()
            return

        thread = threading.Thread(target=runInThread, args=(onExit, command))
        thread.start()
        # returns immediately after the thread starts
        return thread

Player = DezzerPlayer()