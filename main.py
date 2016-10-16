import os
import re

from tkinter import *
from tkinter import filedialog # ! bug in cx_Freeze, should load explicitly
from app import App

class Gui(Tk, App):
    def __init__(self, *argp, **argv):
        Tk.__init__(self)
        App.__init__(self, *argp, **argv)
        
        self.title('French Songs')

        self.radioBoolVar = BooleanVar(self, value = self.isWholeWord)
        self.searchStringVar = StringVar(self)
        self.result = dict()
        
        self.drawWindow()
        self.showCount()

    def drawWindow(self):
        self.geometry('800x600')
        
        self.gui_LabelFrame_Path = LabelFrame(self, text = 'Path to examples:', padx = 10, pady = 10)
        self.gui_LabelFrame_Path.pack(expand = YES, fill = X)
        self.gui_Label_Path = Label(self.gui_LabelFrame_Path, text = os.path.abspath(self.datadir))
        self.gui_Label_Path.pack(side = LEFT)
        Button(self.gui_LabelFrame_Path, text = "...", command = self.selectPath).pack(side = RIGHT)

        self.gui_Label_Info = Label(self)
        self.gui_Label_Info.pack()

        self.gui_LabelFrame_Search = LabelFrame(self, text = 'Search in examples:', padx = 10, pady = 10)
        self.gui_LabelFrame_Search.pack(expand = YES, fill = X)
        Entry(self.gui_LabelFrame_Search, font = ('Helvetica','16','bold'), textvariable = self.searchStringVar).pack(side = LEFT, expand = YES, fill = X)
        Button(self.gui_LabelFrame_Search, text = 'Search', command = self.search).pack(side = RIGHT)
        Checkbutton(self.gui_LabelFrame_Search, text = "Whole word", variable = self.radioBoolVar, command = self.changeCheckbox).pack(side = RIGHT)

        self.gui_LabelFrame_Result = LabelFrame(self, text = 'Result (double click to open file):', padx = 10, pady = 10)
        self.gui_LabelFrame_Result.pack(expand = YES, fill = BOTH)

        self.gui_Frame_Result = Frame(self.gui_LabelFrame_Result)
        self.gui_Frame_Result.pack(expand = YES, fill = BOTH)
        
        self.gui_yScroll = Scrollbar(self.gui_Frame_Result, orient = VERTICAL)
        
        self.gui_List_Result = Listbox(self.gui_Frame_Result, yscrollcommand = self.gui_yScroll.set)
        self.gui_List_Result.pack(side = LEFT, expand = YES, fill = BOTH)
        self.gui_List_Result.bind('<<ListboxSelect>>', self.handleListClick)
        self.gui_List_Result.bind('<Double-1>', self.handleListDouble)
        
        self.gui_yScroll['command'] = self.gui_List_Result.yview
        self.gui_yScroll.pack(side = LEFT, fill = Y)
        
        self.gui_Text_Result = Text(self.gui_LabelFrame_Result, height = 7, bg = 'gray70', font = ('Helvetica','16'))
        self.gui_Text_Result.pack(expand = YES, fill = BOTH)
        self.gui_Text_Result.tag_config('highlight', foreground = 'red', font = ('Helvetica','16','bold'))

    def selectPath(self):
        newPath = filedialog.askdirectory()
        if newPath:
            self.datadir = newPath
            self.gui_Label_Path['text'] = os.path.abspath(self.datadir)
            
            self.clearExamples()
            self.scandir()
            self.showCount()

    def showCount(self):
        if self.count[1]:
            self.gui_Label_Info['text'] = '%d lines have been loaded from %d files' % (self.count[1], self.count[0])
        else:
            self.gui_Label_Info['text'] = 'There is no examples! Try to choose another path.'

    def search(self):
        self.clearResult()

        self.result = self.find(self.searchStringVar.get().strip())

        for example in self.result:
            self.gui_List_Result.insert(END, example)

    def changeCheckbox(self):
        # print(self.radioBoolVar.get())
        self.isWholeWord = self.radioBoolVar.get()

    def handleListClick(self, event):
        self.gui_Text_Result.delete('1.0', END)

        # using just '.get(ACTIVE)' cause not properly working when selecting with mouse (ACTIVE index updates after event handler)
        w = event.widget
        if w.size() == 0:
            return 'break'
        index = int(w.curselection()[0])
        example = w.get(index)

        for row, text in enumerate(self.result[example], 1):
            self.gui_Text_Result.insert(END, '%s (%d)\n' % (text[1], text[0]))

            self.highlight(text[1], row)
            
    def handleListDouble(self, event):
        if self.gui_List_Result.size() == 0:
            return 'break'
        file = self.gui_List_Result.get(ACTIVE) + '.txt'
        os.popen('notepad ' + os.path.join(self.datadir, file))
        
    def highlight(self, text, row):
        for match in re.finditer(self.pattern, text, flags = re.IGNORECASE):
            self.gui_Text_Result.tag_add('highlight', '%d.%d' % (row, match.start()), '%d.%d' % (row, match.end()))
    
    def clearResult(self):
        self.result = dict()
        self.gui_List_Result.delete(0, END)
        self.gui_Text_Result.delete('1.0', END)

if __name__ == '__main__':
    win = Gui(isWholeWord = True)
    win.mainloop()
