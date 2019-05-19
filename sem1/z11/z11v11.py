from tkinter import filedialog
from tkinter import *
from docx import *

class Task:
    def __init__(self):
        self.__init_GUI()

    def __init_GUI(self):
        self.mainWindow = Tk()
        self.opnWindow = None

        self.addMenu = Menu(self.mainWindow, tearoff=0)
        self.addMenu.add_command(label='Open Document', command=self.opn_btn_press)
        # self.addMenu.add_separator()
        self.mainWindow.config(menu=self.addMenu)

        self.txt = None

    def opn_btn_press(self):
        self.opnFile = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(("docx files", "*.docx"), ("all files", "*.*")))
        self.__config_GUI()

    def __config_GUI(self):
        self.txt = Text(self.mainWindow)

        doc = Document(self.opnFile)

        self.txt.insert(INSERT, '')
        self.txt.tag_add('start', CURRENT)
        for i, paragraph in enumerate(doc.paragraphs):
            for run in paragraph.runs:
                self.txt.insert(END, run.text)
                buf = self.txt.get('1.0', 'end')
                self.txt.tag_add('fiction', str(i+1) + '.' + str(len(buf)-len(run.text)),
                                 str(i+1) + '.' + str(len(buf)))
                self.txt.tag_config("fiction", background="yellow", foreground="blue")
            self.txt.insert(END, '\n')

        self.txt.pack()

    def run(self):
        self.mainWindow.mainloop()

if __name__ == '__main__':
    task = Task()
    task.run()