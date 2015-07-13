import Tkinter, os, subprocess, threading

class cmdthread(threading.Thread):
    def __init__(self, commands):
        super(cmdthread, self).__init__()
        self.commands = commands
        self.done = False
        self.success = False
    def run(self):
        self.success = True
        for c in self.commands:
            try:
                subprocess.check_call(c, shell=True)
            except subprocess.CalledProcessError:
                self.success = False
                break
        self.done = True

class CmdWin(Tkinter.Toplevel):
    last = None
    def __init__(self, parent, commands):
        Tkinter.Toplevel.__init__(self, parent)
        if CmdWin.last:
            CmdWin.last.destroy()
        CmdWin.last = self
        self.thread = cmdthread(commands)
        self.thread.start()
        self.grid()
        self.label = Tkinter.Label(self)
        self.label.grid(row=1, column=1)
        self.label.config(text='Working')
        self.after_idle(self.update)
    def update(self):
        if self.thread.done:
            if self.thread.success:
                self.destroy()
                CmdWin.last = None
            else:
                self.label.config(text='Failed!')
        else:
            self.after(100, self.update)

class App(Tkinter.Frame):
    def __init__(self):
        Tkinter.Frame.__init__(self)
        self.grid()
        #self.title('Internet config')
        Tkinter.Button(self, text='Normal Internet', command=self.cmd_internet).grid(row=1, column=1)
        Tkinter.Button(self, text='cRIO', command=self.cmd_crio).grid(row=1, column=2)

    def cmd_internet(self):
        CmdWin(self, ['netsh int ip set address name = "Wireless" source = dhcp'])

    def cmd_crio(self):
        CmdWin(self, [
            'netsh int ip set address name = "Local Area Connection" source = static addr = 10.8.30.37 mask = 255.255.255.0',
            'netsh int ip set address name = "Wireless" source = static addr = 10.8.30.51 mask = 255.255.255.0',
        ])

if __name__ == '__main__':
    App().mainloop()
