from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import cv2
import letterFinder
import numpy as np


class UserInterface(object):

    def __init__(self, model):
        self.root = Tk()
        self.root.title("MathIQ")
        self.root.geometry("500x200")

        self.model = model
        self.currentFrame = MainFrame(self.root,  self.postanalysis)

        self.root.mainloop()

    def postanalysis(self, trial_images):

        self.currentFrame.destroy();
        predictions = self.model.predict(np.array(trial_images.copy(), 'float64'))
        self.currentFrame = TestFrame(self.root, trial_images, predictions, self.finishedfile)

    def finishedfile(self, trial_images, trial_labels):
        self.currentFrame.destroy()
        #below line commented out until it can work
        #self.model(self.model.fit(np.array(trial_images.copy(), 'float64'), np.array(trial_labels), epochs=5))
        self.currentFrame = MainFrame(self.root,  self.postanalysis)


class MainFrame(Frame):

    def __init__(self, master, postFunc):
        super(MainFrame, self).__init__(master)

        self.file = 0
        self.postFunc = postFunc

        self.grid()
        self.textBox = Text(self, width=50, height=5, wrap=WORD)
        self.textBox.grid(row=0, column=0, columnspan=3, sticky=W)
        self.selectFileButton = Button(self, text="Select File")
        self.selectFileButton["command"] = self.findfile
        self.selectFileButton.grid(row=1, column=0, sticky=W)

    def findfile(self):
        #self.file = filedialog.askopenfilename(initialdir="/", title="Select file",
        #                                       filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        #used for testing
        self.file = filedialog.askopenfilename(initialdir="Users\Sasha\PycharmProjects\mathIQ_local", title="Select file",
                                               filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.textBox.insert(0.0, self.file)
        trial_images = letterFinder.img_to_array(self.file)
        self.postFunc(trial_images)


class TestFrame(Frame):

    def __init__(self, master, images, predictions, finishfunc):
        super(TestFrame, self).__init__(master)
        self.root = master
        self.old_images = images
        #self.images = images
        self.images = []
        for i in images:
            img = Image.fromarray(i)
            image = ImageTk.PhotoImage(img)
            self.images.append(image)
        self.predictions = predictions
        self.trail_labels = []
        for prediction in self.predictions:
            self.trail_labels.append(str(np.argmax(prediction)))
        self.finishfunc = finishfunc
        self.index = 0

        self.choices = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

        self.correction = StringVar(self.root)
        self.correction.set(self.trail_labels[self.index])

        self.grid()

        self.imagedisplay = Label(self, image=self.images[self.index])
        self.imagedisplay.grid(row=0, column=0, sticky=W)

        self.predictiondisplay = Label(self, text = "We think this number is " + self.trail_labels[self.index])
        self.predictiondisplay.grid(row=1, column=0, sticky=W)

        self.changelable = Label(self, text = "select the symbol that matches")
        self.changelable.grid(row=2, column=0, sticky=W)

        self.optionsmenu = OptionMenu(self.root, self.correction, *self.choices)
        self.optionsmenu.grid(row=3, column=0, sticky=W)
        self.correction.trace("w", self.correct)

        self.nextbutton = Button(self, text="next")
        self.nextbutton["command"] = self.next
        self.nextbutton.grid(row=4, column=3, sticky=S)

        self.previousbutton = Button(self, text="previous")
        self.previousbutton["command"] = self.previous
        self.previousbutton.grid(row=4, column=1, sticky=S)

        self.donebutton = Button(self, text="done")
        self.donebutton["command"] = self.done
        self.donebutton.grid(row=4, column=2, sticky=S)


    def setvalues(self):
        self.imagedisplay.configure(image= self.images[self.index])
        self.imagedisplay.image =  self.images[self.index]

        newstring = "We think this number is " + self.trail_labels[self.index]
        self.predictiondisplay.configure(text = newstring)
        self.predictiondisplay.text = newstring

        self.correction.set(self.trail_labels[self.index])

    def correct(self, *args):
        self.trail_labels[self.index] = self.correction.get()

    def next(self):
        if self.index < len(self.images)-1:
            self.index = self.index + 1
            self.setvalues()

    def previous(self):
        if self.index > 0:
            self.index = self.index - 1
            self.setvalues()

    def done(self):
        self.optionsmenu.destroy()
        self.finishfunc(self.old_images, self.trail_labels)
        #self.root.destroy()







