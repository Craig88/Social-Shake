
# Playing about with a possible GUI for Social Shakespeare
# Craig Steele (cr@igsteele.com)
# September 2013


import Tkinter, tkFileDialog

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid();

        button = Tkinter.Button(self,text=u"Make it so!")
        button.grid(column=1,row=0) 

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Social Shakespeare App')
    

    filename = tkFileDialog.askopenfilename()
    print filename


