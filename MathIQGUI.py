from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import letterFinder
import main
import numpy as np

classDict = {}

class UserInterface(object):

    def __init__(self, model, classDictFromMain):
        self.root = Tk()
        self.root.title("MathIQ")
        #self.root.geometry("500x200")
        self.model = model
        global classDict
        classDict = classDictFromMain
        self.filemodel = None
        self.currentFrame = MainFrame(self.root,  self)

        self.root.mainloop()


    def loadCorrectionFrame(self):
        self.currentFrame.destroy()
        self.currentFrame = CorrectionFrame(self.root, self)

    def loadMainFrame(self):
        self.currentFrame.destroy()
        self.currentFrame=MainFrame(self.root,  self)


class MainFrame(Frame):

    def __init__(self, master, ui):
        super(MainFrame, self).__init__(master)
        self.ui = ui
        self.file = None
        self.createWigdets()

    def createWigdets(self):
        buttonwidth = 15
        buttonpadx = 2
        buttonpady = 10
        self.grid()

        #self.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=1)
        #self.columnconfigure(2, weight=1)
        #self.columnconfigure(3, weight=1)

        #self.rowconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        #self.rowconfigure(2, weight=1)

        self.textBoxFile = Label(self,
                                 text="No file Selected",
                                 justify = LEFT)
        self.textBoxFile.grid(row=0, column=0, columnspan=4, sticky=W,
                              padx=10, pady=10)
        self.textBoxExpression = Label(self,
                                       text="No expression detected")
        self.textBoxExpression.grid(row=1, column =0, columnspan =3, sticky=W,
                                    padx=10, pady=10)
        self.textBoxAnswer = Label(self, text="N/A")
        self.textBoxAnswer.grid(row=1, column=3, sticky=W,
                                padx=10, pady=10)
        self.selectFileButton = Button(self, text="Select File",
                                       width=buttonwidth)
        self.selectFileButton.grid(row=2, column=0, sticky=S,
                                   padx=buttonpadx, pady=buttonpady)
        self.correctButton = Button(self, text="Correct",
                                    width=buttonwidth)
        self.correctButton.grid(row=2, column=1, sticky=S,
                                padx=buttonpadx, pady=buttonpady)
        self.solveButton = Button(self, text="Solve",
                                  width=buttonwidth)
        self.solveButton.grid(row=2, column=2, sticky=S,
                              padx=buttonpadx, pady=buttonpady)
        self.exitButton = Button(self, text="Exit",
                                 width=buttonwidth)
        self.exitButton.grid(row=2, column=3, sticky=S,
                             padx=buttonpadx, pady=buttonpady)

        self.exitButton["command"] = self.exitAction

        self.selectFileButton["command"] = self.findFileAction

        self.correctButton["command"] = self.correctionAction

        self.solveButton["command"] = self.solveAction

        if(self.ui.filemodel):
            self.textBoxFile.configure(text = self.ui.filemodel.file)
            self.textBoxFile.text = self.ui.filemodel.file
            self.textBoxExpression.configure(text = self.ui.filemodel.expression)
            self.textBoxExpression.text = self.ui.filemodel.expression


    def exitAction(self):
        print("exit called")
        #self.destroy()
        self.master.destroy()

    def findFileAction(self):
        file = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        #file = filedialog.askopenfilename(initialdir="", title="Select file",filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.ui.filemodel = FileModel(file, self.ui.model)
        self.textBoxFile.configure(text = file)
        self.textBoxFile.text = file
        expression = self.ui.filemodel.getExpressionText()
        self.textBoxExpression.configure(text = expression)
        self.textBoxExpression = expression

    def correctionAction(self):
        if self.ui.filemodel:
            print("Entered")
            self.ui.loadCorrectionFrame()

    def solveAction(self):
        answer = self.ui.filemodel.solveExpression()
        self.textBoxAnswer.configure(text = str(answer))
        self.textBoxAnswer.text= str(answer)

class CorrectionFrame(Frame):

    def __init__(self, master, ui):
        super(CorrectionFrame, self).__init__(master)
        self.ui = ui
        self.choices = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/")
        self.index = 0
        self.expressions_text = self.ui.filemodel.getExpressionText()
        self.createWigdets()


    def createWigdets(self):
        buttonwidth = 10
        buttonpadx = 2
        buttonpady = 10
        self.grid()

        self.imageLabelText = Label(self, text="Image")
        self.imageLabelText.grid(row=0, column=0, sticky= W,
                                 padx=10, pady=10)
        self.imageLabel = Label(self, image=self.ui.filemodel.images_tkinter[self.index])
        self.imageLabel.grid(row=0, column=1, sticky=W,
                             padx=10, pady=10)
        self.dropDownText = Label(self, text="Correction")
        self.dropDownText.grid(row=1, column=0, sticky=W,
                               padx=10, pady=10)

        self.correction = StringVar(self)
        self.correction.set(self.expressions_text[self.index])
        self.correctionsMenue = OptionMenu(self, self.correction, *self.choices)
        self.correctionsMenue.grid(row=1, column=1,
                                   padx=10, pady=10, sticky=W)
        self.correction.trace("w", self.correct)

        self.previousButton = Button(self, text="Previous", width=buttonwidth)
        self.previousButton.grid(row=2, column=0,
                                 padx=10, pady=10)
        self.doneButton = Button(self, text="Done", width=buttonwidth)
        self.doneButton.grid(row=2, column=1,
                             padx=10, pady=10)
        self.nextButton = Button(self, text="Next", width=buttonwidth)
        self.nextButton.grid(row=2, column=3,
                             padx=10, pady=10)


        self.doneButton["command"] = self.doneAction
        self.previousButton["command"] = self.prevAction
        self.nextButton["command"] = self.nextAction


    def correct(self, *args):
        self.expressions_text[self.index] = self.correction.get()
        self.ui.filemodel.correctPrediction(self.index ,self.correction.get())

    def updateFrame(self):
        self.imageLabel.configure(image = self.ui.filemodel.images_tkinter[self.index])
        self.imageLabel.image = self.ui.filemodel.images_tkinter[self.index]
        self.correction.set(self.ui.filemodel.expression[self.index])

    def doneAction(self):
        #self.ui.filemodel.updateMLModel()
        self.ui.loadMainFrame()

    def prevAction(self):
        if self.index > 0:
            self.index = self.index - 1
            self.updateFrame()

    def nextAction(self):
        if self.index < len(self.ui.filemodel.expression)-1:
            self.index = self.index + 1
            self.updateFrame()



class FileModel(object):

    def __init__(self, filename, mlmodel):
        self.file = filename
        self.mlmodel = mlmodel
        self.images = letterFinder.img_to_array(self.file)
        self.images_tkinter = []
        self.convertImages()
        self.predicted = self.mlmodel.predict_on_batch(np.asarray(self.images.copy()))
        self.expression = self.getExpressionText()

    def correctPrediction(self, index, correctvalue):
        self.expression[index] = correctvalue

    def updateMLModel(self):
        """Trains the ML model, by telling it the correct values"""
        #self.mlmodel.fit(np.array(self.images.copy(), 'float64'), np.array(self.expression), epochs=5)

    def getExpressionText(self):
        expressiontext = []
        for prediction in self.predicted:
            expressiontext.append(str(self.getRealValue(np.argmax(prediction))))
            #expressiontext.append(str(np.argmax(prediction)))
        return expressiontext

    def convertImages(self):
        for i in self.images:
            img = Image.fromarray(i)
            image = ImageTk.PhotoImage(img)
            self.images_tkinter.append(image)

        temp = []
        for i in self.images:
            i = np.transpose(i, (2, 0, 1))
            temp.append(i)
        self.images = temp

    def solveExpression(self):
        problem = ""
        for char in self.expression:
            problem = problem + char
        return eval(problem)

    def getRealValue(self, index):
        for sym, i in classDict.items():
            if i == index:
                return sym







