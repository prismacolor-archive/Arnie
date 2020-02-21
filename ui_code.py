# -*- coding: utf-8 -*-

# import required libraries
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk
import fitz


filepath = 'output.csv'  # define pathname for output CSV file
with open(filepath, 'w+') as f:  # open the CSV file
    f.write('x1,y1,x2,y2,Label\n')  # specify the headers of the CSV file


# run this function when the Confirm button is pressed
def clicked(box, entry):  # box is the position of the rectangle and label is the text in the entry bar
    res = entry.get()  # get label text from the entry bar
    entry.delete(0, 'end')
    print(box, res)  # print the rectangle position and the label text for debugging
    with open(filepath, 'a+') as f:  # open the CSV file
        # write output data into one CSV row -- the two x,y positions that define the selection rectangle, and the label text
        f.write(str(box[0]) + ',' + str(box[1]) + ',' + str(box[2]) + ',' + str(box[3]) + ',' + res + '\n')


class MainCanvas(Frame):  # define the main canvas
    def __init__(self, master, **kwargs):  # initialize the class
        Frame.__init__(self, master, **kwargs)  # initialize a frame from tkinter

        self.grid_rowconfigure(0, weight=1)  # set the row weight to distribute the space between rows
        self.grid_columnconfigure(0, weight=1)  # set the column weight to distribute the space between columns

        self.canv = Canvas(self, bd=0, highlightthickness=0)  # create a canvas in the frame

        self.canv.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)  # put the canvas in the grid at (position (0, 0))
        # self.combo.grid(row=1, column=0, sticky='nsew', padx=4, pady=4)


class MyApp(Tk):  # define the window
    def __init__(self):  # initialize the class
        Tk.__init__(self)  # initialize tkinter window
        self.grid_rowconfigure(0, weight=1)  # set the row weight to distribute the space between rows
        self.grid_columnconfigure(0, weight=1)  # set the column weight to distribute the space between columns

        self.main = MainCanvas(self)  # create a canvas inside the window, called main
        self.main.grid(row=0, column=0, sticky='nsew')  # put the canvas in the grid at (position (0, 0))
        self.c = self.main.canv  # define c as the canvas in the main Frame (mainCanvas)

        self.currentImage = {}  # initialize currentImage parameter

        self.button = Button(self, text="Browse...", command=self.load_imgfile,
                             width=10)  # define a button used to browse and load the selected PDF

        self.button.grid(row=1, column=0, sticky="nsew")  # Put the button in the grid at (position (1, 0))

        # wait for mouse clicks and movements
        self.c.bind('<ButtonPress-1>', self.on_mouse_down)
        self.c.bind('<B1-Motion>', self.on_mouse_drag)
        self.c.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.c.bind('<Button-3>', self.on_right_click)

        self.dim = (0, 0, 0, 0)  # initialize the box values
        self.txt = Entry(self, width=10)  # define a text entry bar inside the window
        self.txt.grid(row=2, column=0, sticky='nsew', padx=4, pady=4)  # set a position for the entry bar

        self.lbl = Label(self)  # define a tkinter label for the user text entry
        self.lbl.grid(row=4, column=0, sticky='nsew', padx=4, pady=4)  # set a position for the Confirm button

        self.btn = Button(self, text="Confirm", command=lambda: clicked(self.dim, self.txt))  # define a Confirm button
        self.btn.grid(row=3, column=0, sticky='nsew', padx=4, pady=4)  # set a position for the Confirm button

    def load_imgfile(self):
        filename = filedialog.askopenfilename()  # ask the user to choose the PDF file that will be annotated
        doc = fitz.open(filename)  # Open the PDF document
        page = doc.loadPage(0)  # choose the first page of the PDF
        img = page.getPixmap()  # convert the page into image
        output = "outfile.png"  # define the output file name
        img.writePNG(output)  # save the image

        img = Image.open(output)  # open the image
        self.currentImage['data'] = img  # put the image in the currentImage directory

        photo = ImageTk.PhotoImage(img)  # convert the image into tkinter image to be used in the GUI
        self.c.create_image(0, 0, image=photo, anchor='nw', tags='img')  # put the image into the GUI
        self.currentImage['photo'] = photo  # put the image in the currentImage dictionary
        self.img_size = self.currentImage['data'].size  # define and set the img_size parameter

        self.geometry(str(self.img_size[0]) + 'x' + str(self.img_size[1]))  # change the size of the window to fit the image

    def on_mouse_down(self, event):  # define a click method
        self.anchor = (event.widget.canvasx(event.x),
                       event.widget.canvasy(event.y))  # define the anchor as the x and y position of the click
        self.item = None  # define a check variable

    def on_mouse_drag(self, event):  # define a drag mouse method
        bbox = self.anchor + (event.widget.canvasx(event.x),
                              event.widget.canvasy(event.y))  # get the x and y position of the mouse
        if self.item is None:  # check item is empty
            self.item = event.widget.create_rectangle(bbox, outline="red")  # draw the red selection rectangle
        else:
            event.widget.coords(self.item, *bbox)  # else draw the selection rectangle using the mouse position

    def on_mouse_up(self, event):  # define a release click method
        if self.item:  # check if the mouse was clicked
            self.on_mouse_drag(event)  # if the mouse was clicked, use the drag mouse method
            self.dim = tuple(
                (int(round(v)) for v in event.widget.coords(self.item)))  # define the selection rectangle position

    def on_right_click(self, event):  # define a clear method
        found = event.widget.find_all()  # collect all past clicks events
        for iid in found:  # for each click
            if event.widget.type(iid) == 'rectangle':  # check if it's a selection rectangle
                event.widget.delete(iid)  # delete the selection rectangle (but currently not updating the output file)


# this is the main function
if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
