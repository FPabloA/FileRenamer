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
        # self.frame = Frame(self.window)
        # self.frame.pack()

        # self.bottomFrame = Frame(self.window)
        # self.bottomFrame.pack(side=BOTTOM)

        self.window.title("File Explorer")
        self.window.geometry("400x300")
        self.window.grid_columnconfigure((0,1,2), weight=1)
        # self.window.grid_rowconfigure((0,1,2), weight=1)

        self.label_file_explorer = Label(self.window, text = "Selected Dir:", fg="blue")
        
        self.button_explore = Button(self.window, text = "Browse Folders",
                        command = lambda: browse(self))
        self.button_seq = Button(self.window, text = "Sequential Naming",
                        command = lambda: print("seq"))
        self.button_tmdb = Button(self.window, text = "TMDB Match & Name",
                        command = lambda: print("TMDB"))
        self.button_exit = Button(self.window, text = "Exit",
                     command = exit)
        self.button_help = Button(self.window, text = "?",
                     command = lambda: print("Help"))

        #window organization
        self.label_file_explorer.grid(row=0, column=1, sticky="ew", pady=10)
        self.button_explore.grid(row=1, column=1, pady=5)
        self.button_seq.grid(row=2, column=1, pady=5)
        self.button_tmdb.grid(row=3, column=1, pady=5)
        self.button_exit.grid(row=4, column=1, pady=120)
        self.button_help.grid(row=4, column=0, pady=120)

        self.window.mainloop()

init_window = MainWin()
















  

  


