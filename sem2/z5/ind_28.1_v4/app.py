

from wsgiref.simple_server import make_server
from random import seed, randint

import cgi
import json


VICTORY_POINTS = 3
DRAW_POINTS = 1
DEFEAT_POINTS = 0

START_PAGE = "/home/olga/PyCharm/domashki/sem2/z5/ind_28.1_v4/index.html"
ADD_PAGE = "/home/olga/PyCharm/domashki/sem2/z5/ind_28.1_v4/add.html"
ERROR_PAGE = "/home/olga/PyCharm/domashki/sem2/z5/ind_28.1_v4/error.html"


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




class FootballApp:
    def __init__(self, teams_file, points_file, teams_key="teams",
                 games_key="games", points_key="points"):
        # json stuff
        self.json = points_file
        self._teams_key = teams_key
        self._games_key = games_key
        self._points_key = points_key

        # load teams
        with open(teams_file) as f:
            team_dict = json.load(f)
        self.teams = {name: Team(name) for name in team_dict[teams_key]}
        del team_dict

        # load and process games data
        with open(points_file) as f:
            point_dict = json.load(f)
        for game in point_dict[games_key]:
            self.teams[game[teams_key][0]].add_match(
                self.teams[game[teams_key][1]],
                game[points_key][0], game[points_key][1]
            )
        del point_dict

        # server stuff
        self.commands = {
            "":         self.start,
            "add":      self.add,
            "process":  self.process_bet
        }

    def __call__(self, environ, start_response):
        command = environ.get('PATH_INFO', '').lstrip('/')

        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        error = False
        if command in self.commands:
            body = self.commands[command](form)
            if body:
                start_response(
                    '200 OK', [('Content-Type', 'text/html; charset=utf-8')]
                )
            else:
                error = True
        else:
            error = True
        if error:
            start_response(
                '404 NOT FOUND', [('Content-type', 'text/plain')]
            )
            body = 'Daaafaaaquuu! 404 is here, dude.'

        return [bytes(body, encoding='utf-8')]

    def start(self, form):
        return self._format_resp(START_PAGE, [("result_table", self.result_table)])

    def add(self, form):
        return  self._format_resp(
            ADD_PAGE,
            [("team1_select", self.team_list),
             ("team2_select", self.team_list)]
        )

    def process_bet(self, form):
        err = False
        msg = ""

        tag_names = ["team1_name",
                     "team2_name",
                     "team1_points",
                     "team2_points"]

        if all(t in form for t in tag_names):
            team1 = form["team1_name"].value
            team2 = form["team2_name"].value
            if team1 == team2:
                err = True
                msg = "Tango is danced in pair. (c) L. Randall Wray <br> I mean, you should choose 2 different teams."
            else:
                points1 = int(form["team1_points"].value)
                points2 = int(form["team2_points"].value)

                # now we can finally process our match:

                # step 1 - process teams' progress
                self.teams[team1].add_match(
                    self.teams[team2],
                    points1, points2
                )

                # step 2 - save it to json
                self._commit_to_json(team1, team2, points1, points2)
        else:
            err = True
            msg = "Someting wrong with your form, sorry."

        if err:
            return self.error(msg)

        return self.start(None)

    def error(self, message, error_page=ERROR_PAGE):
        return  self._format_resp(error_page, [("err_message", message)])

    def _commit_to_json(self, team1, team2, points1, points2):
        f = open(self.json)
        cnt = json.load(f)
        f.close()

        game_list = cnt[self._games_key]
        game_list.append({
            self._teams_key:    [team1, team2],
            self._points_key:   [points1, points2]
        })
        cnt[self._games_key] = game_list

        f = open(self.json, 'w')
        json.dump(cnt, fp=f)
        f.close()

    def _format_resp(self, resp_file, arg_list):
        '''
        потому что ?)$#@$0 css со своими четырежды ?)$#@$0 фигурными скобками не может ?)$#@$0 не помешать
        :param resp:
        :param key:
        :param value: STRING!!!!
        :return:
        '''
        with open(resp_file) as f:
            lines = f.readlines()
        for (key, value) in arg_list:
            for j,line in enumerate(lines):
                """
                 чекаем на наличие фигурных скобок с параметром
                 с помощью регулярки мб
                 если да, форматируем строку
                 
                 после этого все строки тупо сливаем вместе
                 (надо глянуть, прописан ли там ньюлайн, или через него соединять. )
                 мб при считке не лайнсами, а считать и сплитануть через ньюлайны. 
                """
                keyword = "{"+key+"}"
                if keyword in line:
                    i = line.find(keyword)
                    lines[j] = line[:i] + value + line[i+len(keyword):]
        return ''.join(lines)

    # def _make_select_options(self, values):
    #     opt_pattern = '<option value="{v}">{v}</option>\n'
    #     return ''.join(
    #         [opt_pattern.format(v=value) for value in values]
    #     )

    def _get_winners(self):
        res = list(self.teams.keys())
        res.sort(reverse=True, key=lambda team: self.teams[team].finalPoint)
        return res

    @property
    def result_table(self):
        res = """
        <table>
            <tr>
                <th>Place</th>
                <th>Team</th>
                <th>Games</th>
                <th>Wins</th>
                <th>Draws</th>
                <th>Loses</th>
                <th>Goals scored</th>
                <th>Goals lost</th>
                <th>Total score</th>
            </tr>
        """

        col_pattern = "<th>{}</th>\n"

        f = self._get_winners()

        for place, team_name in enumerate(f):
            res += "<tr>\n"

            res += col_pattern.format(place + 1) # place
            res += col_pattern.format(team_name) # team
            res += col_pattern.format(           # games
                self.teams[team_name].games
            )
            res += col_pattern.format(           # wins
                self.teams[team_name].wins
            )
            res += col_pattern.format(           # draws
                self.teams[team_name].draws
            )
            res += col_pattern.format(           # loses
                self.teams[team_name].loses
            )
            res += col_pattern.format(           # scored goals
                self.teams[team_name].scoredGoals
            )
            res += col_pattern.format(           # lost goals
                self.teams[team_name].lostGoals
            )
            res += col_pattern.format(           # total points
                self.teams[team_name].points
            )

            res += "</tr>\n"

        res += "</table>\n"

        return res

    @property
    def team_list(self):
        opt_pattern = '<option value="{v}">{v}</option>\n'

        res = '<option value="Choose team" disabled>Choose team</option>\n'
        res += ''.join(
            [opt_pattern.format(v=team) for team in self.teams]

        )
        return res


if __name__ == "__main__":
    application = FootballApp(
        "/home/olga/PyCharm/domashki/sem2/z5/ind_28.1_v4/teams.json",
        "/home/olga/PyCharm/domashki/sem2/z5/ind_28.1_v4/points.json"
    )
    print("======= ШАХТА ЧЕМПИОН ========")

    server = make_server("localhost", 8888, application)
    server.serve_forever()
