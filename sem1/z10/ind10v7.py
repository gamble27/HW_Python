from tkinter import *
from random import seed, randint

VICTORY_POINTS = 3
DRAW_POINTS = 1
DEFEAT_POINTS = 0


class Team:
    def __init__(self, name):
        self.name = name

        self.games = 0

        self.wins = 0
        self.draws = 0
        self.loses = 0

        self.points = 0

        self.scoredGoals = 0
        self.lostGoals = 0

        self.scoreDifference = 0

        self.finalPoint = 0

    def add_match(self, team, scored, lost):
        if scored > lost:  # victory
            self.wins += 1
            self.points += VICTORY_POINTS

            team.loses += 1
            team.points += DEFEAT_POINTS
        elif scored == lost:  # draw
            self.points += DRAW_POINTS
            self.draws += 1

            team.draws += 1
            team.points += DRAW_POINTS
        else:  # defeat
            team.wins += 1
            team.points += VICTORY_POINTS

            self.loses += 1
            self.points += DEFEAT_POINTS

        self.games += 1
        team.games += 1

        self.scoredGoals += scored
        self.lostGoals += lost
        team.scoredGoals += lost
        team.lostGoals += scored

        self.scoreDifference = self.scoredGoals - self.lostGoals
        team.scoreDifference = team.scoredGoals - team.lostGoals

        self._upd_final()
        team._upd_final()

    def _upd_final(self):
        seed()
        self.finalPoint = (1000*self.points+
                           100*self.scoreDifference+
                           10*self.scoredGoals+ randint(1, 10))


class Task:
    def __init__(self, teamlist_file, results_file):
        with open(teamlist_file) as f:
            words = f.read().split()
            self.teams = {word:  Team(word) for word in words if word!='\n'}

        with open(results_file) as f:
            results = f.readlines()
            for line in results:
                x = line.split()
                if (x[0] in self.teams) and (x[1] in self.teams):
                    self.teams[x[0]].add_match(self.teams[x[1]],
                                               int(x[2]), int(x[3]))

        self.__init_GUI()

    def __init_GUI(self):
        self.mainWindow = Tk()
        self.addWindow = None

        self.addMenu = Menu(self.mainWindow, tearoff=0)
        self.addMenu.add_command(label='Add result', command=self.add_res_btn_press)
        # self.addMenu.add_separator()
        self.mainWindow.config(menu=self.addMenu)

        rows = len(self.teams) + 1
        self.captions = ['Place', 'Team', 'Games',
                    'Wins', 'Draws', 'Loses',
                    'Goals scored', 'Goals lost',
                    'Total Score']
        columns = len(self.captions)

        places = self.get_winners()

        self.labels = [[Label(self.mainWindow, text=self.captions[i]).grid(row=0, column=i)
                        for i in range(len(self.captions))]]
        # ToDo: doit!!!
        self.labels += [[Label(self.mainWindow,text=str(i+1)).grid(row=i+1, column=0),  # place
                         Label(self.mainWindow, text=t).grid(row=i+1, column=1),  # team
                         Label(self.mainWindow, text=str(self.teams[t].games)).grid(row=i+1, column=2),  # games
                         Label(self.mainWindow, text=str(self.teams[t].wins)).grid(row=i + 1, column=3),  # wins
                         Label(self.mainWindow, text=str(self.teams[t].draws)).grid(row=i + 1, column=4),  # draws
                         Label(self.mainWindow, text=str(self.teams[t].loses)).grid(row=i + 1, column=5),  # loses
                         Label(self.mainWindow, text=str(self.teams[t].scoredGoals)).grid(row=i + 1, column=6),  # Goals scored
                         Label(self.mainWindow, text=str(self.teams[t].lostGoals)).grid(row=i + 1, column=7),  # goals lost
                         Label(self.mainWindow, text=str(self.teams[t].points)).grid(row=i + 1, column=8),  # total
                         ]
                        for i, t in enumerate(places)]

    def add_res_btn_press(self):
        self.addWindow = Toplevel(self.mainWindow)

        self.t1 = Spinbox(self.addWindow, values=list(self.teams.keys()))
        self.t1.grid(row=0, column=0)

        self.t2 = Spinbox(self.addWindow, values=list(self.teams.keys()))
        self.t2.grid(row=0, column=1)

        self.s1 = Spinbox(self.addWindow, from_=0, to=20)
        self.s1.grid(row=1, column=0)

        self.s2 = Spinbox(self.addWindow, from_=0, to=20)
        self.s2.grid(row=1, column=1)
        self.cancel_btn = Button(self.addWindow, text='Cancel', command=self.addWindow.withdraw)
        self.cancel_btn.grid(row=3, column=0)
        self.add_btn = Button(self.addWindow, text='Add', command=self.add_btn_press)
        self.add_btn.grid(row=3, column=1)

    def add_btn_press(self):
        team1 = self.t1.get()
        team2 = self.t2.get()
        if team1 != team2:
            self.teams[self.t1.get()].add_match(self.teams[self.t2.get()],
                                               int(self.s1.get()),
                                               int(self.s2.get()))
            self.addWindow.withdraw()
            self.__config_GUI()


#################################GOVNOKOD
    def __config_GUI(self):
        for i in self.labels:
            for label in i:
                del label

        # self.mainWindow

        places = self.get_winners()

        self.labels = [[Label(self.mainWindow, text=self.captions[i]).grid(row=0, column=i)
                        for i in range(len(self.captions))]]

        self.labels += [[Label(self.mainWindow, text=str(i + 1)).grid(row=i + 1, column=0),  # place
                         Label(self.mainWindow, text=t).grid(row=i + 1, column=1),  # team
                         Label(self.mainWindow, text=str(self.teams[t].games)).grid(row=i + 1, column=2),  # games
                         Label(self.mainWindow, text=str(self.teams[t].wins)).grid(row=i + 1, column=3),  # wins
                         Label(self.mainWindow, text=str(self.teams[t].draws)).grid(row=i + 1, column=4),  # draws
                         Label(self.mainWindow, text=str(self.teams[t].loses)).grid(row=i + 1, column=5),  # loses
                         Label(self.mainWindow, text=str(self.teams[t].scoredGoals)).grid(row=i + 1, column=6),
                         # Goals scored
                         Label(self.mainWindow, text=str(self.teams[t].lostGoals)).grid(row=i + 1, column=7),
                         # goals lost
                         Label(self.mainWindow, text=str(self.teams[t].points)).grid(row=i + 1, column=8),  # total
                         ]
                        for i, t in enumerate(places)]

    def get_winners(self):
        res = list(self.teams.keys())
        res.sort(reverse=True, key=lambda team: self.teams[team].finalPoint)
        return res

    def run(self):
        self.mainWindow.mainloop()

if __name__ == '__main__':
    task = Task('teams.txt', 'points.txt')
    task.run()
