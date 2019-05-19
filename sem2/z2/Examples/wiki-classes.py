#t26_33
# РљР»Р°СЃ РґР»СЏ РїРµСЂРµРіР»СЏРґСѓ С‚РµРєСЃС‚РѕРІРёС… С„Р°Р№Р»С–РІ С‚Р° РїРѕРєР°Р·Сѓ РІРёР·РЅР°С‡РµРЅРЅСЏ Р· Р’С–РєС–РїРµРґС–С—

from tkinter import *
from tkinter.messagebox import *
from T24.t24_31_text_view import *
from t26_31_wiki_def import *
from t26_32_lang import *

class TextViewerWiki(TextViewer):
    '''РљР»Р°СЃ РґР»СЏ РїРµСЂРµРіР»СЏРґСѓ С‚РµРєСЃС‚РѕРІРёС… С„Р°Р№Р»С–РІ.

       Р”РѕРґР°РЅРѕ РјРѕР¶Р»РёРІС–СЃС‚СЊ Р·Р°РІР°РЅС‚Р°Р¶РёС‚Рё Р· Р’С–РєС–РїРµРґС–С— РѕР·РЅР°С‡РµРЅРЅСЏ СЃР»РѕРІР° С‡Рё С„СЂР°Р·Рё.
       self.language - РјРѕРІР° Р’С–РєС–РїРµРґС–С—
    '''
    def __init__(self, master, filename=None):
        TextViewer.__init__(self, master, filename)
        self.language = 'uk'


    def _make_widgets(self):
        '''РЎС‚РІРѕСЂРёС‚Рё РјРµРЅСЋ Р’С–РєС–.
        '''
        TextViewer._make_widgets(self)
        # СЃС‚РІРѕСЂРёС‚Рё РјРµРЅСЋ РІС–РєС–
        wikimenu = Menu(self.menubar, tearoff=0)
        wikimenu.add_command(label="Р’С–РєС–", command=self.displaywiki)
        wikimenu.add_command(label="РњРѕРІР°", command=self.setlanguage)
        self.menubar.add_cascade(label="Р’С–РєС–", menu=wikimenu)
        # РїРѕРєР°Р·Р°С‚Рё РјРµРЅСЋ
        self.top.config(menu=self.menubar)

    def displaywiki(self):
        '''РџРѕРєР°Р·Р°С‚Рё РѕР·РЅР°С‡РµРЅРЅСЏ РІРёР±СЂР°РЅРѕРіРѕ СЃР»РѕРІР° (СЃР»С–РІ).'''
        if self.text.tag_ranges(SEL): # СЏРєС‰Рѕ РІРёР±СЂР°РЅРѕ С‚РµРєСЃС‚
            # Р·Р°РїР°Рј'СЏС‚Р°С‚Рё РІРёР±С–СЂ
            selection = self.text.get(SEL_FIRST, SEL_LAST)
            selection = ' '.join(selection.split()) # РІРёРґР°Р»РёС‚Рё Р·Р°Р№РІС– РїСЂРѕРїСѓСЃРєРё
#            print(selection)
            if selection:
                # Р·Р°РїРёС‚Р°С‚Рё РѕР·РЅР°С‡РµРЅРЅСЏ РІС–РєС–
                wd = WikiDef(selection, self.language)
                definition = wd.definition # РѕС‚СЂРёРјР°С‚Рё СЂРµР·СѓР»СЊС‚Р°С‚ Р·Р°РїРёС‚Сѓ
                if definition:
                    showinfo(selection, definition)
                else:
                    showwarning(selection, 'РќРµ Р·РЅР°Р№РґРµРЅРѕ')


    def setlanguage(self):
        '''Р’СЃС‚Р°РЅРѕРІРёС‚Рё РјРѕРІСѓ Р’С–РєС–РїРµРґС–С—.'''
        dialog = Toplevel()
        lo = LangOpts(dialog, self.language)
        # Р·СЂРѕР±РёС‚Рё РґС–Р°Р»РѕРі РјРѕРґР°Р»СЊРЅРёРј
        dialog.focus_set()
        dialog.grab_set()
        dialog.wait_window()
        lang = lo.get()
        if lang:
            self.language = lang



def main():
    '''Р¤СѓРЅРєС†С–СЏ РґР»СЏ С‚РµСЃС‚СѓРІР°РЅРЅСЏ.

       РџСЂР°С†СЋС”, РєРѕР»Рё РјРѕРґСѓР»СЊ С” РіРѕР»РѕРІРЅРёРј
    '''
    top = Tk()
    t = TextViewerWiki(top)
    mainloop()

if __name__ == '__main__':
    main()
