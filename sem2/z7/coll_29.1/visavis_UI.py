from tkinter import *
from database import SQLiteDatabase
from datetime import date
from calendar import monthrange


class VisavisApp(Tk):
    def __init__(self, db_name):
        Tk.__init__(self)

        self.months = [
            "January", "February",
            "March", "April", "May",
            "June", "July", "August",
            "September", "October", "November",
            "December"
        ]

        self.__init_DB(db_name)

        self.__init_UI()

    def __init_DB(self, db_name):
        self.DB = SQLiteDatabase(db_name)
        structure = {
            "name":  "TEXT",
            "day":   "NUMERIC",
            "month": "TEXT",
            "year":  "NUMERIC"
        }
        self.table_name = "birthdays"
        self.DB.create_table(self.table_name, structure)

    def __init_UI(self):
        self.title("Almost Calendar")

        self.addMenu = Menu(self, tearoff=0)
        self.addMenu.add_command(label="Add person", command=self.add_person_handler)
        self.addMenu.add_command(label="Find birthday", command=self.find_bday_handler)

        self.config(menu=self.addMenu)


        birthdays = self._fetch_week_bdays()
        if len(birthdays) == 0:
            Label(self, text="This week birthdays").grid(row=0, column=0)

        self.widgets = []

        for i in range(len(birthdays)):
            self.widgets.append(Label(
                self, text="{}".format(birthdays[i][0])
            ))
            self.widgets[len(self.widgets)-1].grid(row=i, column=0)
            date = "{dd} {mm} {yy}".format(
                dd=birthdays[i][1],
                mm=birthdays[i][2],
                yy=birthdays[i][3],
            )
            self.widgets.append(Label(self, text=date))
            self.widgets[len(self.widgets)-1].grid(row=i, column=1)

        # print(self.resultsWindow.winfo_height())
        # self.geometry("{w}x{h}".format(
        #     w=250, h=len(birthdays)*20
        # ))

    def _fetch_week_bdays(self):
        buf = (monthrange(date.today().year, date.today().month)[1]
                - date.today().day) # проверка, выскакиваем ли мы за рамки месяца
        if  buf < 7:
            c = """OR (day<={dd} AND month="{mm}")""".format(
                dd=buf, mm=self.months[date.today().month]
            ) # если да, докидываем еще условие
        else: c="" # ну нет так нет
        condition = """(day>={dd} AND day<={dd}+7 AND month="{mm}")
        {c2}""".format(
            dd=date.today().day, mm=self.months[date.today().month-1],
            c2=c
        )
        return self.DB.fetchall(
            self.table_name,
            condition,
            fetch_fields=["name", "day", "month", "year"]
        )

    def find_bday_handler(self):
        names = [n[0] for n in self.DB.show_table(self.table_name, fields=["name"])]
        self.findWindow = Toplevel(self)
        self.findWindow.title("Find birthday")

        self.search_name_inp = Spinbox(self.findWindow, values=names)
        self.search_name_inp.grid(row=0, column=0)

        Button(self.findWindow, text="Find", command=self.find_handler).grid(row=1, column=0)

        self.show_res_label = Label(self.findWindow, text="")
        self.show_res_label.grid(row=2, column=0)

    def find_handler(self):
        name = '"{}"'.format(self.search_name_inp.get())
        # print(name)
        bday = ' '.join(map(str,self.DB.fetchall(
            self.table_name,
            condition={"name": name},
            fetch_fields=["day", "month", "year"]
        )[0]))
        self.show_res_label.config(text=bday)
        self.show_res_label.update_idletasks()


    def add_person_handler(self):
        self.addWindow = Toplevel(self)
        self.addWindow.title("Add person to database")

        Label(self.addWindow, text="Name:").grid(row=0, column=0)
        self.name_inp = Entry(self.addWindow)
        self.name_inp.grid(row=0, column=1)


        Label(self.addWindow, text="Birth day:").grid(row=1, column=0)
        self.b_day_inp = Entry(self.addWindow)
        self.b_day_inp.grid(row=1, column=1)


        Label(self.addWindow, text="Birth month:").grid(row=2, column=0)
        self.b_month_inp = Spinbox(self.addWindow, values=self.months)
        self.b_month_inp.grid(row=2, column=1)


        Label(self.addWindow, text="Birth year:").grid(row=3, column=0)
        self.b_year_inp = Entry(self.addWindow)
        self.b_year_inp.grid(row=3, column=1)

        Button(
            self.addWindow, text="Add", command=self.save_person_handler
        ).grid(row=4, column=1)

    def save_person_handler(self):
        values = {
            "name":  self.name_inp.get(),
            "day":   int(self.b_day_inp.get()),
            "month": self.b_month_inp.get(),
            "year":  int(self.b_year_inp.get())
        }
        self.addWindow.destroy()
        self.DB.join(self.table_name, values)

        self._clear_screen()

        self.__init_UI()

    def _clear_screen(self):
        for widget in self.widgets:
            widget.destroy()
            del widget
        # print(len(self.widgets))

if __name__ == "__main__":
    app = VisavisApp("bdays")
    app.mainloop()
