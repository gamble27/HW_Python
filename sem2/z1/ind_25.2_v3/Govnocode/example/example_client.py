# t25_12 РљР»С–С”РЅС‚ РіСЂРё Сѓ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ СЃР»С–РІ
# РћС‚СЂРёРјСѓС” РІС–Рґ СЃРµСЂРІРµСЂР° РєРѕРјР°РЅРґРё С‚Р° СЂСЏРґРєРё РґР»СЏ РїРѕРєР°Р·Сѓ
# Р’С–РґРїСЂР°РІР»СЏС” РЅР° СЃРµСЂРІРµСЂ Р»С–С‚РµСЂРё Р°Р±Рѕ СЃР»РѕРІР°
# Р’РёРєРѕСЂРёСЃС‚РѕРІСѓС” С„Р°Р№Р»РѕРїРѕРґС–Р±РЅС– РѕР±'С”РєС‚Рё РґР»СЏ РѕР±РјС–РЅСѓ РґР°РЅРёРјРё


import socket

HOST = 'localhost'    # РљРѕРјРї'СЋС‚РµСЂ РґР»СЏ Р·'С”РґРЅР°РЅРЅСЏ Р· СЃРµСЂРІРµСЂРѕРј
PORT = 30003          # РџРѕСЂС‚ РґР»СЏ Р·'С”РґРЅР°РЅРЅСЏ Р· СЃРµСЂРІРµСЂРѕРј

class ServerError(Exception):
    "Р’РёРєР»СЋС‡РµРЅРЅСЏ Сѓ СЂР°Р·С– РѕС‚СЂРёРјР°РЅРЅСЏ РЅРµРїСЂР°РІРёР»СЊРЅРёС… РґР°РЅРёС… РІС–Рґ СЃРµСЂРІРµСЂР°."
    pass


class WordGuessClient:
    """РљР»Р°СЃ РєР»С–С”РЅС‚Р° РіСЂРё Сѓ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ СЃР»С–РІ."""

    def __init__(self, host, port, name):
        """Р’СЃС‚Р°РЅРѕРІРёС‚Рё Р·'С”РґРЅР°РЅРЅСЏ Р· СЃРµСЂРІРµСЂРѕРј."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # СЃС‚РІРѕСЂРёС‚Рё С„Р°Р№Р»РѕРїРѕРґС–Р±РЅС– РѕР±'С”РєС‚Рё РґР»СЏ РѕР±РјС–РЅСѓ РґР°РЅРёРјРё
        self.input = self.socket.makefile('rb', 0)
        self.output = self.socket.makefile('wb', 0)
        self.sendMessage(name)          # РЅР°РґС–СЃР»Р°С‚Рё С–Рј'СЏ РЅР° СЃРµСЂРІРµСЂ.
        self.run()                      # РІРµСЃС‚Рё РіСЂСѓ

    def run(self):
        """Р’РµРґРµ РіСЂСѓ, РїСЂРёР№РјР°С” С‚Р° РІС–РґРїСЂР°РІР»СЏС” РґР°РЅС–."""
        done = False
        # Р’РµСЃС‚Рё РіСЂСѓ
        while not done:
            try:
                done = self.processInput() # РѕР±СЂРѕР±РёС‚Рё РѕС‚СЂРёРјР°РЅС– РґР°РЅС–
            except ServerError as error:
                print(error)
                done = self.quitCommand()
            except socket.error as e:
                print(e)
                done = self.quitCommand()

    def sendMessage(self, message):
        """Р’С–РґРїСЂР°РІРёС‚Рё РїРѕРІС–РґРѕРјР»РµРЅРЅСЏ СЃРµСЂРІРµСЂСѓ."""
        self.output.write(bytes(message + '\r\n', encoding='utf-8'))

    def processInput(self):
        """Р§РёС‚Р°С” СЂСЏРґРѕРє С‚РµРєСЃС‚Сѓ РІС–Рґ СЃРµСЂРІРµСЂР° С‚Р° РѕР±СЂРѕР±Р»СЏС” РѕС‚СЂРёРјР°РЅСѓ РєРѕРјР°РЅРґСѓ.

           РЇРєС‰Рѕ СЂСЏРґРѕРє РЅРµ С” РєРѕРјР°РЅРґРѕСЋ, - РїРѕРєР°Р·СѓС” Р№РѕРіРѕ.
        """
        done = False
        line = self._readline()
        # РѕС‚СЂРёРјР°С‚Рё РєРѕРјР°РЅРґСѓ С‚Р° Р°СЂРіСѓРјРµРЅС‚Рё
        command, arg = self._parseCommand(line)
        if command:
            # РІРёРєР»РёРєР°С‚Рё РјРµС‚РѕРґ РґР»СЏ РІРёРєРѕРЅР°РЅРЅСЏ РєРѕРјР°РЅРґРё
            # С‚Р° РїРµСЂРµРґР°С‚Рё РїР°СЂР°РјРµС‚СЂРё, СЏРєС‰Рѕ С”
            if arg:
                done = command(arg)
            else:
                done = command()
        else:   # СЏРєС‰Рѕ РЅРµ РєРѕРјР°РЅРґР°, - РїСЂРѕСЃС‚Рѕ РїРѕРєР°Р·Р°С‚Рё СЂСЏРґРѕРє
            print(line)
        return done

    def turnCommand(self):
        """РљРѕРјР°РЅРґР° /turn (Р·СЂРѕР±РёС‚Рё С…С–Рґ)."""
        while True:
            m = input("1 - Р»С–С‚РµСЂР°, 2 - СЃР»РѕРІРѕ: ")[0]
            if m == '1' or m == '2': break
        if m == '1':                            #Р»С–С‚РµСЂР°
            c = input('Р»С–С‚РµСЂР°: ')[0]
            message = '/letter {}'.format(c)
        else:                                   #СЃР»РѕРІРѕ
            w = input('СЃР»РѕРІРѕ: ')
            message = '/word {}'.format(w)
        self.sendMessage(message)   # РІС–РґРїСЂР°РІРёС‚Рё РєРѕРјР°РЅРґСѓ С‚Р° РґР°РЅС– СЃРµСЂРІРµСЂСѓ
        return False

    def quitCommand(self):
        """РљРѕРјР°РЅРґР° /quit (Р·Р°РІРµСЂС€РёС‚Рё СЂРѕР±РѕС‚Сѓ)."""
        self.socket.shutdown(2)     # Р·Р°РєСЂРёС‚Рё "С„Р°Р№Р»Рё"
        self.socket.close()         # Р·Р°РєСЂРёС‚Рё Р·'С”РґРЅР°РЅРЅСЏ
        return True

    def _parseCommand(self, inp):
        """РќР°РјР°РіР°С”С‚СЊСЃСЏ СЂРѕР·С–Р±СЂР°С‚Рё СЂСЏРґРѕРє СЏРє РєРѕРјР°РЅРґСѓ РєР»С–С”РЅС‚Сѓ.

           РЇРєС‰Рѕ С†СЋ РєРѕРјР°РЅРґСѓ СЂРµР°Р»С–Р·РѕРІР°РЅРѕ, РІРёРєР»РёРєР°С” РІС–РґРїРѕРІС–РґРЅРёР№ РјРµС‚РѕРґ.
           РЇРєС‰Рѕ СЂСЏРґРѕРє РЅРµ С” РєРѕРјР°РЅРґРѕСЋ, - РїРѕРєР°Р·СѓС” Р№РѕРіРѕ.
        """
        commandMethod, arg = None, None
        # СЏРєС‰Рѕ СЂСЏРґРѕРє РЅРµРїРѕСЂРѕР¶РЅС–Р№ С‚Р° РїРѕС‡РёРЅР°С”С‚СЊСЃСЏ Р· '/'
        if inp and inp[0] == '/':
            if len(inp) < 2:
                raise ServerError('РќРµРґРѕРїСѓСЃС‚РёРјР° РєРѕРјР°РЅРґР°: "{}"'.format(inp))
            # СЃРїРёСЃРѕРє Р· 2 (Р°Р±Рѕ 1) Р·РЅР°С‡РµРЅСЊ: РєРѕРјР°РЅРґР° С‚Р° С—С— Р°СЂРіСѓРјРµРЅС‚Рё (СЏРєС‰Рѕ С”)
            commandAndArg = inp[1:].split(' ', 1)
            if len(commandAndArg) == 2: # С” Р°СЂРіСѓРјРµРЅС‚Рё
                command, arg = commandAndArg
            else:
                command, = commandAndArg # РЅРµРјР°С” Р°СЂРіСѓРјРµРЅС‚С–РІ
            # Р§Рё СЂРµР°Р»С–Р·РѕРІР°РЅРѕ Сѓ РєР»Р°СЃС– РјРµС‚РѕРґ, СЏРєРёР№ РїРѕС‡РёРЅР°С”С‚СЊСЃСЏ
            # С–Рј'СЏРј РєРѕРјР°РЅРґРё С‚Р° Р·Р°РІРµСЂС€СѓС”С‚СЊСЃСЏ 'Command'
            commandMethod = getattr(self, command + 'Command', None)
            if not commandMethod:
                raise ServerError('РќРµРјР°С” С‚Р°РєРѕС— РєРѕРјР°РЅРґРё: "{}"'.format(command))
        return commandMethod, arg

    def _readline(self):
        """Р§РёС‚Р°С” Р· РјРµСЂРµР¶С– СЂСЏРґРѕРє, РІРёРґР°Р»СЏС” РїСЂРѕРїСѓСЃРєРё Р· РїРѕС‡Р°С‚РєСѓ С‚Р° РєС–РЅС†СЏ."""
        line = str(self.input.readline().strip(), encoding='utf-8')
#        print(line)
        return line


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:              # СЏРєС‰Рѕ РЅРµ РІРёСЃС‚Р°С‡Р°С” РїР°СЂР°РјРµС‚СЂС–РІ, РІРІРµСЃС‚Рё
        host = HOST
        port = PORT
        name = input("Р’РІРµРґС–С‚СЊ С–Рј'СЏ: ")
    else:
        host = sys.argv[1]     # 1 РїР°СЂР°РјРµС‚СЂ
        port = sys.argv[2]     # 2 РїР°СЂР°РјРµС‚СЂ
        name = sys.argv[3]     # 3 РїР°СЂР°РјРµС‚СЂ

    wg = WordGuessClient(host, port, name)
