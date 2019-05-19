#t27_41_wsgi_quiz_application.py
#? ?µ?°?»?–?·?°?†?–?? ???????…?????¶?µ?????? ?‚?µ???‚?–?? ?‡?µ???µ?· wsgi.

import cgi
import os
from t27_22_testio import *


HTML_WRONG_PASS = """

<p align=center>
	<font size="4" color="red">

		???µ?????°?????»?????? ?»?????–??/???°?????»??. ???????‚?????–?‚?? ?????µ???µ??????
	</font>
</p>
"""


HTML_THEME = """
<tr>
        <td>
                <input type=radio name=theme value="{0}">
        </td>
        <td align=left> 
                <font size="4">
                        {1}
                </font>
        </td>

"""

HTML_CHECK = """
<tr>
        <td>
                <input type=checkbox name=answer value="{0}">
        </td>
        <td align=left> 
                <font size="4">
                        {1}
                </font>
        </td>

"""


HTML_RADIO = """
<tr>
        <td>
                <input type=radio name=answer value="{0}">
        </td>
        <td align=left> 
                <font size="4">
                        {1}
                </font>
        </td>

"""


URN = "quizsuite1.xlsx"
LOGIN_HTML_FILE = "../w_quiz_login.html"
THEMES_HTML_FILE = "../w_quiz_themes.html"
QUEST_HTML_FILE = "../w_quiz_question.html"
RESULT_HTML_FILE = "../quiz_result.html"


class QuizSession:
    "???»?°?? ???µ?°?»?–?·???” ???????? ???µ???–?? ???????…?????¶?µ?????? ?‚?µ???‚?–??."
    def __init__(self, app, sid, user):
        self.app = app      # ???»?°??, ?‰?? ???–???‚???‚?? ???°?????? (QuizApplication)
        self.sid = sid      # ???????µ?? ???µ???–?—
        self.user = user    # ???????????‚?????°?‡, ???????? ???????…???????‚?? ?‚?µ???‚
        self.replies = []   # ???????????? ???????????–?? ???°???°?????… ???–?????????–???µ??
        self.quest_no = 0   # ???????µ?? ?????‚?°??????
        self.theme = ""     # ?‚?µ???° ?‚?µ???‚??
        self.quiz = None    # ?‚?µ???‚


class QuizApplication:
    """???»?°?? ???µ?°?»?–?·???” ???·?°?”???????–?? ?· ???»?–?”???‚???? ???–?? ?‡?°?? ???????…?????¶?µ?????? ?‚?µ???‚?–??.

        self.last_id - ???????µ?? ?????‚?°?????????— ?·?°?????‡?°?‚???????°?????— ???µ???–?—
        self.sessions - ???»?????????? ???µ???–?? (???±'?”???‚?–?? ???»?°???? QuizSession)
        self.suite - ???°?±?–?? ?‚?µ???‚?–??
        self.commands - ???»?????????? ???????°???? ?· HTML-?„?°???»?–?? ?‚?° ?„???????†?–?? ?—?… ???±?????±????
    """

    def __init__(self, test_io_cls, urn, path, **params):
        self.path = path + os.sep
        self.last_id = 0
        self.sessions = {}
        self.suite = QuizSuite(test_io_cls, urn, **params)
        self.commands = {"": self.start,
                         "login": self.login,
                         "theme": self.theme,
                         "question": self.question}

    def __call__(self, environ, start_response):
        """?’?????»?????°?”?‚?????? WSGI-???µ?????µ??????.

           ???‚?????????” ???‚???‡?µ?????? environ ?‚?° ?„???????†?–??,
           ?????? ?‚???µ?±?° ???????»?????°?‚?? ?? ???–?????????–????: start_response.
           ???????µ???‚?°?” ???–?????????–????, ?????° ???µ???µ???°?”?‚?????? ???»?–?”???‚??.
        """
        command = environ.get('PATH_INFO', '').lstrip('/')
        # ???‚???????°?‚?? ???»?????????? ???°???°???µ?‚???–??, ???µ???µ???°?????… ?· HTTP-?·?°?????‚??
        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                        environ=environ)
        err = False
        if command in self.commands:
            # ???????????°?‚?? ???????°?????? ?‚?° ???‚???????°?‚?? ?‚?–?»?? ???–?????????–???–
            body = self.commands[command](form)
            if body:
                start_response('200 OK', [('Content-Type',
                                           'text/html; charset=utf-8')])
            else:
                # ?????‰?? body - ?????????¶???–?? ??????????, ?‚?? ???????????»?° ?????????»???°
                err = True
        else:
            # ?????‰?? ???????°?????° ???µ???–???????°, ?‚?? ???????????»?° ?????????»???°
            err = True
        if err:
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            body = '???‚?????–?????? ???µ ?·???°?????µ????'
        return [bytes(body, encoding='utf-8')]

    def start(self, form):
        """???±?????±???‚?? ???????°?????? ?????‡?°?‚???? ?????±???‚?? (/).

           ???????????????°?‚?? ???»?–?”???‚?? ???‚?????–?????? ???…?????? ???? ???????‚?µ????.
        """
        with open(self.path + LOGIN_HTML_FILE, encoding='utf-8') as f:
            # ???????‡???‚?°?‚?? ???–???????‚?????»?µ?????? html-?„?°???»
            cnt = f.read()
        return cnt


    def login(self, form):
        """???±?????±???‚?? ???????°?????? ???…?????? ???? ???????‚?µ???? (/login).

           ???????????????°?‚?? ???»?–?”???‚?? ???‚?????–?????? ?????±?????? ?‚?µ????.
        """
        # ???‚???????°?‚?? ?· ?„???????? ?»?????–?? ?‚?° ???°?????»??
        login = form.getfirst("login","")
        password = form.getfirst("pass","")
        users = self.suite.getusers()
        # ?‡?? ?????°?????»???????? ?»?????–??,???°?????»??
        if self._check_user(login, password, users):
            # ?????·?????‡?°?‚?? ???????? ???µ???–?? ???»?? ???????????‚?????°?‡?°
            self.last_id += 1
            self.sessions[self.last_id] = QuizSession(self, self.last_id, login)
            # ???????°?·?°?‚?? ?‚?µ????
            body = self._show_themes(self.suite.getthemes(), self.last_id)
        else:
            # ???????°?·?°?‚?? ???????–???????»?µ?????? ?????? ?????????»????
            body = self._show_error()
        return body


    def _check_user(self, login, password, users):
        """?????‚?µ???‚???„?–???°?†?–?? ???????????‚?????°?‡?°."""
        success = False
        for user in users:
            # user - ???????????? [?»?????–??, ???°?????»??]
            if user == list((login, password)):
                success = True
                break
        return success

    def _show_themes(self, themes, sid):
        """???„???????????°?‚?? ???‚?????–?????? ?· ?‚?µ???°???? ?‚?µ???‚??."""
        ins = ""
        for i, theme in enumerate(themes):
            # ?????±?????????°?‚?? ?????????? ?· ?‚?µ???°???? ?‚?° ???°???–?????????????°????
            ins = ins + HTML_THEME.format(i, theme)
        with open(self.path + THEMES_HTML_FILE, encoding='utf-8') as f:
            # ???????‡???‚?°?‚?? ???–???????‚?????»?µ?????? html-?„?°???»
            cnt = f.read()
        # ?????‚?°?????‚?? ?????±?????????°?????? ?????????? ?‚?° ???????µ?? ???µ???–?—
        return cnt.format(ins, sid)

    def _show_error(self):
        """???„???????????°?‚?? ???‚?????–?????? ?? ???°?·?– ?????????»???? ???…??????."""
        # ???????‡???‚?°?‚?? ?„?°???» html ???? ????????????
        # encoding='utf-8' ?????‚???–?±???? ???»?? ?????°?????»?????????? ???????????°?????? ?‚?µ?????‚??
        with open(self.path + LOGIN_HTML_FILE, encoding='utf-8') as f:
            lines = f.readlines()
        # ?????‚?°?????‚?? ???????–???????»?µ?????? ?????? ?????????»???? ???µ???µ?? ?????‚?°?????–???? 2 ?‚?µ???°???? ?„?°???»??
        lines.insert(-2, HTML_WRONG_PASS)
        out = ''.join(lines)
        return out

    def theme(self, form):
        """???±?????±???‚?? ???????°?????? ?????±?????? ?‚?µ???? ?‚?µ???‚?? (/theme).

           ???????????????°?‚?? ???»?–?”???‚?? ???‚?????–?????? ?· ???µ???€???? ?????‚?°????????.
        """
        theme_no = int(form.getfirst("theme","0"))  # ???????µ?? ?‚?µ????
        sid = int(form.getfirst("sid","0"))         # ???????µ??
        body = ''
        if sid in self.sessions:
            themes = self.suite.getthemes()
            ses = self.sessions[sid]
            ses.theme = themes[theme_no]
            ses.quiz = self.suite.getquiz(ses.theme)
            body = self._show_question(ses)
        return body


    def _show_question(self, ses):
        """???„???????????°?‚?? ???‚?????–?????? ?· ?????‚?°????????."""
        ins = ""
        quest = ses.quiz.questions[ses.quest_no]
        if quest.type == SEVERAL: # ?????±?–?? ???µ???–?»???????— ???°???–?°???‚?–??
            # ?????‚?°???»???‚?? ???????????? ?????±??????
            html = HTML_CHECK
        else:
            # ?????‚?°???»???‚?? ???°???–??????????????
            html = HTML_RADIO
        for i, answer in enumerate(quest.answers):
            # ?????±?????????°?‚?? ?????????? ?· ???–?????????–????????
            ins = ins + html.format(i, answer.text)
        with open(self.path + QUEST_HTML_FILE, encoding='utf-8') as f:
            # ???????‡???‚?°?‚?? ???–???????‚?????»?µ?????? html-?„?°???»
            cnt = f.read()
        # ?????‚?°?????‚?? ?‚?µ?????‚ ?????‚?°??????, ?????±?????????°?????? ??????????, ???°???°???µ?‚????
        return cnt.format(quest.text, ins, ses.sid)


    def question(self, form):
        """???±?????±???‚?? ???????°?????? ???°???°?????? ?????‚?°?????? (/qurstion).

           ???????????????°?‚?? ???»?–?”???‚?? ???‚?????–?????? ?· ???°???‚?????????? ?????‚?°????????.
           ?????‰?? ?????‚?°?????? ?·?°???–???‡???»??????, ?‚?? ???????°?…?????°?‚?? ?‚?° ?·?±?µ???µ???‚?? ???µ?·???»???‚?°?‚.
           ???????????????°?‚?? ???»?–?”???‚?? ???‚?????–?????? ?· ???µ?·???»???‚?°?‚???? ?‚?µ???‚??.
        """
        sid = int(form.getfirst("sid","0"))         # ???????µ??
        body = ''
        # ?????‰?? ???µ???–?? ???µ ?·?°???µ???€?µ????
        if sid in self.sessions:
            ses = self.sessions[sid]
            # ???‚???????°?‚?? ???–?????????–???– ???° ?????‚?°?????– ?????‚?°?????? ?‚?° ???????°?‚?? ?—?…
            # ???? ???????????? ???–?????????–???µ??
            last_reply = self._get_reply(form, ses)
            ses.replies.append(last_reply)
            ses.quest_no += 1   # ???µ???µ???‚?? ???? ???°???‚???????????? ?????‚?°??????
            if ses.quest_no < len(ses.quiz.questions):
                # ?‰?µ ?” ?????‚?°??????
                body = self._show_question(ses)
            else:
                # ?????‚?°?????? ?·?°???–???‡???»??????
                result = ses.quiz.assess(ses.user, ses.replies)
                ses.quiz.writeresult(result)
                body = self._show_result(result)
                # ???????°?»???‚?? ?·?°???µ???µ?€???? ???µ???–?? ?· ???»???????????° ???µ???–??
                del self.sessions[ses.sid]
        return body

    def _show_result(self, result):
        """???„???????????°?‚?? ???‚?????–?????? ?· ???µ?·???»???‚?°?‚????."""
        with open(self.path + RESULT_HTML_FILE, encoding='utf-8') as f:
            # ???????‡???‚?°?‚?? ???–???????‚?????»?µ?????? html-?„?°???»
            cnt = f.read()
        # ?????‚?°?????‚?? ???‚???????°???– ?±?°?»?? ?‚?° ???°?????????°?»?????– ?±?°?»??
        return cnt.format(result.points, result.maxpoints)

    def _get_reply(self, form, ses):
        """???‚???????°?‚?? ?????????? ?· ???–?????????–???????? ???° ?????‚?°??????.

           ? ?µ?·???»???‚?°?‚ - ?†?µ ???????????? ?· ?????»?–?? ?‚?° ???????????†??.
           ???–?»?????–???‚?? ?????»?–?? ?‚?° ???????????†?? ???–?????????–???°?” ???–?»?????????‚?– ???–?????????–???µ??.
           ???????????†?– ???‚?°???»???‚?????? ???»?? ?????±???°?????… ???–?????????–???µ??.
         """
        quest = ses.quiz.questions[ses.quest_no]
        if quest.type == SEVERAL: # ?????±?–?? ???µ???–?»???????— ???°???–?°???‚?–??
            # ???????????? ?????±???°?????… ???????µ???–?? ???–?????????–???µ??
            lst = form.getlist("answer")
            lst = list(map(int, lst))
        else:
            # ???????????? ?· ???????–?”?— ?????±???°?????— ???–?????????–???–
            lst = [int(form.getfirst("answer", "-1"))]

        # ?????±?????????° ???????????? ?????»?–?? ?‚?° ???????????†??
        r = [0] * len(quest.answers)
        for i in lst:
            r[i] = 1
        return r

