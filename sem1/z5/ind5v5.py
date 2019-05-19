import re

P_MAIL = r'<.+@\w+.\w+>'
# r'<\w+@\.+.\.{2,3}>'  # r'^<\w+@\.+.\.{2,3}>$' r'@\.+.\.{2,3}>$'

def extract_mail_from_line(line,mail_list):
    mails = re.findall(P_MAIL, line)
    for mail in mails:
        mail_list.append(mail)
    del mails

def extract_mail_from_file(filename):
    contacts = []
    f = open(filename)
    for line in f.readlines():
        extract_mail_from_line(line,contacts)
    f.close()
    return contacts

filename = 'inp.txt'
interlocuteurs = extract_mail_from_file(filename)
interlocuteurs.sort()
print(*interlocuteurs, sep='\n')