# t24_32
# РљР»Р°СЃ РґР»СЏ Р·РјС–РЅРё СЂРѕР·РјС–СЂСѓ С‚Р° РЅР°РїРёСЃР°РЅРЅСЏ С€СЂРёС„С‚Р°

from tkinter import *


class FontOpts:
    '''РљР»Р°СЃ РґР»СЏ Р·РјС–РЅРё СЂРѕР·РјС–СЂСѓ С‚Р° РЅР°РїРёСЃР°РЅРЅСЏ С€СЂРёС„С‚Р°.

       self.top - РІС–РєРЅРѕ РІРµСЂС…РЅСЊРѕРіРѕ СЂС–РІРЅСЏ Сѓ СЏРєРѕРјСѓ СЂРѕР·РјС–С‰РµРЅРѕ РµР»РµРјРµРЅС‚Рё
       self.cancel - С‡Рё Р±СѓР»Рѕ РЅР°С‚РёСЃРЅСѓС‚Рѕ РєРЅРѕРїРєСѓ "Р’С–РґРјС–РЅРёС‚Рё"
       self.sizevar - Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· СЂР°РґС–РѕРєРЅРѕРїРєР°РјРё
       self.boldvar - Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· 'РќР°РїС–РІРіСЂСѓР±РёР№'
       self.italicvar - Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· 'РќР°С…РёР»РµРЅРёР№'
    '''

    def __init__(self, master):
        self.top = master
        self.cancel = False
        self._make_widgets()

    def _make_widgets(self):
        '''РЎС‚РІРѕСЂРёС‚Рё РµР»РµРјРµРЅС‚Рё РґР»СЏ Р·РјС–РЅРё СЂРѕР·РјС–СЂСѓ С‚Р° РЅР°РїРёСЃР°РЅРЅСЏ С€СЂРёС„С‚Р°.
        '''
        # СЂР°РјРєР° С‚Р° СЂР°РґС–РѕРєРЅРѕРїРєРё СЂРѕР·РјС–СЂСѓ С€СЂРёС„С‚Р°
        fsizeopts = Frame(self.top)
        fsize = LabelFrame(fsizeopts, text='Р РѕР·РјС–СЂ С€СЂРёС„С‚Р°')
        sizes = [10, 12, 14, 16, 20]
        self.sizevar = IntVar()  # Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· СЂР°РґС–РѕРєРЅРѕРїРєР°РјРё
        for sz in sizes:
            s = str(sz)
            Radiobutton(fsize, text=s,
                        variable=self.sizevar,
                        value=sz).pack(anchor=NW)
        self.sizevar.set(sizes[0])  # СѓРІС–РјРєРЅСѓС‚Рё РєРЅРѕРїРєСѓ "10"
        fsize.pack(side=LEFT, fill=BOTH, expand=YES)

        # СЂР°РјРєР° С‚Р° РєРЅРѕРїРєРё РІРёР±РѕСЂСѓ РїР°СЂР°РјРµС‚СЂС–РІ С€СЂРёС„С‚Р°
        fopts = LabelFrame(fsizeopts, text='РќР°РїРёСЃР°РЅРЅСЏ')
        self.boldvar = IntVar()  # Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· 'РќР°РїС–РІРіСЂСѓР±РёР№'
        Checkbutton(fopts, text='РќР°РїС–РІРіСЂСѓР±РёР№',
                    variable=self.boldvar).pack(anchor=NW)
        self.italicvar = IntVar()  # Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· 'РќР°С…РёР»РµРЅРёР№'
        Checkbutton(fopts, text='РќР°С…РёР»РµРЅРёР№',
                    variable=self.italicvar).pack(anchor=NW)
        fopts.pack(side=LEFT, fill=BOTH, expand=YES)
        fsizeopts.pack(side=TOP, fill=BOTH, expand=YES)

        # СЂР°РјРєР° С‚Р° РєРЅРѕРїРєРё 'Ok' С‚Р° 'Р’С–РґРјС–РЅРёС‚Рё'
        fbut = Frame(self.top)
        bcancel = Button(fbut,
                         text='Р’С–РґРјС–РЅРёС‚Рё',
                         command=self.cancel_handler).pack(
            side=RIGHT, padx=5, pady=5)
        bok = Button(fbut, text='Ok',
                     command=self.ok_handler).pack(
            side=RIGHT, padx=5, pady=5)
        fbut.pack(side=TOP, fill=X, expand=YES)

    def ok_handler(self, ev=None):
        '''РћР±СЂРѕР±РёС‚Рё РЅР°С‚РёСЃРЅРµРЅРЅСЏ РєРЅРѕРїРєРё "Ok".'''
        self.top.destroy()  # Р·Р°РєСЂРёС‚Рё РІС–РєРЅРѕ self.top

    def cancel_handler(self, ev=None):
        '''РћР±СЂРѕР±РёС‚Рё РЅР°С‚РёСЃРЅРµРЅРЅСЏ РєРЅРѕРїРєРё "Р’С–РґРјС–РЅРёС‚Рё".'''
        # РІС–РґРјС–РЅРёС‚Рё
        self.cancel = True
        self.ok_handler(ev)

    def get(self):
        '''РџРѕРІРµСЂРЅСѓС‚Рё СЂРѕР·РјС–СЂ С‚Р° РЅР°РїРёСЃР°РЅРЅСЏ С€СЂРёС„С‚Р°.

           РЇРєС‰Рѕ РЅР°С‚РёСЃРЅСѓС‚Рѕ "РІС–РґРјС–РЅРёС‚Рё", С‚Рѕ РїРѕРІРµСЂС‚Р°С” (None, None).
        '''
        if not self.cancel:
            # РѕС‚СЂРёРјР°С‚Рё Р·РЅР°С‡РµРЅРЅСЏ Р·РјС–РЅРЅРёС…, РїРѕРІ'СЏР·Р°РЅРёС… Р· РєРЅРѕРїРєР°РјРё
            size = self.sizevar.get()
            bold = self.boldvar.get()
            italic = self.italicvar.get()
            if bold and italic:
                opts = "bold italic"
            elif bold:
                opts = "bold"
            elif italic:
                opts = "italic"
            else:
                opts = "normal"
        else:
            size = opts = None
        return size, opts


def main():
    '''Р¤СѓРЅРєС†С–СЏ РґР»СЏ С‚РµСЃС‚СѓРІР°РЅРЅСЏ.

       РџСЂР°С†СЋС”, РєРѕР»Рё РјРѕРґСѓР»СЊ С” РіРѕР»РѕРІРЅРёРј
    '''
    top = Tk()
    f = FontOpts(top)
    mainloop()
    print(f.get())


if __name__ == '__main__':
    main()