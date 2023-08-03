from tkinter import *
from tkinter import filedialog

def browse (window):
    #filename = filedialog.askopenfilename(initialdir="/", title="Select a Folder", filetypes=[("All files","*.*")])
    folder_selected = filedialog.askdirectory(initialdir=window.lastDir, title="Select a Folder")
    #window.label_file_explorer.configure(text="File Opened: "+filename)
    window.lastDir = folder_selected
    window.label_file_explorer.configure(text="Folder Opened: "+folder_selected)

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


        # self.window.title("File Explorer")
        # self.window.geometry("400x300")
        # self.window.grid_columnconfigure((0,1,2), weight=1)

        # self.label_file_explorer = Label(self.window, text = "Selected Dir:", fg="blue")
        
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
            frame = self.frames[pgName]
            frame.tkraise()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to Page One",
                            command=lambda: controller.showFrame("SeqPage"))
        button2 = Button(self, text="Go to Page Two",
                            command=lambda: controller.showFrame("TMDBPage"))
        button1.pack()
        button2.pack()

class SeqPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is Sequential Naming")
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button.pack()

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
















  

  


