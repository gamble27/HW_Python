import cgi

from phonebook import JSONPhoneBook

START_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2/index.html"
ADD_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2/add_contact.html"
EDIT_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2/edit_contact.html"
FIND_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2/find_contact.html"


class PhoneBookWeb(JSONPhoneBook):
    def __init__(self, json_addr, key_field, field_list):
        JSONPhoneBook.__init__(self, json_addr, key_field, field_list)

        self.commands = {
            "": self.start,
            "add": self.add,
            "edit": self.edit,
            "search": self.search,
            "process": self.process
        }

    def __call__(self, environ, start_response):
        command = environ.get('PATH_INFO', '').lstrip('/')
        form = cgi.FieldStorage(
            fp=environ['wsgi.input'], environ=environ
        )
        error = False
        if command in self.commands:
            body = self.commands[command](form)
            if body:
                start_response(
                    '200 OK', [('Content-Type', 'text/plain; charset=utf-8')]
                )
            else:
                error = True
        else:
            error = True

        if error:
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            body = 'Dafaq is going on, laaad?'
        return [bytes(body, encoding='utf-8')]

    @staticmethod
    def start(self, form):
        # with open(START_PAGE) as f:
        #     cnt = f.read()
        # return cnt
        pass

    def add(self, form):
        pass

    def edit(self, form):
        pass

    def search(self, form):
        pass


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    application = PhoneBookWeb(
        "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2/phones.json",
        "contact", ["phone"]
    )

    hhtpd = make_server('localhost', 8042, application)
    hhtpd.serve_forever()
