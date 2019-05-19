from tkinter import *
from database import SQLiteDatabase


class ToysApp(Tk):
    def __init__(self, toy_db_name):
        Tk.__init__(self)

        self.__init_DB(toy_db_name)

        self.__init_UI()

    def __init_DB(self, toy_db_name):
        self.toy_DB = SQLiteDatabase(toy_db_name)
        structure = {
            "name":    "TEXT",
            "price":   "NUMERIC",
            "min_age": "NUMERIC",
            "max_age": "NUMERIC"
        }
        self.table_name = "toys_catalogue"
        self.toy_DB.create_table(self.table_name, structure)

    def __init_UI(self):
        self.title("Toy Search")

        self.addMenu = Menu(self, tearoff=0)
        self.addMenu.add_command(label="Add a toy", command=self.add_toy_handler)
        self.config(menu=self.addMenu)

        Label(self, text="Search for toys").grid(row=0, column=0)

        Label(self, text="Kid age:").grid(row=1, column=0)
        self.kid_age_inp = Entry(self)
        self.kid_age_inp.grid(row=1, column=1)

        Label(self, text="Max price:").grid(row=2, column=0)
        self.toy_price_inp = Entry(self)
        self.toy_price_inp.grid(row=2, column=1)

        Button(
            self, text="Search", command=self.search_toys_handler
        ).grid(row=3, column=1)

    def add_toy_handler(self):
        self.addWindow = Toplevel(self)
        self.addWindow.title("Add a toy to database")

        Label(self.addWindow, text="Toy name:").grid(row=0, column=0)
        self.toy_name_inp = Entry(self.addWindow)
        self.toy_name_inp.grid(row=0, column=1)


        Label(self.addWindow, text="Toy price:").grid(row=1, column=0)
        self.toy_price_inp = Entry(self.addWindow)
        self.toy_price_inp.grid(row=1, column=1)


        Label(self.addWindow, text="Min age:").grid(row=2, column=0)
        self.min_age_inp = Entry(self.addWindow)
        self.min_age_inp.grid(row=2, column=1)


        Label(self.addWindow, text="Max age:").grid(row=3, column=0)
        self.max_age_inp = Entry(self.addWindow)
        self.max_age_inp.grid(row=3, column=1)

        Button(
            self.addWindow, text="Add", command=self.save_toy_handler
        ).grid(row=4, column=1)

    def search_toys_handler(self):
        self.resultsWindow = Toplevel(self)
        self.resultsWindow.title("Toys found")
        # self.resultsWindow.propagate(0)

        toys = self._toy_search()

        for i in range(len(toys)):
            Label(
                self.resultsWindow, text="{}".format(toys[i][0])
            ).grid(row=i, column=0)
            Label(
                self.resultsWindow, text="{}".format(toys[i][1])
            ).grid(row=i, column=1)

        # print(self.resultsWindow.winfo_height())
        self.resultsWindow.geometry("{w}x{h}".format(
            w=250, h=len(toys)*20
        ))

    def _toy_search(self):
        query = """max_age>={age} AND min_age<={age} AND price<={price}""".format(
            age=int(self.kid_age_inp.get()),
            price=int(self.toy_price_inp.get())
        )
        return self.toy_DB.fetchall(
            self.table_name, query, fetch_fields=["name", "price"]
        )

    def save_toy_handler(self):
        values = {
            "name":    self.toy_name_inp.get(),
            "price":   int(self.toy_price_inp.get()),
            "min_age": int(self.min_age_inp.get()),
            "max_age": int(self.max_age_inp.get())
            }
        self.addWindow.destroy()
        self.toy_DB.join(self.table_name, values)


if __name__ == "__main__":
    app = ToysApp("toys")
    app.mainloop()
