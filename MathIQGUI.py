from tkinter import filedialog
from tkinter import *


class UserInterface(Frame):

    def __init__(self, master):
        super(UserInterface, self).__init__(master)
        self.grid()
        self.textBox = Text(self, width=50, height=5, wrap=WORD)
        self.textBox.grid(row=0, column=0, columnspan=3, sticky=W)
        self.selectFileButton = Button(self, text="Select File")
        self.selectFileButton["command"] = self.findFile
        self.selectFileButton.grid(row=1, column=0, sticky=W)

    def findFile(self):
        self.file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.textBox.insert(0.0, self.file)





