'''
in the input you shoud give
a path to the journal from sysjourn directory

just select a journal you like and
click 'Copy Path'
'''

from sem1.z7.classes_i7v4 import SysJournal

jrn = SysJournal()

#jrn1 = SysJournal.make_journ('Loremipsum')
jrn.get()

j = jrn.reg_name
print(j)

jrn1 = jrn.chk_size(1024)

# s = jrn.get_content()
# print(s[0])

j1 = jrn1.reg_name
print('Ok' if j==j1 else j1)
