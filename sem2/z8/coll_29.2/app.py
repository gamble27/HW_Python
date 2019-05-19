from wsgiref.simple_server import make_server
import cgi
from database import SQLiteDatabase

START_PAGE = "/home/olga/Projects/domashki/sem2/z8/coll_29.2/index.html"

# todo: <option selected="selected"> for previously selected currencies


class CurrencyConverterApp:

    def __init__(self, currency_db, tablename):
        # DB currencies stuff
        self.DB = SQLiteDatabase(currency_db)

        # table: currency, exchange_rate, inverse_rate
        self.table = tablename
        self.currencies = self._get_currencies_list()

        #  server stuff
        self.commands = {
            "":          self.start,
            "calculate": self.calculate
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

    def start(self, form=None):
        return self._format_resp(
            START_PAGE,
            [("currencies", self._curr_opt_),
             ("value", "")]
        )

    def convert(self, sell, buy, qnt):

        cond = 'currency="{}"'
        ex_rate = float(self.DB.fetchall(
            self.table, cond.format(buy), ["exchange_rate"]
        )[0][0])
        # print(ex_rate)
        inv_rate = float(self.DB.fetchall(
            self.table, cond.format(sell), ["inverse_rate"]
        )[0][0])

        return qnt*ex_rate*inv_rate

    def calculate(self, form):
        tags = ["curr_sell", "curr_buy", "sell_quantity"]
        if all([tag in form for tag in tags]):
            curr_sell = form["curr_sell"].value
            curr_buy = form["curr_buy"].value
            qnt = float(form["sell_quantity"].value)

            converted = self.convert(curr_sell, curr_buy, qnt)

            converted = str(qnt) + " " + curr_sell + " = " + str(converted) + " " + curr_buy
        else:
            return "error"

        return self._format_resp(
            START_PAGE,
            [("currencies", self._curr_opt_),
             ("value", converted)]
        )

    def _get_currencies_list(self):
        currencies = self.DB.show_table(
            self.table, fields=["currency"]
        )
        currencies = [c[0] for c in currencies]

        return sorted(currencies)

    @property
    def _curr_opt_(self):
        res = '<option value="Select currency" disabled>Select currency</option>'
        opt_pattern = '<option value="{v}">{v}</option>\n'
        for curr in self.currencies:
            res += opt_pattern.format(v=curr)
        return res

    def _format_resp(self, resp_file, arg_list):
        """
        потому что сраный css со своими четырежды уебанными фигурными скобками не может блять не помешать
        :param resp_file: html file with response
        :param arg_list: list of tuples like this: ("param_name", value)
        :return: formatted response without any errors!
        """
        with open(resp_file) as f:
            lines = f.readlines()
        for (key, value) in arg_list:
            for j, line in enumerate(lines):
                keyword = "{" + key + "}"
                if keyword in line:
                    i = line.find(keyword)
                    lines[j] = line[:i] + str(value) + line[i+len(keyword):]
        return ''.join(lines)


if __name__ == "__main__":
    app = CurrencyConverterApp("currencies", "usd")

    server = make_server("localhost", 8051, app)
    server.serve_forever()
