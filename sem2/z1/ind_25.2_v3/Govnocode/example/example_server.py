# t25_11 РЎРµСЂРІРµСЂ РіСЂРё Сѓ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ СЃР»С–РІ
# Р’РёРєРѕСЂРёСЃС‚Р°РЅРѕ РїСЂРёРєР»Р°Рґ PythonChatServer
# Р· РєРЅРёРіРё Beginning Python, Р°РІС‚РѕСЂРё Peter Norton, Alex Samuel,
# David Aitel С‚Р° С–РЅС€С–

import socketserver
import socket
import os
from example_lib import *
# from rlist import *

TURN = '/turn'   # РєРѕРјР°РЅРґР° "Р·СЂРѕР±РёС‚Рё С…С–Рґ"
QUIT = '/quit'   # РєРѕРјР°РЅРґР° "Р·Р°РІРµСЂС€РёС‚Рё"
NUM_TO_START = 3 # РєС–Р»СЊРєС–СЃС‚СЊ РіСЂР°РІС†С–РІ РґР»СЏ РїРѕС‡Р°С‚РєСѓ РіСЂРё

class ClientError(Exception):
    "Р’РёРєР»СЋС‡РµРЅРЅСЏ Сѓ СЂР°Р·С– РѕС‚СЂРёРјР°РЅРЅСЏ РЅРµРїСЂР°РІРёР»СЊРЅРёС… РґР°РЅРёС… РІС–Рґ РєР»С–С”РЅС‚Р°."
    pass


class NetGuesser(Guesser):
    """Р’С–РґРіР°РґСѓРІР°С‡ Сѓ РјРµСЂРµР¶С– """
    def __init__(self, name, wfile):
        Guesser.__init__(self, name)
        self.wfile = wfile # С„Р°Р№Р»РѕРїРѕРґС–Р±РЅРёР№ РѕР±'С”РєС‚ РґР»СЏ РїРµСЂРµРґР°С‡С– РґР°РЅРёС… Сѓ РјРµСЂРµР¶С–

    def __str__(self):
        return '{} {}'.format(self._name, self._points)


class WordGuessServer(socketserver.ThreadingTCPServer):
    "РљР»Р°СЃ Р±Р°РіР°С‚РѕРїРѕС‚РѕС‡РЅРѕРіРѕ TCP-СЃРµСЂРІРµСЂР°."

    def __init__(self, server_address, RequestHandlerClass):
        """РЎРµСЂРІРµСЂ, С‰Рѕ С–РґС‚СЂРёРјСѓС” РіСЂСѓ Сѓ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ СЃР»С–РІ."""
        socketserver.ThreadingTCPServer.__init__(self, server_address,
                                                    RequestHandlerClass)
        self.glist = Rlist()        # РєС–Р»СЊС†РµРІРёР№ СЃРїРёСЃРѕРє РіСЂР°РІС†С–РІ (РІС–РґРіР°РґСѓРІР°С‡С–РІ)
                                    # С‚РёРїСѓ NetGuesser
        self.num_guessers = 0       # РїРѕС‚РѕС‡РЅР° РєС–Р»СЊРєС–СЃС‚СЊ РіСЂР°РІС†С–РІ
        self.num_to_start = NUM_TO_START  # РєС–Р»СЊРєС–СЃС‚СЊ РіСЂР°РІС†С–РІ РґР»СЏ РїРѕС‡Р°С‚РєСѓ РіСЂРё
        self.game_on = False        # С‡Рё Р№РґРµ РіСЂР°
        self.word = ''              # СЃР»РѕРІРѕ РґР»СЏ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ
        self.guessed = ''           # СЃР»РѕРІРѕ,Р·Р°РїРѕРІРЅРµРЅРµ '*'


class RequestHandler(socketserver.StreamRequestHandler):
    """РљР»Р°СЃ РѕР±СЂРѕР±Р»СЏС” Р·Р°РїРёС‚Рё РѕРґРЅРѕРіРѕ РєР»С–С”РЅС‚Р°"""

    def handle(self):
        """РћР±СЂРѕР±Р»СЏС” Р·'С”РґРЅР°РЅРЅСЏ РѕРґРЅРѕРіРѕ РіСЂР°РІС†СЏ С‚Р° РїС–РґС‚СЂРёРјСѓС” Р№РѕРіРѕ СѓС‡Р°СЃС‚СЊ Сѓ РіСЂС–."""
        print('connected from', self.client_address)
        self.name = None    # С–Рј'СЏ РіСЂР°РІС†СЏ
        done = self.server.game_on # done - С‡Рё Р·Р°РІРµСЂС€РµРЅРѕ Р·'С”РґРЅР°РЅРЅСЏ
        if not done:
            name = self._readline()
            try:
                self.addGuesser(name)   # РґРѕРґР°С‚Рё РіСЂР°РІС†СЏ
                # СЏРєС‰Рѕ РіСЂР°РІС†С– Р·С–Р±СЂР°Р»РёСЃСЊ, С‚Рѕ РїРѕС‡Р°С‚Рё РіСЂСѓ
                if self.server.num_guessers >= self.server.num_to_start:
                    self.startGame()
            except ClientError as error:
                print(error)
                self.privateMessage(error.args[0])
                done = True
            except socket.error as e:
                print(e)
                done = True

        # Р’РµСЃС‚Рё РіСЂСѓ
        while not done:
            try:
                done = self.processInput() # РѕР±СЂРѕР±РёС‚Рё РѕС‚СЂРёРјР°РЅС– РґР°РЅС–
            except ClientError as error:
                self.privateMessage(str(error))
            except socket.error as e:
                done = True

    def finish(self):
        """РђРІС‚РѕРјР°С‚РёС‡РЅРѕ РІРёРєР»РёРєР°С”С‚СЊСЃСЏ РєРѕР»Рё Р·Р°РІРµСЂС€РµРЅРѕ РјРµС‚РѕРґ handle()."""
        if self.name:
            # Р“СЂР°РІРµС†СЊ СЂР°РЅС–С€Рµ СѓСЃРїС–С€РЅРѕ Р·'С”РґРЅР°РІСЃСЏ.
            # Р’РёРґР°Р»РёС‚Рё Р№РѕРіРѕ Р·С– СЃРїРёСЃРєСѓ РіСЂР°РІС†С–РІ
            for i in range(self.server.glist.len()):
                netguesser = self.server.glist.getcurrent()
                if netguesser.getname() == self.name:
                    self.server.glist.delete()
                    self.server.num_guessers -= 1
                else:
                    self.server.glist.next()
        # СЏРєС‰Рѕ РіСЂР°РІС†С–РІ РЅРµ Р·Р°Р»РёС€РёР»РѕСЃСЊ, РїРѕРЅРѕРІРёС‚Рё РіРѕС‚РѕРІРЅС–СЃС‚СЊ РґРѕ РіСЂРё
        if self.server.glist.len() == 0:
            self.server.game_on = False
        print('disconnected', self.client_address)
        # Р·Р°РІРµСЂС€РёС‚Рё Р·'С”РґРЅР°РЅРЅСЏ
        self.request.shutdown(2)
        self.request.close()


    def processInput(self):
        """Р§РёС‚Р°С” СЂСЏРґРѕРє С‚РµРєСЃС‚Сѓ С‚Р° РѕР±СЂРѕР±Р»СЏС” РѕС‚СЂРёРјР°РЅСѓ РєРѕРјР°РЅРґСѓ."""
        done = False
        line = self._readline()
        # РѕС‚СЂРёРјР°С‚Рё РєРѕРјР°РЅРґСѓ С‚Р° Р°СЂРіСѓРјРµРЅС‚Рё
        command, arg = self._parseCommand(line)
        if command:
            # РІРёРєР»РёРєР°С‚Рё РјРµС‚РѕРґ РґР»СЏ РІРёРєРѕРЅР°РЅРЅСЏ РєРѕРјР°РЅРґРё
            done = command(arg)
        else:
            raise ClientError('РќРµРѕС‡С–РєСѓРІР°РЅС– РґР°РЅС– РІС–Рґ РєР»С–С”РЅС‚Р° {}'.format(self.name))
        return done

    def addGuesser(self, name):
        """Р”РѕРґР°С” РЅРѕРІРѕРіРѕ РІС–РґРіР°РґСѓРІР°С‡Р° Р· С–Рј'СЏРј name."""
        if not name:
            raise ClientError('РќРµ РЅР°РґР°РЅРѕ С–РјРµРЅС– РіСЂР°РІС†СЏ.')
        self.name = name
        # РІСЃС‚Р°РІРёС‚Рё РіСЂР°РІС†СЏ Сѓ СЃРїРёСЃРѕРє
        self.server.glist.insert(NetGuesser(self.name, self.wfile))
        self.server.num_guessers += 1
        # РїРѕРІС–РґРѕРјРёС‚Рё РїСЂРѕ РїСЂРёС”РґРЅР°РЅРЅСЏ РіСЂР°РІС†СЏ
        self.broadcast('Р”Рѕ РіСЂРё РїСЂС”РґРЅР°РІСЃСЏ(Р»Р°СЃСЊ) {}'.format(self.name))

    def startGame(self):
        """РџРѕС‡РёРЅР°С” РіСЂСѓ."""
        self.server.game_on = True
        #С–Рј'СЏ С„Р°Р№Р»Сѓ Р·С– СЃР»РѕРІР°РјРё
        self.filename = os.pardir + '/' + os.pardir + '/' + \
                        'Lect_Python/T14/' + filename
        #РІРёР±СЂР°С‚Рё СЃР»РѕРІРѕ Р· С„Р°Р№Р»Сѓ РґР»СЏ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ
        word, guessed = makeword(self.filename)
#        print('word', word, 'guessed', guessed)
        self.server.word = word
        self.server.guessed = guessed
        # РїРѕРІС–РґРѕРјРёС‚Рё РїСЂРѕ РїРѕС‡Р°С‚РѕРє РіСЂРё С‚Р° СЃР»РѕРІРѕ
        self.broadcast('Р“СЂР° РїРѕС‡Р°Р»Р°СЃСЊ!')
        self.broadcast('РЎР»РѕРІРѕ: {}'.format(self.server.guessed))
        # РЅР°РґР°С‚Рё С…С–Рґ РїРµСЂС€РѕРјСѓ РіСЂР°РІС†СЋ
        self.nextTurn()

    def endGame(self):
        """Р—Р°РІРµСЂС€СѓС” РіСЂСѓ."""
        # РїРѕР±СѓРґСѓРІР°С‚Рё СЂСЏРґРѕРє СЂРµР·СѓР»СЊС‚Р°С‚С–РІ, СЂРѕР·РґС–Р»РµРЅРёР№ \n
        results = ''
        for i in range(self.server.glist.len()):
            netguesser = self.server.glist.getcurrent()
            self.server.glist.next()
            results = results + str(netguesser) + '\n'
        # РїРѕРІС–РґРѕРјРёС‚Рё РїСЂРѕ Р·Р°РєС–РЅС‡РµРЅРЅСЏ С‚Р° РїРѕРєР°Р·Р°С‚Рё СЂРµР·СѓР»СЊС‚Р°С‚Рё
        self.broadcast('Р“СЂСѓ Р·Р°РєС–РЅС‡РµРЅРѕ!')
        self.broadcast(results)
        # РЅР°РґС–СЃР»Р°С‚Рё РєР»С–С”РЅС‚Р°Рј РєРѕРјР°РЅРґСѓ Р·Р°РІРµСЂС€РµРЅРЅСЏ СЂРѕР±РѕС‚Рё
        self.broadcast(QUIT)

    def nextTurn(self):
        """РќР°РґР°С” РіСЂР°РІС†СЋ С…С–Рґ."""
        netguesser = self.server.glist.getcurrent()
        # РїРѕРІС–РґРѕРјР»СЏС” РІСЃС–С… РїСЂРѕ С‚Рµ, Сѓ РєРѕРіРѕ С…С–Рґ
        self.broadcast('РҐС–Рґ {}'.format(netguesser.getname()))
        # РЅР°РґСЃРёР»Р°С” РіСЂР°РІС†СЋ РєРѕРјР°РЅРґСѓ РїРѕС‚РѕС‡РЅРѕРіРѕ С…РѕРґСѓ (TURN)
        netguesser.wfile.write(bytes(self._ensureNewline(TURN),
                                     encoding='utf-8'))

    # Р РµР°Р»С–Р·Р°С†С–СЏ РєРѕРјР°РЅРґ СЃРµСЂРІРµСЂР°.

    def letterCommand(self, letter):
        """РљРѕРјР°РЅРґР° /letter (Р»С–С‚РµСЂР°)."""
        if letter in self.server.guessed: # Р»С–С‚РµСЂСѓ РІР¶Рµ РІС–РґРіР°РґР°РЅРѕ
            self.privateMessage('Р›С–С‚РµСЂСѓ РІР¶Рµ РІС–РґРіР°РґР°РЅРѕ')
            self.nextTurn() # РЅР°РґС–СЃР»Р°С‚Рё РєРѕРјР°РЅРґСѓ /turn
            done = False
        else:
            self.broadcast("РќР°Р·РІР°РЅРѕ Р»С–С‚РµСЂСѓ '{}'".format(letter), False)
            points = 0
            gw = ""
            #Р·Р°РјС–РЅСЋС”РјРѕ Сѓ guessed РІСЃС– '*" Сѓ РјС–СЃС†СЏС… РІС…РѕРґР¶РµРЅРЅСЏ letter РґРѕ word РЅР° letter
            for i in range(len(self.server.word)):
                if self.server.word[i] == letter:
                    gw = gw + letter    #РґРѕРїРёСЃСѓС”РјРѕ СЃРёРјРІРѕР» letter РґРѕ СЃР»РѕРІР° РІС–РґРіР°РґСѓРІР°РЅРЅСЏ
                    points += 1         #Р·Р±С–Р»СЊС€СѓС”РјРѕ Р±Р°Р»Рё РЅР° 1
                else:
                    #РґРѕРїРёСЃСѓС”РјРѕ С‚РѕР№ СЃРёРјРІРѕР» СЏРєРёР№ Р±СѓРІ Сѓ guessed
                    gw = gw + self.server.guessed[i]
            self.server.guessed = gw
            # РїРѕРІРµСЂРЅСѓС‚Рё СЂРµР·СѓР»СЊС‚Р°С‚ РѕР±СЂРѕР±РєРё Р±Р°Р»С–РІ (С‡Рё Р·Р°РєС–РЅС‡РµРЅРѕ РіСЂСѓ)
            done = self._processResults(points)
        return done

    def wordCommand(self, word):
        """РљРѕРјР°РЅРґР° /word (СЃР»РѕРІРѕ)."""
        self.broadcast('РќР°Р·РІР°РЅРѕ СЃР»РѕРІРѕ "{}"'.format(word), False)
        if word == self.server.word:  #СЃР»РѕРІРѕ РІС–РґРіР°РґР°РЅРѕ
            #РґРѕРґР°С”РјРѕ Р±Р°Р»С–РІ СЃС‚С–Р»СЊРєРё, СЃРєС–Р»СЊРєРё Р±СѓР»Рѕ *
            points = self.server.guessed.count('*')
            self.server.guessed = self.server.word
        else:                       #СЃР»РѕРІРѕ РЅРµ РІС–РґРіР°РґР°РЅРѕ
            points = -1             #-1 РѕР·РЅР°С‡Р°С”, С‰Рѕ С‚СЂРµР±Р° РѕС‡РёСЃС‚РёС‚Рё РІСЃС– Р±Р°Р»Рё
        # РїРѕРІРµСЂРЅСѓС‚Рё СЂРµР·СѓР»СЊС‚Р°С‚ РѕР±СЂРѕР±РєРё Р±Р°Р»С–РІ (С‡Рё Р·Р°РєС–РЅС‡РµРЅРѕ РіСЂСѓ)
        return self._processResults(points)

    def _processResults(self, points):
        """РћР±СЂРѕР±Р»СЏС” Р±Р°Р»Рё РіСЂР°РІС†СЏ points.

           Р’РёСЂС–С€СѓС”, С‡Рё Р·Р°РІРµСЂС€РµРЅРѕ РіСЂСѓ С‚Р° С‡Рё С‚СЂРµР±Р° РїРµСЂРµРґР°С‚Рё С…С–Рґ.
           РџРѕРІРµСЂС‚Р°С” Р·РЅР°С‡РµРЅРЅСЏ True/False: С‡Рё Р·Р°РєС–РЅС‡РµРЅРѕ РіСЂСѓ."""
        gameover = False    # С‡Рё Р·Р°РІРµСЂС€РµРЅРѕ РіСЂСѓ
        netguesser = self.server.glist.getcurrent() # РїРѕС‚РѕРЅРёР№ РіСЂР°РІРµС†СЊ
        if points > 0: # СЏРєС‰Рѕ Р±Р°Р»Рё Р·Р°СЂРѕР±Р»РµРЅРѕ
            netguesser.inc(points)
            self.privateMessage('Р’Рё Р·Р°СЂРѕР±РёР»Рё Р±Р°Р»С–РІ: {}'.format(points))
            gameover = not '*' in self.server.guessed
            if gameover:
                self.privateMessage('Р’С–С‚Р°С”РјРѕ! Р’Рё РІРёРіСЂР°Р»Рё!!!')
                #РїСЂРµРјС–СЏ Р·Р° РІС–РґРіР°РґСѓРІР°РЅРЅСЏ СЃР»РѕРІР°
                netguesser.inc(len(self.server.word))
        elif points < 0: # СЏРєС‰Рѕ РЅРµ РІС–РґРіР°РґР°РЅРѕ СЃР»РѕРІРѕ
            self.privateMessage('РќР° Р¶Р°Р»СЊ, Р’Р°С€С– Р±Р°Р»Рё "Р·РіРѕСЂС–Р»Рё"')
            netguesser.clear()
        else:                       #points == 0, РЅРµ РІС–РґРіР°РґР°РЅРѕ Р»С–С‚РµСЂСѓ
            self.privateMessage('РќРµРјР°С” С‚Р°РєРѕС— Р»С–С‚РµСЂРё')
        self.server.glist.update(netguesser)   #РѕРЅРѕРІРёС‚Рё РґР°РЅС– РіСЂР°РІС†СЏ Сѓ СЃРїРёСЃРєСѓ
        # РїРѕРєР°Р·Р°С‚Рё РІСЃС–Рј РѕРЅРѕРІР»РµРЅРµ СЃР»РѕРІРѕ РїС–СЃР»СЏ РІС–РґРіР°РґСѓРІР°РЅРЅСЏ
        self.broadcast('РЎР»РѕРІРѕ: {}'.format(self.server.guessed))
        if gameover:
            self.endGame()  # Р·Р°РІРµСЂС€РёС‚Рё РіСЂСѓ
        else:
            if points <= 0:
                # РїРµСЂРµРґР°С‚Рё С…С–Рґ РЅР°СЃС‚СѓРїРЅРѕРјСѓ РіСЂР°РІС†СЋ
                self.server.glist.next()
            self.nextTurn() # РЅР°РґС–СЃР»Р°С‚Рё РєРѕРјР°РЅРґСѓ /turn
        return gameover


    # Р”РѕРїРѕРјС–Р¶РЅС– РјРµС‚РѕРґРё.

    def broadcast(self, message, includeThisUser=True):
        """Р РѕР·С–СЃР»Р°С‚Рё РїРѕРІС–РґРѕРјР»РµРЅРЅСЏ message РІСЃС–Рј РєР»С–С”РЅС‚Р°Рј.

           РџРѕРІС–РґРѕРјР»РµРЅРЅСЏ РІС–РґРїРїСЂР°РІР»СЏС”С‚СЊСЃСЏ РІСЃС–Рј РїСЂРёС”РґРЅР°РЅРёРј РєР»С–С”РЅС‚Р°Рј,
           РѕРєСЂС–Рј, РјРѕР¶Р»РёРІРѕ, РїРѕС‚РѕС‡РЅРѕРіРѕ, С‰Рѕ РІСЃС‚Р°РЅРѕРІР»СЋС”С‚СЊСЃСЏ РїР°СЂР°РјРµС‚СЂРѕРј
           includeThisUser."""
        message = bytes(self._ensureNewline(message), encoding='utf-8')
        for i in range(self.server.glist.len()):
            netguesser = self.server.glist.getcurrent()
            self.server.glist.next()
            if includeThisUser or netguesser.getname() != self.name:
                netguesser.wfile.write(message)

    def privateMessage(self, message):
        """РќР°РґС–СЃР»Р°С‚Рё РїРѕРІС–РґРѕРјР»РµРЅРЅСЏ С‚С–Р»СЊРєРё РїРѕС‚РѕС‡РЅРѕРјСѓ РєР»С–С”РЅС‚Сѓ."""
        self.wfile.write(bytes(self._ensureNewline(message), encoding='utf-8'))

    def _readline(self):
        """Р§РёС‚Р°С” Р· РјРµСЂРµР¶С– СЂСЏРґРѕРє, РІРёРґР°Р»СЏС” РїСЂРѕРїСѓСЃРєРё Р· РїРѕС‡Р°С‚РєСѓ С‚Р° РєС–РЅС†СЏ."""
        line = str(self.rfile.readline().strip(), encoding='utf-8')
#        print(line)
        return line

    def _ensureNewline(self, s):
        """Р—Р°РїРµРІРЅСЏС”, С‰Рѕ СЂСЏРґРѕРє Р·Р°РІРµСЂС€СѓС”С‚СЊСЃСЏ СЃРёРјРІРѕР»РѕРј '\n'."""
        if s and s[-1] != '\n':
            s += '\n'
        return s

    def _parseCommand(self, inp):
        """РќР°РјР°РіР°С”С‚СЊСЃСЏ СЂРѕР·С–Р±СЂР°С‚Рё СЂСЏРґРѕРє СЏРє РєРѕРјР°РЅРґСѓ СЃРµСЂРІРµСЂСѓ.

           РЇРєС‰Рѕ С†СЋ РєРѕРјР°РЅРґСѓ СЂРµР°Р»С–Р·РѕРІР°РЅРѕ, РІРёРєР»РёРєР°С” РІС–РґРїРѕРІС–РґРЅРёР№ РјРµС‚РѕРґ.
        """
        commandMethod, arg = None, None
        # СЏРєС‰Рѕ СЂСЏРґРѕРє РЅРµРїРѕСЂРѕР¶РЅС–Р№ С‚Р° РїРѕС‡РёРЅР°С”С‚СЊСЃСЏ Р· '/'
        if inp and inp[0] == '/':
            if len(inp) < 2:
                raise ClientError('РќРµРґРѕРїСѓСЃС‚РёРјР° РєРѕРјР°РЅРґР°: "{}"'.format(inp))
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
                raise ClientError('РќРµРјР°С” С‚Р°РєРѕС— РєРѕРјР°РЅРґРё: "{}"'.format(command))
        return commandMethod, arg


HOST = ''                 # РљРѕРјРї'СЋС‚РµСЂ РґР»СЏ Р·'С”РґРЅР°РЅРЅСЏ
PORT = 30003              # РџРѕСЂС‚ РґР»СЏ Р·'С”РґРЅР°РЅРЅСЏ

if __name__ == '__main__':
    print('=== WordGuess server ===')
    # Р·Р°РїСѓСЃС‚РёС‚Рё СЃРµСЂРІРµСЂ
    WordGuessServer((HOST, PORT), RequestHandler).serve_forever()
