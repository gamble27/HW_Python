from wsgiref.simple_server import make_server
import cgi
from static.database import SQLiteDatabase
# import templating


HOST = "localhost"
PORT = 8060

START_PAGE = "/home/olga/Projects/domashki/sem2/z8/ind_29.2_v5/static/index.html"
ADD_ROUTE_PAGE = "/home/olga/Projects/domashki/sem2/z8/ind_29.2_v5/static/add_route.html"
ADD_PASSENGER_PAGE = "/home/olga/Projects/domashki/sem2/z8/ind_29.2_v5/static/add_passenger.html"
ERROR_PAGE = "/home/olga/Projects/domashki/sem2/z8/ind_29.2_v5/static/error.html"

PRICE_PER_KM = 1  # у гривнях за кілометр

def log(error):
    with open("log.txt", 'a') as f:
        f.write(str(error))
        f.write("\n")
        f.close()


class Passenger:
    def __init__(self, id_card, name=None, db=None, table=None, fields=None):
        self.id_card = id_card
        if name:
            self.name = name
        else:
            if all([db, table] + fields):
                self.get_from_db(db, table, fields)
            else:
                raise Exception("no passenger presized")

        # useless stuff
        self.departure = None
        self.destination = None

    def calculate_price(self):
        # if self.departure and self.destination:
        #     pass
        # else:
        #     raise Exception("no departure, destination and stuff")

        # P.S. Your architecture is really dull.

        pass

    def add_to_db(self, db, table, fields):
        values = {
            fields[0]: self.id_card,
            fields[1]: self.name
        }

        db.join(table, values)

    # @useless
    def get_from_db(self, db, table, fields):
        """
        get name from DB
        :param db: opened database
        :param table: table name
        :param fields: 0: id field name
                       1: name field name
        :return: None
        """
        name = db.find(table, self.id_card, fields[0], fetch_fields=fields[1])
        if not name:
            raise Exception("invisible man detected")
        self.name = name[1]


class Application:
    def __init__(self, db_name):
        #  db stuff
        self.db = SQLiteDatabase(db_name)
        self._passenger_table = "passengers"
        # self.db.create_table(
        #     self._passenger_table,
        #     {
        #         "id_card": "TEXT",
        #         "name": "TEXT"
        #     }
        # )
        self._destins_table = "destinations"
        # self.db.create_table(
        #     self._destins_table,
        #     {"name": "TEXT"}
        # )
        self._routes_table = "routes"
        # self.db.create_table(
        #     self._routes_table,
        #     {
        #         "fr0m": "TEXT",
        #         "t0": "TEXT",
        #         "distance": "INTEGER"
        #     }
        # )

        #  server stuff
        self.commands = {
            "":              self.start,
            "add_passenger": self.add_passenger,
            "add_route":     self.add_route,
            "calculate":     self.calculate_price,

            "add_route_btn": self.open_route,
            "add_passenger_btn": self.open_passenger,
        }

        # self._destinations_list()

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
            body = self.throw_error('Daaafaaaquuu! 404 is here, dude.')

        # return [templating.load_page(
        #     {'content': 'page 1 content'},
        #     START_PAGE
        # )]
        return [bytes(body, encoding='utf-8')]

    def _format_resp(self, resp_file, arg_list=None):
        """
        потому что сраный css со своими четырежды уебанными фигурными скобками не может блять не помешать
        :param resp_file: html file with response
        :param arg_list: list of tuples like this: ("param_name", value)
        :return: formatted response without any errors!
        """
        with open(resp_file) as f:
            lines = f.readlines()

        if arg_list is None:
            return ''.join(lines)

        for (key, value) in arg_list:
            for j, line in enumerate(lines):
                keyword = "{" + key + "}"
                if keyword in line:
                    i = line.find(keyword)
                    lines[j] = line[:i] + str(value) + line[i+len(keyword):]
        return ''.join(lines)

    def start(self, form=None, price=0):
        price = str(price) if price > 0 else ""
        return self._format_resp(
            START_PAGE,
            [("price", price),
             ("destinations", self._destinations_list),
             ("passengers", self._passengers_list)]
        )

    def add_route(self, form):
        tags = [
            "from",
            "to",
            "distance"
        ]
        if all([tag in form for tag in tags]):
            depart = str(form["from"].value)
            destin = str(form["to"].value)
            distance = int(form["distance"].value)
            if depart == destin:
                return self.throw_error("You can't make a route from {t} to {t}, dude :)".format(t=destin))

            self.db.join(
                self._routes_table,
                {"fr0m": depart,
                 "t0": destin,
                 "distance": distance,
                 }
            )
        return self.start()

    def add_passenger(self, form):
        tags = [
            "name",
            "id_card"
        ]
        if all([tag in form for tag in tags]):
            id_card = form["id_card"].value
            name = form["name"].value
            Passenger(id_card, name).add_to_db(
                self.db, self._passenger_table,
                ["id_card", "name"]
            )
        return self.start()

    def calculate_price(self, form):
        tags = [
            "passenger",
            "from",
            "to"
        ]
        if all([tag in form for tag in tags]):
            name = form["passenger"].value
            depart = form["from"].value
            destin = form["to"].value

            if destin == depart:
                return self.throw_error("You are already here, dude ;)")
            try:
                distance = self.db.fetchall(
                    self._routes_table,
                    # {
                    #     "fr0m": depart,
                    #     "t0": destin
                    # },
                    """fr0m='{dep}' AND t0='{dest}'""".format(dep=depart, dest=destin),
                    fetch_fields=["distance"],
                )
                if not distance:
                    log(distance)
                    return self.throw_error("There are no routes from {fr0m} to {t0}".format(
                        fr0m=depart, t0=destin
                    ))
            except Exception as e:
                log(e)

                return self.throw_error("There are no routes from {fr0m} to {t0}".format(
                    fr0m=depart, t0=destin
                ))

            pr1ce = distance[0][0] * PRICE_PER_KM
            return self.start(price=pr1ce)
        else:
            return self.throw_error("no data chosen")

    def open_route(self, form=None):
        return self._format_resp(
            ADD_ROUTE_PAGE,
            [("destinations", self._destinations_list)]
        )

    def open_passenger(self, form=None):
        return self._format_resp(ADD_PASSENGER_PAGE)

    @property
    def _passengers_list(self):
        res = '<option value="Select passenger" disabled>Select passenger</option>\n'
        opt_pattern = '<option value="{v}">{v}</option>\n'
        passengers = sorted(list(map(
            lambda fetched: fetched[0],
            self.db.show_table(self._passenger_table, fields=["name"], distinct=True)
        )))
        for passenger in passengers:
            res += opt_pattern.format(v=passenger)
        return res

    @property
    def _destinations_list(self):
        res = '<option value="Select town" disabled>Select town</option>\n'
        opt_pattern = '<option value="{v}">{v}</option>\n'
        for option in self.db.show_table(self._destins_table, fields=["name"], distinct=True):
            res += opt_pattern.format(v=option[0])
        return res

    def throw_error(self, message="unexpected error"):
        return self._format_resp(
            ERROR_PAGE,
            [("error", message)]
        )


if __name__ == "__main__":
    db = "infrastructure"
    app = Application(db)

    server = make_server(HOST, PORT, app)
    server.serve_forever()
