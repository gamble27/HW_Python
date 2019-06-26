import os.path as path
import datetime

class SysJournal:
    def __init__(self, pth=None):
        self.full_path = pth
        if pth:
            self.divide()
        else:
            self.name = None
            self.reg_name = None
            self.date = None
            self.size = None

    @classmethod
    def _get_journ_dir(cls):
        while True: #zapah govnokoda...
            directory = input("Gimme path to the system journals' directory \n")
            if path.exists(directory):
                return directory
            else:
                print("This path doesn't exist")

    @classmethod
    def make_journ(cls, j_name, filename=None, directory=None, content=None):
        filenom = input('Gimme filename \n') if not filename else filename
        # filename = 'input.txt'
        if content is None:
            with open(filenom) as f:
                text = f.read()
        else:
            text = content

        # '2014-02-07 11:52:21'
        dt = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        pth = SysJournal._get_journ_dir() if not directory else directory

        nom = '{Path}{name} {date}.evtx'.format(
            Path=pth, name=j_name, date=dt)

        outp = open(nom, 'w')

        outp.write(text)
        outp.close()

        return SysJournal(nom)

    def divide(self):
        self.reg_name = path.split(self.full_path)[1]
        res = self.reg_name[:-5].split()
        self.name = res[0]
        self.date = res[1] + res[2]

    def chk_size(self, size):
        self.size = path.getsize(self.full_path)
        if self.size >= size:
            print('gotcha!')
            # self = SysJournal.make_journ(self.name,
            #                              directory=self.full_path[:-len(self.reg_name)],
            #                              filename=self.full_path,
            #                              content='')
            return SysJournal.make_journ(self.name,
                                         directory=self.full_path[:-len(self.reg_name)],
                                         filename=self.full_path,
                                         content='')
        else: return self

    def get(self):
        while True: #zapah govnokoda...
            pth = input('Gimme path to the journal \n')
            nom = path.split(pth)[1]
            if path.exists(pth) and \
                    ('.evtx' in nom):
                self.full_path = pth
                self.divide()

                return
            else:
                print("This path doesn't exist")

    def get_content(self):
        with open(self.full_path) as f:
            txt = f.read()
        return txt
