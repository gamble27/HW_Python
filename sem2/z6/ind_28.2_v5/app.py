from wsgiref.simple_server import make_server
import cgi
from xml.etree.ElementTree import ElementTree, Element, parse


START_PAGE = "/home/olga/PyCharm/domashki/sem2/z6/ind_28.2_v5/index.html"

# todo: <option selected="selected"> for previously selected currencies


class CurrencyConverterApp:

    def __init__(self, XML_currency_file):
        #  xml currencies stuff
        self.XML = XML_currency_file
        self.currencies_tree = None
        self.currencies = self._get_currencies_list()

        #server stuff
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
        # act just like in http parser
        in_buy = False
        in_sell = False
        for child in self.currencies_tree.iter():
            if child.tag == "targetCurrency":
                if child.text == sell:
                    in_sell = True
                elif child.text == buy:
                    in_buy = True
            elif child.tag == "exchangeRate" and in_buy:
                ex_rate = float(child.text)
                in_buy = False
            elif child.tag == "inverseRate" and in_sell:
                inv_rate = float(child.text)
                in_sell = False
            else:
                pass

        return qnt*ex_rate*inv_rate

    def calculate(self, form):
        tags = ["curr_sell", "curr_buy", "sell_quantity"]
        if all([tag in form for tag in tags]):
            curr_sell = form["curr_sell"].value
            curr_buy = form["curr_buy"].value
            qnt = float(form["sell_quantity"].value)

            converted = self.convert(curr_sell, curr_buy, qnt)

            converted = curr_sell + " = " + str(converted) + " " + curr_buy
        else:
            return "error"

        return self._format_resp(
            START_PAGE,
            [("currencies", self._curr_opt_),
             ("value", converted)]
        )

    def _get_currencies_list(self):
        with open(self.XML) as f:
            self.currencies_tree = parse(self.XML)
        # tree = ElementTree(Element("item"))

        currencies = []
        # currencies.append(tree.findtext("baseCurrency"))
        #
        # currs = tree.findall("item")
        # for cur_el in currs:
        # cc = self.currencies_tree.findtext("baseCurrency")
        # currencies.append(cc)

        for child in self.currencies_tree.iter():
            if child.tag == "targetCurrency":
                currencies.append(child.text)

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
    app = CurrencyConverterApp("/home/olga/PyCharm/domashki/sem2/z6/ind_28.2_v5/currencies_usd.xml")

    server = make_server("localhost", 8051, app)
    server.serve_forever()
