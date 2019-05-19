from tkinter import filedialog
from tkinter import *
from docx import *
from tkinter.font import Font

class Task(Tk):
    def __init__(self):
        super().__init__()

        self.opnFile = None

        self.__init_GUI()

    def __init_GUI(self):
        self.addMenu = Menu(self, tearoff=0)
        self.addMenu.add_command(label='Open Document', command=self.opn_btn_press)
        # self.addMenu.add_separator()
        self.config(menu=self.addMenu)
        self.txt = None

    def opn_btn_press(self):
        self.opnFile = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                  filetypes=(("docx files", "*.docx"), ("all files", "*.*")))
        self.__config_GUI()

    def __config_GUI(self):
        doc = Document(self.opnFile)

        self.txt = Text(self)
        abzac = 1
        for paragraph in doc.paragraphs:
            leng = 0
            for run in paragraph.runs:
                self.txt.insert('end', run.text)
                leng += len(run.text)

                beg = str(abzac) + '.' + str(leng-len(run.text))
                self.txt.tag_add('{}'.format(run.text), beg, 'end')

                #run formatting
                # bg_color = 'yellow'
                color = run.font.color.rgb
                fg_color = '#000000' if color is None else '#'+str(color)
                fnt_name = run.font.name  # 'Times New Roman'
                # вот тут аж бесит! не везде видит размер шрифта:
                fnt_size = int(run.font.size.pt) if run.font.size else 14
                fnt_wg = 'bold' if run.font.bold else 'normal'
                fnt_sl = 'italic' if run.font.italic else 'roman'

                fnt = Font(family=fnt_name, size=fnt_size,
                               weight=fnt_wg, slant=fnt_sl)


                self.txt.tag_config('{}'.format(run.text),
                                    # background=bg_color,
                                    foreground=fg_color,
                                    font=fnt)

                # self.txt.tag_delete('va')
            self.txt.insert('end', '\n')
            abzac += 1

        # doc.save()

        self.txt.pack()


if __name__ == '__main__':
    tsk = Task()
    tsk.mainloop()