from wsgiref.simple_server import make_server
from phoneapp import PhoneBook

application = PhoneBookWeb()

print("=========== Phone server =============")

hhtpd = make_server('localhost', 8042, application)
hhtpd.serve_forever()
