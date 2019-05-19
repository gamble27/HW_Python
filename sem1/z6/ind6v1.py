import re

TRANSL = {
    'в':'фф',
    'б':'п',
    'о':'а',
    'а':'о',
    'я':'йа',
    'к':'г'
}

def translate_text(line):
    res = line
    for key in TRANSL:
        res = re.sub(key, TRANSL[key], res)
    return res

def extract_text(filename):
    f = open(filename)
    contacts = []
    for line in f.readlines():
        contacts.append(translate_text(line.lower()))
    f.close()
    return contacts

f = open('out.txt', 'w', encoding='windows-1251')
f.writelines(extract_text('1inp.txt'))
f.close()