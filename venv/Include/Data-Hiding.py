from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import cv2
import tkinter as tk
import numpy as np
from CPT import Util,k,w
import io

class Root(Tk):

    util = Util()
    imgResult = None
    txtResult = None

    def __init__(self):
        super(Root, self).__init__()
        self.tabControl = ttk.Notebook(self)
        self.iconbitmap('./icon.ico')

        self.tab0 = ttk.Frame(self.tabControl)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Encode')
        self.tabControl.add(self.tab2, text='Decode')
        self.tabControl.add(self.tab0, text='Author')
        self.tabControl.pack(expand=1, fill="both")
        self.title("Data-hiding though Image")
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("750x550+%d+%d" % (screen_width / 2 - 275, screen_height / 2 - 250))

        #=== Author ===
        self.createAuthourInfos()

        #=== ENCODE ===
        self.createBrowseImage_tab1()
        self.createBrowseText_tab1()
        self.createButtonConvert_tab1()
        self.createButtonSave_tab1()

        #== DECODE ===
        self.createBrowseImage_tab2()
        self.createButtonDecode_tab2()
        self.createButtonSave_tab2()

    #====== BEGIN AUTHOR TAB ===========#
    def createAuthourInfos(self):
        self.lblName_tab0 = ttk.Label(self.tab0,     text="Name:")
        self.lblName_tab0.grid(row=1, column=0, sticky=W, pady=10, padx=20)
        self.lblName1_tab0 = ttk.Label(self.tab0, text="Nguyen, Truong An")
        self.lblName1_tab0.grid(row=1, column=1, sticky=W, pady=10)

        self.lblEmail1_tab0 = ttk.Label(self.tab0,   text="Email:")
        self.lblEmail1_tab0.grid(row=2, column=0, sticky=W, pady=10,  padx=20)
        self.lblEmail11_tab0 = ttk.Label(self.tab0, text="nguyentruongan.it.dlu@gmail.com")
        self.lblEmail11_tab0.grid(row=2, column=1, sticky=W)

        self.lblEmail2_tab0 = ttk.Label(self.tab0,   text="Truong.Nguyen@Student.HTW-Berlin.de")
        self.lblEmail2_tab0.grid(row=3, column=1, sticky=W)

        self.lblFacebook_tab0 = ttk.Label(self.tab0, text="Facebook:")
        self.lblFacebook_tab0.grid(row=4, column=0, sticky=W, pady=20)
        self.lblFacebook1_tab0 = ttk.Label(self.tab0, text="https://www.facebook.com/yiianguyen")
        self.lblFacebook1_tab0.grid(row=4, column=1, sticky=W)

        self.lblGithub_tab0 = ttk.Label(self.tab0, text="Github:")
        self.lblGithub_tab0.grid(row=5, column=0, sticky=W, pady=10)
        self.lblGithub1_tab0 = ttk.Label(self.tab0, text="https://github.com/yiimnta")
        self.lblGithub1_tab0.grid(row=5, column=1, sticky=W)

        self.lblAlgorithm_tab0 = ttk.Label(self.tab0, text="Algorithm:")
        self.lblAlgorithm_tab0.grid(row=6, column=0, sticky=W, pady=20)
        self.lblAlgorithm1_tab0 = ttk.Label(self.tab0, text="Chen-Pan-Tseng")
        self.lblAlgorithm1_tab0.grid(row=6, column=1, sticky=W)
    #====== END AUTHOR TAB ===========#

    #====== BEGIN ENCODE TAB ===========#
    def createBrowseImage_tab1(self):
        self.lblImage_tab1 = ttk.Label(self.tab1, text="1. Select an Image")
        self.lblImage_tab1.grid(row=0, column=0, pady=15, sticky=W)
        self.btnImage_tab1 = ttk.Button(self.tab1, text="Browse", command=self.fileImageDialog_tab1)
        self.btnImage_tab1.grid(row=1, column=0)
        self.txtImage_tab1 = ttk.Entry(self.tab1, width=50, state='readonly')
        self.txtImage_tab1.grid(row=1, column=1)

    def fileImageDialog_tab1(self):
        self.filename_tab1 = filedialog.askopenfilename(initialdir="/", title="Select an Image", filetype=
        (("image files", "*.png;*.jpg"), ("all files", "*.*")))
        self.txtImage_tab1.configure(state='normal')
        self.txtImage_tab1.delete(0, END)
        self.txtImage_tab1.insert(0, self.filename_tab1)
        self.createImageLeft_tab1(self.filename_tab1)
        self.txtImage_tab1.configure(state='readonly')

    def createBrowseText_tab1(self):
        self.lblText_tab1 = ttk.Label(self.tab1, text="2. Select Text file")
        self.lblText_tab1.grid(row=2, column=0, pady=15, sticky=W)
        self.btnText_tab1 = ttk.Button(self.tab1, text="Browse", command=self.selectFileText_tab1)
        self.btnText_tab1.grid(row=3, column=0)
        self.txtText_tab1 = ttk.Entry(self.tab1, width=50, state='readonly')
        self.txtText_tab1.grid(row=3, column=1)

    def selectFileText_tab1(self):
        self.textname_tab1 = filedialog.askopenfilename(initialdir="/", title="Select a File", filetype=(("Notepad files","*.txt"), ("all files", "*.*")))
        self.txtText_tab1.configure(state='normal')
        self.txtText_tab1.delete(0, END)
        self.txtText_tab1.insert(0, self.textname_tab1)
        self.txtText_tab1.configure(state='readonly')

    def createImageLeft_tab1(self, filePath):
        if filePath is None or filePath == "":
            return
        self.lblInput_tab1 = ttk.Label(self.tab1, text="Input:")
        self.lblInput_tab1.grid(column=0, sticky=W+E+S+N, row=5, columnspan=2, pady=25, padx=10)
        imgBinary = self.util.convertImageToBlackWhiteImage(filePath)

        img = Image.fromarray(imgBinary)
        img = img.resize((290, 290))
        imgL = ImageTk.PhotoImage(img)
        self.imgLeft_tab1 = Label(self.tab1, image=imgL)
        self.imgLeft_tab1.image = imgL
        self.imgLeft_tab1.grid(column=0, sticky=W, row=6, columnspan=2, pady=4, padx=10)

    def createButtonSave_tab1(self):
        self.btnSave_tab1 = ttk.Button(self.tab1, text="Save", command=self.saveFile_tab1, width=40)
        self.btnSave_tab1.grid(row=3, rowspan=1, column=3, padx=20, sticky=N+S+E+W)

    def saveFile_tab1(self):
        if self.imgResult is None:
            return

        files = [("image files", "*.png;*.jpg"),('All Files', '*.*')]
        self.savePath_tab1 = filedialog.asksaveasfile(title="Save the image",filetypes=files, defaultextension=files)
        if self.savePath_tab1 is None:
            return
        path = self.savePath_tab1.name
        self.util.convertMatrixToImage(self.imgResult, path)
        messagebox.showinfo("Message Box", "Save image successfully!")

    def createButtonConvert_tab1(self):
        self.btnConvert_tab1 = ttk.Button(self.tab1, text="Convert", command=self.convert_tab1)
        self.btnConvert_tab1.grid(row=1, rowspan=2, column=3, padx=20, sticky=N+S+E+W)

    def convert_tab1(self):
        if self.filename_tab1 is None or self.filename_tab1 == "":
            messagebox.showerror("Error", "Please select an image")
            return
        if self.textname_tab1 is None or self.textname_tab1 == "":
            messagebox.showerror("Error", "Please select a Text file")
            return

        self.imgResult = self.util.runEncode(self.filename_tab1, self.textname_tab1)
        self.createImageRight_tab1()

    def createImageRight_tab1(self):
        self.lblOutput_tab1 = ttk.Label(self.tab1, text="Output:")
        self.lblOutput_tab1.grid(column=2, row=5, columnspan=2, pady=25, padx=10)

        img = Image.fromarray(self.imgResult)
        img = img.resize((290, 290))
        imgL = ImageTk.PhotoImage(img)
        self.imgRight_tab1 = Label(self.tab1, image=imgL)
        self.imgRight_tab1.image = imgL
        self.imgRight_tab1.grid(column=2, row=6, columnspan=2, pady=5, padx=10)
        messagebox.showinfo("Message Box", "Convert successfully!")

    # ====== END ENCODE TAB ===========#

    # ====== BEGIN DECODE TAB ===========#

    def createBrowseImage_tab2(self):
        self.lblImage_tab2 = ttk.Label(self.tab2, text="1. Select an Image")
        self.lblImage_tab2.grid(row=0, column=0, pady=15, sticky=W)
        self.btnImage_tab2 = ttk.Button(self.tab2, text="Browse", command=self.fileImageDialog_tab2)
        self.btnImage_tab2.grid(row=1, column=0)
        self.txtImage_tab2 = ttk.Entry(self.tab2, width=50, state='readonly')
        self.txtImage_tab2.grid(row=1, column=1)

    def fileImageDialog_tab2(self):
        self.filename_tab2 = filedialog.askopenfilename(initialdir="/", title="Select an Image", filetype=
        (("image files", "*.png;*.jpg"), ("all files", "*.*")))
        self.txtImage_tab2.configure(state='normal')
        self.txtImage_tab2.delete(0, END)
        self.txtImage_tab2.insert(0, self.filename_tab2)
        self.createImageLeft_tab2(self.filename_tab2)
        self.txtImage_tab2.configure(state='readonly')

    def createImageLeft_tab2(self, filePath):
        if filePath is None or filePath == "":
            return
        self.lblInput_tab2 = ttk.Label(self.tab2, text="Input:")
        self.lblInput_tab2.grid(column=0, sticky=W+E+S+N, row=2, columnspan=2, pady=25, padx=10)
        img = Image.open(filePath)
        img = img.resize((290, 290))
        imgL = ImageTk.PhotoImage(img)
        self.imgLeft_tab2 = Label(self.tab2, image=imgL)
        self.imgLeft_tab2.image = imgL
        self.imgLeft_tab2.grid(column=0, sticky=W, row=3, columnspan=2, pady=4, padx=10)

    def createButtonSave_tab2(self):
        self.btnSave_tab2 = ttk.Button(self.tab2, text="Save", command=self.saveFile_tab2)
        self.btnSave_tab2.grid(row=1, rowspan=1, column=4, padx=20, sticky=N+S+E+W)

    def saveFile_tab2(self):
        if self.txtResult is None:
            return

        files = [("Text file", "*.txt"),('All Files', '*.*')]
        self.savePath_tab2 = filedialog.asksaveasfile(title="Save the text",filetypes=files, defaultextension=files)
        if self.savePath_tab2 is None:
            return
        path = self.savePath_tab2.name
        file = io.open(path, "w", encoding="utf8")
        file.write(self.txtResult)
        file.close()
        messagebox.showinfo("Message Box", "Save text file successfully!")

    def decode_tab2(self):
        if self.filename_tab2 is None or self.filename_tab2 == "":
            messagebox.showerror("Error", "Please select an image")
            return

        self.txtResult = self.util.runDecode(self.filename_tab2)
        self.createTextArea_tab2()

    def createButtonDecode_tab2(self):
        self.btnDecode_tab2 = ttk.Button(self.tab2, text="Decode", command=self.decode_tab2)
        self.btnDecode_tab2.grid(row=1, rowspan=1, column=3, padx=20, sticky=N+S+E+W)

    def createTextArea_tab2(self):
        if self.txtResult is None:
            messagebox.showerror("Error", "Please select an image")
            return

        self.lblOutput_tab2 = ttk.Label(self.tab2, text="Output:")
        self.lblOutput_tab2.grid(column=2, row=2, columnspan=2, pady=25, padx=10)
        self.txtarea_tab2 = tk.Text(self.tab2, height=19, width=30)
        self.txtarea_tab2.grid(row=3, column=2, columnspan=2)
        self.txtarea_tab2.delete('1.0', END)
        self.txtarea_tab2.insert(tk.END, self.txtResult)

    # ====== END DECODE TAB ===========#
root = Root()
root.mainloop()