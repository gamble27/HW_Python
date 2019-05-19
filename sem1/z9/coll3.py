import tkinter as tk

def MakeTheDifference():
    res = difference(txt1.get(),txt2.get())
    ans.configure(text='Difference: '+res)

def difference(s1,s2):

    '''
    :param s1: sravnenie
    :param s2: obrazec
    :return: string difference
    '''

    s1set = set(iter(s1))
    s2set = set(iter(s2))

    return ' '.join(s1set-s2set)

wnd = tk.Tk()

txt1cap = tk.Label(wnd, text='String: ')
txt1cap.pack()
txt1 = tk.Entry(wnd)
txt1.pack()

txt2cap = tk.Label(wnd, text='Specimen: ')
txt2cap.pack()
txt2 = tk.Entry(wnd)
txt2.pack()

res = ''

ansCap = tk.Label(wnd, text='Difference: ')
ansCap.pack()
ans = tk.Label(wnd, text=res)

calcButton = tk.Button(wnd, text='Get Results!',
              command = MakeTheDifference(),
              font=('arial', 16))
calcButton.pack()

quitButton = tk.Button(wnd, text='IQuit',
              command=wnd.quit,
              font=('arial', 16))           # кнопка "Закрити"
quitButton.pack()

wnd.mainloop()