from tkinter import *

from tkinter import messagebox

from PIL import ImageTk, Image

import multiprocessing

import time

import numpy as np

from problem_generator import *

MAX_STATS = (100,) * 2


class BattleGUI:

    def __init__(self, master, stats, inv, enemy_stats):

        self.master = master

        self.victory = False

        self._player_stats_form(stats, inv)

        self._enemy_stats_form(enemy_stats)

        self._window_set(self.master, 'Battle!', (400, 242))

        self._set_widgets()

    def loop(self):

        self.master.mainloop()

        print('=== Результат ===')

        if self.victory:

            print('Победа')

        else:

            print('Проигрыш')

    def _player_stats_form(self, max_hp_and_mp, inventory):

        self.stats = max_hp_and_mp

        self.inv = inventory

    def _show_results(self):

        if self.victory:

            messagebox.showinfo('Результат сражения',
                                'Игрок сразил противника {}!\nПобеда.'.format(self.enemy_name))

        else:

            messagebox.showinfo('Результат сражения',
                                'Игрок потерял сознание!\nПоражение.')

        self.master.destroy()

    def _enemy_stats_form(self, dct):

        self.enemy_name = dct['NAME']

        self.catchphrase = dct['CATCHPHRASE']

        self.enemy_curr_hp = self.enemy_max_hp = dct['MAXHP']

        self.enemy_atk, self.enemy_prob = dct['ATK'], dct['PROB']

        self.enemy_img = dct['IMG']

        self._enemy_tier = dct['TIER']

    def _check_player_numeric(self):

        if self.stats['HP'] <= 0:

            self._show_results()

        else:

            if self.stats['MP'] < 0:

                self.stats['MP'] = 0

    def _player_attack(self, damage):

        self.enemy_curr_hp -= damage

        self._enemy_attack(appendix='Герой наносит урон в {} ед.!'.format(damage))

        self._update_enemy_numeric()

    def _enemy_attack(self, appendix='', def_coefficient=None):

        d = 1

        if def_coefficient:

            d = def_coefficient

        if appendix:

            appendix += '\n\n'

        if self.enemy_curr_hp > 0:

            rand_coefficient = np.random.randint(0, 17)

            damage = int(d * 0.1 * rand_coefficient * self.enemy_atk)

            if np.random.binomial(1, self.enemy_prob):

                if not damage:

                    self._edit_text(appendix + '{} мало ел каши в детстве!'.format(self.enemy_name), True)

                else:

                    self.stats['HP'] -= damage

                    if rand_coefficient > 10:

                        self._edit_text(
                            appendix + '{} наносит коллосальный урон в {} ед. !'.format(self.enemy_name, damage), True)

                    else:

                        self._edit_text(appendix + '{} наносит урон в {} ед.'.format(self.enemy_name, damage), True)

            else:

                self._edit_text(appendix + '{} промахнулся!'.format(self.enemy_name), True)

            self._update_numeric()

            self._check_player_numeric()

        else:

            self.victory = True

            self._show_results()

    def _stats_w(self):

        stats_frame = Frame(self.master, relief=SUNKEN, bd=2)

        stats_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=EW)

        Label(stats_frame, text='HP:', fg='red').grid(row=0, column=0, sticky=E)

        self.lbl_hp = Label(stats_frame)

        self.lbl_hp.grid(row=0, column=1, columnspan=2, sticky=W)

        Label(stats_frame, text='MP:', fg='blue').grid(row=1, column=0, sticky=E)

        self.lbl_mp = Label(stats_frame)

        self.lbl_mp.grid(row=1, column=1, columnspan=2, sticky=W)

        self._update_enemy_numeric()

        self._update_numeric()

    def _act_w(self):

        action_frame = Frame(self.master, relief=SUNKEN, bd=2)

        action_frame.grid(row=2, column=0, rowspan=3, columnspan=2, sticky=EW)

        self.button_attack = Button(action_frame, text='Атаковать', command=self._on_ev_atk_b)

        self.button_attack.grid(row=0, columnspan=3, sticky=EW, padx=20)

        self.button_defend = Button(action_frame, text='Оборониться', command=self._on_ev_def_b)

        self.button_defend.grid(row=1, columnspan=2, sticky=EW, padx=20)

        self.button_inv = Button(action_frame, text='Инвентарь', command=self._on_ev_inv_b)

        self.button_inv.grid(row=2, columnspan=2, sticky=EW, padx=20)

    def _list_w(self):

        info_frame = Frame(self.master, relief=SUNKEN, bd=2)

        info_frame.grid(row=5, column=0, rowspan=3, columnspan=2)

        self.info_listbox = Listbox(info_frame, height=5, width=20, state=DISABLED)

        self.info_listbox.grid(row=0, sticky=EW)

        self.info_listbox.config(state=NORMAL)

        # TODO: В метод

        for item in self.inv:

            if self.inv[item] is not None:

                self.info_listbox.insert(END, self.inv[item]['NAME'])

        self.info_listbox.config(state=DISABLED)

        self.info_listbox.bind('<<ListboxSelect>>', self._selected_lstbox_inv)

        self.info_listbox.bind('<Double-Button>', self._on_clicked_item_ev)

    def _info_w(self):

        info_frame = Frame(self.master, relief=SUNKEN, bd=2)

        info_frame.grid(row=5, column=2, rowspan=3, columnspan=4)

        scrollbar = Scrollbar(info_frame)

        scrollbar.grid(row=0, column=6, sticky=NS)

        self.info_text = Text(info_frame, font=('Arial', 10), height=5, width=30,
                              wrap=WORD, state=DISABLED, yscrollcommand=scrollbar.set)

        self.info_text.grid(row=0, columnspan=6, sticky=NSEW)

        self._edit_text(self.catchphrase[np.random.randint(0, len(self.catchphrase) - 1)],
                        appendix='Начинается поединок между героем и противником {}!'.format(self.enemy_name))

        scrollbar.config(command=self.info_text.yview)

    def _image_w(self):

        img_frame = Frame(self.master, relief=SUNKEN, bd=2)

        img_frame.grid(row=0, column=2, rowspan=3, columnspan=5)

        pic = Image.open(self.enemy_img)

        img = ImageTk.PhotoImage(pic)

        self.panel = Label(img_frame, image=img)

        self.panel.image = img

        self.panel.grid(row=0, column=1, sticky=EW)

    def _edit_text(self, string, bold=None, appendix=''):

        if appendix:

            appendix += '\n\n'

        self.info_text.config(state=NORMAL)

        self.info_text.delete('1.0', END)

        self.info_text.insert(END, appendix + string)

        if bold:

            self.info_text.config(font=('Arial', 10, 'bold'))

        else:

            self.info_text.config(font=('Arial', 10))

        self.info_text.config(state=DISABLED)

    def _update_listbox(self):

        self.info_listbox.config(state=NORMAL)

        self.info_listbox.delete(0, END)

        for item in self.inv:

            if self.inv[item] is not None:

                self.info_listbox.insert(END, self.inv[item]['NAME'])

        self.info_listbox.config(state=DISABLED)

    def _update_stats(self):

        self._update_numeric()

        self._update_listbox()

    def _update_numeric(self):

        self.lbl_hp.config(text='{} | {}'.format(self.stats['HP'], MAX_STATS[0]))

        self.lbl_mp.config(text='{} | {}'.format(self.stats['MP'], MAX_STATS[-1]))

    def _update_enemy_numeric(self):

        self.master.title('Противник: {} | HP: {} / {}'.format(self.enemy_name, self.enemy_curr_hp, self.enemy_max_hp))

    def _selected_lstbox_inv(self, ev=None):

        self._edit_text(self.inv[list(self.inv.keys())[self.info_listbox.curselection()[0]]]['INFO'])

    def _timer_active(self):  # FIXME: ХУИКСМИ

        MAX_TIME = 10  # TODO: Подойти реальнее к проблеме, разобраться

        while True:

            self.attack_window.title('Атака | Оставшееся время: {} сек.'.format(MAX_TIME))

            MAX_TIME -= 1

            time.sleep(1)

    def _on_closing_atk(self):

        print('atk_invoke')

        res = self.entry.get()

        if res:

            try:
                res = list(map(float, res.split(' ')))

            except ValueError:

                self._enemy_attack(appendix='Пользователь оказался слепым, чтобы набрать правильный ответ.'.format())

            else:

                if res == self._task[1]:

                    dmg = np.random.randint(0, 4) + 10

                    self._player_attack(dmg)

                else:

                    self._enemy_attack(appendix='Герой слишком косой, чтобы попать по врагу..'.format())

        else:

            self._enemy_attack(appendix='Герой слишком косой, чтобы попать по врагу..'.format())

        self.attack_window.destroy()

    def _on_closing_def(self):

        print('def_invoke')

        res = self.entry.get()

        if res:

            try:
                res = list(map(float, res.split(' ')))

            except ValueError:

                self._enemy_attack(appendix='Герой упустил свой шанс оборониться,'
                                            ' ибо неправильные заклинания применяет..'.format())

            else:

                if res == self._task[1]:

                    mana_power = np.random.randint(0, 4)

                    self.stats['MP'] += mana_power

                    self._enemy_attack(appendix='Герой оборонился и повысил запасы маны на {} ед.!'.format(mana_power),
                                       def_coefficient=(mana_power * 1.5) * 0.1)

                else:

                    self._enemy_attack(appendix='Герой упустил свой шанс оборониться,'
                                                ' ибо что-то неправильное прошептал себе под нос..'.format())

        else:

            self._enemy_attack(appendix='Герой упустил свой шанс оборониться..'.format())

        self.defense_window.destroy()

    def _on_ev_atk_b(self):

        self.attack_window = Toplevel(self.master)  # TODO: Если открыто, блокировать виджеты главного!

        self.attack_window.title('Хрен вам, а не таймер.')

        self._window_set(self.attack_window, 'Атака', (228, 264))

        self._task = ProblemGenerator(self._enemy_tier).get_task

        print(self._task[1], 'ans')

        scrollbar = Scrollbar(self.attack_window)

        scrollbar.grid(row=0, column=4, sticky=NS)

        self.text_box = Text(self.attack_window, width=26, height=12,
                             wrap=WORD, state=DISABLED, yscrollcommand=scrollbar.set)

        self.text_box.grid(row=0, column=0, sticky=EW)

        self.text_box.config(state=NORMAL)

        self.text_box.insert('1.0', self._task[0])

        self.text_box.config(state=DISABLED)

        self.entry = Entry(self.attack_window)

        self.entry.grid(row=1, columnspan=8)

        Button(self.attack_window, text='Ответить', command=self._on_closing_atk).grid(row=2,
                                                                                           columnspan=8,
                                                                                           sticky=EW)

        self.attack_window.protocol("WM_DELETE_WINDOW", self._on_closing_atk)

    def _on_ev_def_b(self):

        self.defense_window = Toplevel(self.master)

        self.defense_window.title('Хрен вам, а не таймер.')

        self._window_set(self.defense_window, 'Оборона', (228, 264))

        self._task = ProblemGenerator(self._enemy_tier + 1).get_task

        print(self._task[1], 'ans')

        scrollbar = Scrollbar(self.defense_window)

        scrollbar.grid(row=0, column=4, sticky=NS)

        self.text_box = Text(self.defense_window, width=26, height=12,
                             wrap=WORD, state=DISABLED, yscrollcommand=scrollbar.set)

        self.text_box.grid(row=0, column=0, sticky=EW)

        self.text_box.config(state=NORMAL)

        self.text_box.insert('1.0', self._task[0])

        self.text_box.config(state=DISABLED)

        self.entry = Entry(self.defense_window)

        self.entry.grid(row=1, columnspan=8)

        Button(self.defense_window, text='Ответить', command=self._on_closing_def).grid(row=2,
                                                                                           columnspan=8,
                                                                                           sticky=EW)

        self.defense_window.protocol("WM_DELETE_WINDOW", self._on_closing_def)

    def _on_ev_inv_b(self, ev=None):

        # print(self.inv)

        if self.info_listbox['state'] == DISABLED:

            self._edit_text('Выберите предмет', True)

            self.info_listbox.config(state=NORMAL)

        else:

            self.info_listbox.config(state=DISABLED)

            self._edit_text(self.catchphrase[np.random.randint(0, len(self.catchphrase) - 1)])

    def _on_clicked_item_ev(self, ev=None):

        if self.info_listbox['state'] == NORMAL:

            # print(list(self.inv.keys()))

            item = list(self.inv.keys())[self.info_listbox.curselection()[0]]

            item_name = self.inv[item]['NAME'].lower()

            if self.inv[item]['USE']:

                self.stats['HP'] += self.inv[item]['HP']

                self.stats['MP'] += self.inv[item]['MP']

                lst = list(self.stats.keys())

                for i, stat in enumerate(lst):

                    if self.stats[stat] > MAX_STATS[i]:

                        self.stats[stat] = MAX_STATS[i]

                del self.inv[item]

                self._update_stats()

                self._enemy_attack(appendix='Использован предмет {}'.format(item_name))

            else:

                self._edit_text('Предмет {} нельзя использовать в бою!'.format(item_name), True)

    def _set_widgets(self):

        self._stats_w()

        self._act_w()

        self._list_w()

        self._info_w()

        self._image_w()

    def _window_set(self, window, string, w_h):

        window.resizable(False, False)

        window.geometry('%ix%i' % w_h)

        window.grid_propagate(0)

        window.title(string)


if __name__ == '__main__':

    PLAYER_STATS = {'HP': 100, 'MP': 0}

    PLAYER_INV = {'1': {'NAME': 'Камасутра',
                        'HP': 0,
                        'MP': 25,
                        'USE': True,
                        'INFO': 'Просвещает и прибавляет 25 ед. маны.'},
                  '2': {'NAME': 'Молоко',
                        'HP': 50, 'MP': 0,
                        'USE': True,
                        'INFO': 'Амброзия кузена. Прибавляет 50 ед. здоровья'},
                  '3': {'NAME': 'Таумономикон',
                        'HP': 0, 'MP': 0,
                        'USE': False,
                        'INFO': 'Никому не доверяй'},
                  '4': {'NAME': 'Манговый нектар',
                        'HP': 25, 'MP': 45,
                        'USE': True,
                        'INFO': 'Не злоупотребляйте.\n+45 MP; +25 HP'},
                  '5': {'NAME': 'Виски',
                        'HP': -45, 'MP': 0,
                        'USE': True,
                        'INFO': 'Вредит здоровью.\n-30 HP'}}

    ENEMY_CATCHPHRASE = ['Жареных гвоздей не желаешь отведать?',
                         'Бубубу, я пингвин',
                         'Все сражаются, а ты говнокодишь',
                         """Вот она — та самая Цитадель, где когда-то кузены рассуждали о грандиозных планах, что
вскоре воплотили в реальности. С Цитаделью связана вся история завязки первородных
нитей: её формировали те, кто умел разделять идеи Архимага; приводили до окончательной
точки разными способами. Это место станет обратным отсчётом для мучительных
ментальных страданий молочного юноши."""]

    ENEMY_QUIZ = [['', ''],
                  ['', ''],
                  ['', ''],
                  ['', ''],
                  ['', '']]  # Блок финальных вопросов

    ENEMY_STATS = {'NAME': 'Пингвин',
                   'IMG': '/home/olga/PyCharm/domashki/sem2/z6/examples/dans_proj/background_angry_penguin.gif',
                   'TIER': 1,
                   'CATCHPHRASE': ENEMY_CATCHPHRASE,
                   'MAXHP': 100,
                   'ATK': 25,
                   'PROB': 0.9,
                   'TASKS': ENEMY_QUIZ}

    top = Tk()

    BattleGUI(top, PLAYER_STATS, PLAYER_INV, ENEMY_STATS).loop()
