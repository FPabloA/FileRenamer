from tkinter import *
from tkinter import _setit
from tkinter import filedialog
from tmdbv3api import TV, TMDb, Season
import webbrowser
import os

tmdb = TMDb()
tmdb.api_key = ''
tv = TV()
season = Season()

def browse (window, page):
    #filename = filedialog.askopenfilename(initialdir="/", title="Select a Folder", filetypes=[("All files","*.*")])
    folder_selected = filedialog.askdirectory(initialdir=window.lastDir, title="Select a Folder")
    #window.label_file_explorer.configure(text="File Opened: "+filename)
    window.lastDir = folder_selected
    page.label.configure(text="Folder Opened: "+folder_selected)

#defines the parameters of the underlying tkinter window and handles frame switching
class MainWin:
    def __init__(self) -> None:
        self.lastDir = "/"
        self.window = Tk()
        self.container = Frame(self.window)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #creates and stores a list of frames to switch between
        self.frames = {}
        for F in (StartPage, SeqPage, TMDBPage, HelpPage):
            pgName = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[pgName] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartPage")


        self.window.title("File Renamer")
        self.window.geometry("400x300")

        self.window.mainloop()

    def showFrame(self, pgName):
            #ensures a directory is selected before allowing the user to switch to other pages
            if(self.lastDir != '/'):
                frame = self.frames[pgName]
                frame.updateFrame()
                frame.tkraise()
            else:
                frame = self.frames["StartPage"]
                frame.updateFrame()
                frame.tkraise()
                print("please select a directory")

#defines and displays the features of the start page frame
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

#defines and displays the features of the sequential naming frame
class SeqPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="Selected Dir: ", fg="blue", font = ('calibre',12,'normal'))
        self.label.grid(row=0, column=0,  columnspan=3, sticky=EW)
        button_Back = Button(self, text="Back",
                           command=lambda: controller.showFrame("StartPage"))
        
        #hold the contents of the prefix and start seq entry boxes
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
    
    #updates the currently opened label
    def updateFrame(self):
        self.label.configure(text="Folder Opened: "+self.controller.lastDir)
        if(self.prefix.get() != ""):
            self.label_preview.configure(text="Preview File Name: " + self.prefix.get() + "*")

    #ensures that users can only enter digits into the seq entry
    def validateSeq(self, val):
        if str.isdigit(val) or val == "":
            return True
        else:
            return False
    
    #loops through the files of the selected directory and renames them according to the parameters set by the user
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

    #if an error occurs at any point in the renaming process, revert files that were already renamed and exit
    def rollback(self, backup):
        currDir = self.controller.lastDir
        for filename in os.listdir(currDir):
            if(len(backup) == 0):
                break
            os.rename(os.path.join(currDir, filename), os.path.join(currDir, backup.pop(0)))
        
#defines and displays the features of the sequential naming frame
class TMDBPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="Selected Dir: ", fg="blue", font = ('calibre',12,'normal'))
        self.label.grid(row=0, column=0,  columnspan=3)
        self.grid_columnconfigure((0,1,2), weight=1)

        self.TMDBName = StringVar()
        self.suggestions = {}
        self.currSelect = None
        self.seasonSelect = IntVar()

        label_Name = Label(self, text="TMDB Name: ", font=('calibre',10, 'bold'))
        entry_Name = Entry(self, textvariable=self.TMDBName, font = ('calibre',10,'normal'))
        entry_Name.bind('<KeyRelease>', self.checkkey)
        self.lb_suggestions = Listbox(self, height=5, selectmode=SINGLE)
        self.lb_suggestions.bind('<<ListboxSelect>>', self.sugSelect)

        label_Seasons = Label(self, text="Seasons: ", font=('calibre',10, 'bold'))
        self.spin_Seasons = Spinbox(self, from_=1, to=1, textvariable=self.seasonSelect)

        button_TMDB = Button(self, text="TMDB Page",
                           command=lambda: self.openPage())
        button_Rename = Button(self, text="Rename",
                           command=lambda: self.renameFiles())
        button_Back = Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        
        label_Name.grid(row=1, column=0)
        entry_Name.grid(row=1, column=1, columnspan=3, sticky=EW, pady=5, padx=10)
        self.lb_suggestions.grid(row=2, column=1, columnspan=3, padx=10, sticky=NSEW)
        label_Seasons.grid(row=3, column=0, pady=5)
        self.spin_Seasons.grid(row=3, column=1, pady=5, padx=9, sticky=W)
        button_TMDB.grid(row=4, column=0, pady=5)
        button_Rename.grid(row=4, column=2)
        button_Back.grid(row=5, column=0, pady=10)

        self.updateLB(1)
        
    def updateFrame(self):
        self.label.configure(text="Folder Opened: "+self.controller.lastDir)

    def checkkey(self, event):
        input = self.TMDBName.get()
        self.fetchSuggestions(input)

        if input == '':
            list = 1
        else:
            list = []
            for item in self.suggestions.values():
                if input.lower() in item.name.lower():
                    list.append(item)
        self.updateLB(list)

    def updateLB(self, list):
        self.lb_suggestions.delete(0, 'end')

        if(list != 1):
            for item in list:
                self.lb_suggestions.insert('end', item.name)
    
    def sugSelect(self, event):
        value = self.lb_suggestions.get(self.lb_suggestions.curselection())
        self.TMDBName.set(value)
        self.currSelect = self.suggestions[value]
        details = tv.details(self.currSelect.id)
        self.spin_Seasons.config(from_= 1, to=details["number_of_seasons"])
        print(self.currSelect)
        

    def fetchSuggestions(self, input):
        results = tv.search(input)
        self.suggestions.clear()
        for show in results:
            self.suggestions[show.name] = show

    def openPage(self):
        webbrowser.open('https://www.themoviedb.org/tv/' + str(self.currSelect.id))
        
            

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
















  

  


