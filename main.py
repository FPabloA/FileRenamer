from tkinter import *
from tkinter import filedialog
import os

def browse (window, page):
    #filename = filedialog.askopenfilename(initialdir="/", title="Select a Folder", filetypes=[("All files","*.*")])
    folder_selected = filedialog.askdirectory(initialdir=window.lastDir, title="Select a Folder")
    #window.label_file_explorer.configure(text="File Opened: "+filename)
    window.lastDir = folder_selected
    page.label.configure(text="Folder Opened: "+folder_selected)

class MainWin:
    def __init__(self) -> None:
        self.lastDir = "/"
        self.window = Tk()
        self.container = Frame(self.window)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SeqPage, TMDBPage, HelpPage):
            pgName = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[pgName] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartPage")


        self.window.title("File Explorer")
        self.window.geometry("400x300")
        self.window.grid_columnconfigure((0,1,2), weight=1)

        
        
        # self.button_explore = Button(self.window, text = "Browse Folders",
        #                 command = lambda: browse(self))
        # self.button_seq = Button(self.window, text = "Sequential Naming",
        #                 command = lambda: print("seq"))
        # self.button_tmdb = Button(self.window, text = "TMDB Match & Name",
        #                 command = lambda: print("TMDB"))
        # self.button_exit = Button(self.window, text = "Exit",
        #              command = exit)
        # self.button_help = Button(self.window, text = "?",
        #              command = lambda: print("Help"))

        #window organization
        # self.label_file_explorer.grid(row=0, column=1, sticky="ew", pady=10)
        # self.button_explore.grid(row=1, column=1, pady=5)
        # self.button_seq.grid(row=2, column=1, pady=5)
        # self.button_tmdb.grid(row=3, column=1, pady=5)
        # self.button_exit.grid(row=4, column=1, pady=120)
        # self.button_help.grid(row=4, column=0, pady=120)

        self.window.mainloop()

    def showFrame(self, pgName):
            if(self.lastDir != '/'):
                frame = self.frames[pgName]
                frame.updateFrame()
                frame.tkraise()
            else:
                print("please select a directory")

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text = "Selected Dir:", fg="blue", font = ('calibre',12,'normal'))
        self.label.pack(side="top", fill="x", pady=10)

        button_Browse = Button(self, text = "Browse Folders",
                        command = lambda: browse(controller, self))

        button_Seq = Button(self, text="Go to Seq Naming",
                            command=lambda: controller.showFrame("SeqPage"))
        button_TMDB = Button(self, text="Go to TMDB Naming",
                            command=lambda: controller.showFrame("TMDBPage"))
        
        button_Help = Button(self, text = "?",
                     command = lambda: print("Help"))

        button_Browse.pack(pady=5)
        button_Seq.pack(pady=5)
        button_TMDB.pack(pady=5)
        button_Help.pack(pady=65)

    def updateFrame(self):
        print('called update start')

class SeqPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="Selected Dir: ", fg="blue", font = ('calibre',12,'normal'))
        self.label.grid(row=0, column=0,  columnspan=3, sticky=EW)
        button_Back = Button(self, text="Back",
                           command=lambda: controller.showFrame("StartPage"))
        
        self.prefix = StringVar()
        self.seq = StringVar()

        label_prefix = Label(self, text="Prefix: ", font=('calibre',10, 'bold'))
        entry_prefix = Entry(self, textvariable=self.prefix, font = ('calibre',10,'normal'))

        label_seq = Label(self, text="Start from:  ", font=('calibre',10, 'bold'))
        vcmd = (self.register(self.validateSeq))
        entry_seq = Entry(self, textvariable=self.seq, font = ('calibre',10,'normal'), validate='all', validatecommand=(vcmd, '%P'))
        button_preview = Button(self, text='Show Preview', command=lambda: self.updateFrame())

        self.label_preview = Label(self, text="", font=('calibre',10, 'bold'))

        button_Rename = Button(self, text="Rename",
                           command=lambda: self.renameFiles())


        label_prefix.grid(row=1, column=0)
        entry_prefix.grid(row=1, column=1, columnspan=2, sticky=EW, pady=5)
        label_seq.grid(row=2, column=0, pady=5)
        entry_seq.grid(row=2, column=1, sticky=EW)
        button_preview.grid(row=2, column=2, padx=5)
        self.label_preview.grid(row=3, column=1, sticky=EW, pady=5)
        button_Rename.grid(row=4, column=1, sticky=EW, pady=10)
        button_Back.grid(row=4, column=0)
    
    def updateFrame(self):
        print("called seq update")
        self.label.configure(text="Folder Opened: "+self.controller.lastDir)
        if(self.prefix.get() != ""):
            self.label_preview.configure(text="Preview File Name: " + self.prefix.get() + "*")

    def validateSeq(self, val):
        if str.isdigit(val) or val == "":
            return True
        else:
            return False
        
    def renameFiles(self):
        currDir = self.controller.lastDir
        backupList = []
        start = 1
        if self.seq.get() != "":
            start = int(self.seq.get())
        for filename in os.listdir(currDir):
            extension = os.path.splitext(filename)[1]
            newName = self.prefix.get() + str(start) + extension
            try:
                os.rename(os.path.join(currDir, filename), os.path.join(currDir, newName))
            except OSError:
                self.rollback(backupList)
                exit()
            backupList.append(filename)
            start += 1

    def rollback(self, backup):
        print("rollback called")
        currDir = self.controller.lastDir
        for filename in os.listdir(currDir):
            if(len(backup) == 0):
                break
            os.rename(os.path.join(currDir, filename), os.path.join(currDir, backup.pop(0)))
        

class TMDBPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is TMDB Naming")
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button.pack()

class HelpPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is the Help Page")
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button.pack()

init_window = MainWin()
















  

  


