#t26_32
# РљР»Р°СЃ РґР»СЏ Р·РјС–РЅРё РјРѕРІРё Р’С–РєС–РїРµРґС–С—

from tkinter import *

class LangOpts:
    '''РљР»Р°СЃ РґР»СЏ Р·РјС–РЅРё РјРѕРІРё.

       self.top - РІС–РєРЅРѕ РІРµСЂС…РЅСЊРѕРіРѕ СЂС–РІРЅСЏ Сѓ СЏРєРѕРјСѓ СЂРѕР·РјС–С‰РµРЅРѕ РµР»РµРјРµРЅС‚Рё
       self.cancel - С‡Рё Р±СѓР»Рѕ РЅР°С‚РёСЃРЅСѓС‚Рѕ РєРЅРѕРїРєСѓ "Р’С–РґРјС–РЅРёС‚Рё"
       self.langvar - Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· СЂР°РґС–РѕРєРЅРѕРїРєР°РјРё
       self.language - РјРѕРІР° Р’С–РєС–РїРµРґС–С— (СЃРїРѕС‡Р°С‚РєСѓ - РїРѕС‡Р°С‚РєРѕРІР° РјРѕРІР° init_lang)
    '''

    def __init__(self, master, init_lang='uk'):
        self.top = master
        self.cancel = False
        self.language = init_lang
        self._make_widgets()

    def _make_widgets(self):
        '''РЎС‚РІРѕСЂРёС‚Рё РµР»РµРјРµРЅС‚Рё РґР»СЏ Р·РјС–РЅРё РјРѕРІРё.
        '''
        # Р·Р°РіРѕР»РѕРІРѕРє РІС–РєРЅР°
        self.top.title('РњРѕРІР° Р’С–РєС–РїРµРґС–С—')
        # СЂР°РґС–РѕРєРЅРѕРїРєРё РјРѕРІРё
        languages = {'uk': 'РЈРєСЂР°С—РЅСЃСЊРєР°',
                     'en': 'РђРЅРіР»С–Р№СЃСЊРєР°',
                     'ru': 'Р РѕСЃС–Р№СЃСЊРєР°'}
        l_codes = ['uk', 'en', 'ru']  # РєРѕРґРё РјРѕРІ РґР»СЏ РІРїРѕСЂСЏРґРєСѓРІР°РЅРЅСЏ РєРЅРѕРїРѕРє
        self.langvar = StringVar() # Р·РјС–РЅРЅР°, РїРѕРІ'СЏР·Р°РЅР° Р· СЂР°РґС–РѕРєРЅРѕРїРєР°РјРё
        for lang in l_codes:
            Radiobutton(self.top, text=languages[lang],
                        variable=self.langvar,
                        value=lang).pack(anchor=NW)
        self.langvar.set(self.language) # СѓРІС–РјРєРЅСѓС‚Рё РєРЅРѕРїРєСѓ, С‰Рѕ РІС–РґРїРѕРІС–РґР°С”
                                        # РїРѕС‡Р°С‚РєРѕРІС–Р№ РјРѕРІС–

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
        self.top.destroy()   # Р·Р°РєСЂРёС‚Рё РІС–РєРЅРѕ self.top

    def cancel_handler(self, ev=None):
        '''РћР±СЂРѕР±РёС‚Рё РЅР°С‚РёСЃРЅРµРЅРЅСЏ РєРЅРѕРїРєРё "Р’С–РґРјС–РЅРёС‚Рё".'''
        # РІС–РґРјС–РЅРёС‚Рё
        self.cancel = True
        self.ok_handler(ev)

    def get(self):
        '''РџРѕРІРµСЂРЅСѓС‚Рё РјРѕРІСѓ.

           РЇРєС‰Рѕ РЅР°С‚РёСЃРЅСѓС‚Рѕ "РІС–РґРјС–РЅРёС‚Рё", С‚Рѕ РїРѕРІРµСЂС‚Р°С” None.
        '''
        if not self.cancel:
            # РѕС‚СЂРёРјР°С‚Рё Р·РЅР°С‡РµРЅРЅСЏ Р·РјС–РЅРЅРѕС—, РїРѕРІ'СЏР·Р°РЅРѕС— Р· РєРЅРѕРїРєР°РјРё
            lang = self.langvar.get()
        else:
            lang = None
        return lang


def main():
    '''Р¤СѓРЅРєС†С–СЏ РґР»СЏ С‚РµСЃС‚СѓРІР°РЅРЅСЏ.

       РџСЂР°С†СЋС”, РєРѕР»Рё РјРѕРґСѓР»СЊ С” РіРѕР»РѕРІРЅРёРј
    '''
    top = Tk()
    f = LangOpts(top)
    mainloop()
    print(f.get())


if __name__ == '__main__':
    main()
