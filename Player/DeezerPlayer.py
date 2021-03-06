import subprocess
import threading
import fcntl
import os
import time

class DezzerPlayer():
    
    def __init__(self):
        self._process = None
        self._callback = None
        self._thread = None

    def exit(self):
        self._callback = None
        self.stop()
    
    def stop(self):
        print("stopping thread now ...")
        if self._process:
            self.communicate('exit')
            #line, err = self._process.communicate('exit\n'.encode())
            #print("result from process: " + str(line))

    def pause(self):
        print("pause deezer player")
        self.communicate('pause')

    def resume(self):
        print("resume deezer player")
        self.communicate('resume')

    def communicate(self, input):
        if self._process:
            command = input + '\n'
            #line, err = self._process.communicate(command.encode())
            
            self._process.stdin.write(command.encode())
            if self._process:
                self._process.stdin.flush()

            stdout = ''
            stderr = ''
            is_stdout_failed = True
            is_stderr_failed = True
            sleep = 0.2
            error_count = 0
            while True:
                # Read from stdout
                print("read stdout")
                try:
                    stdout = self._process.stdout.read()
                    break
                except Exception:
                    pass
                time.sleep(sleep)
                if(error_count > 1):
                    break
                error_count = error_count + 1

            error_count = 0
            while True:
                # Read from stderr
                print("read stderr")
                try:
                    stderr = self._process.stderr.read()
                    break
                except Exception:
                    pass
                time.sleep(sleep)
                if(error_count > 1):
                    break
                error_count = error_count + 1

            #print("stdout from process: " + str(stdout))
            #print("stderr from process: " + str(stderr))

    def play(self, dz_track_uri, callback):
        self.exit()
        self._callback = callback
        dz_track_uri = str(dz_track_uri)
        #command = "./NanoPlayer dz_track dzmedia:///track/85509044"
        command = "./Player/NanoPlayer dz_track dzmedia:///track/" + dz_track_uri
        print(command)
        
        self.popenAndCall(command)

    def popenAndCall(self, command):
        """
        Runs the given args in a subprocess.Popen, and then calls the function
        onExit when the subprocess completes.
        onExit is a callable object, and popenArgs is a list/tuple of args that 
        would give to subprocess.Popen.
        """
        
        def runInThread(command, nothing):

            self._process = subprocess.Popen(command.split()
                ,stdin=subprocess.PIPE
                ,stdout=subprocess.PIPE
                ,stderr=subprocess.PIPE
                ,shell=False)
            
            # Fix the pipes to be nonblocking
            fcntl.fcntl(self._process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            fcntl.fcntl(self._process.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

            self._process.wait()
            
            if self._callback:
                self._callback()
                #print("callback was called. terminate process and set to null.")
            #self._process = None
            return

        thread = threading.Thread(target=runInThread, args=(command, None))
        thread.start()
        # returns immediately after the thread starts
        return thread

Player = DezzerPlayer()