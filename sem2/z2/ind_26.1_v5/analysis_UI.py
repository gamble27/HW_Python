import tkinter as tk

from text_tone_analyzer import *

from soup_parser import *
from html_parser import HTMLPravdaParser


class PravdaAnalysisUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self._internal_parser = SOUPPravdaParser()
        self._html_parser = None
        self.parser = None

        self.__init_Analyzer()
        self.__init_GUI()

    def __init_GUI(self):
        # UI future stuff
        self.ResultsWindow = None
        self.AuthorLabel = None
        self.ResultLabel = None

        # UI stuff
        days = list(range(1, 31))
        years = list(range(2007, 2020))
        self._months = ['січня', 'лютого', 'березня',
                  'квітня', 'травня', 'червня',
                  'липня', 'серпня', 'вересня',
                  'жовтня', 'листопада', 'грудня']
        self._parsers = ("SOUPPravdaParser", "HTMLPravdaParser")

        # Choose hecking parser
        self.ChooseParserLabel = tk.Label(
            self, text = "Choose Parser:")
        self.ChooseParserLabel.grid(
            row = 0, column = 1)
        self.SBoxParsers = tk.Spinbox(
            self, values = self._parsers)
        self.SBoxParsers.grid(
            row = 0, column = 2)

        # Choose the author
        self.ChooseAuthorLabel = tk.Label(
            self, text = "Choose Author:")
        self.ChooseAuthorLabel.grid(
            row = 1, column = 1)
        authors = list(self._internal_parser.authors.keys())
        authors.sort()
        self.SBoxAuthors = tk.Spinbox(
            self, values = authors)
        self.SBoxAuthors.grid(
            row = 1, column = 2)

        # Choose date interval
        self.ChooseDateLabel = tk.Label(
            self, text = "Choose Date Period:")
        self.ChooseDateLabel.grid(
            row = 2, column = 1)
        # Start
        self.start_date = None
        self.StartDateLabel = tk.Label(
            self, text = "From:").grid(
            row = 3, column = 0)
        self.SBoxFDay = tk.Spinbox(
            self, values = days,
            )
        self.SBoxFDay.grid(
            row = 3, column = 1)
        self.SBoxFMon = tk.Spinbox(
            self, values = list(self._months),
            )
        self.SBoxFMon.grid(
            row = 3, column = 2)
        self.SBoxFYear = tk.Spinbox(
            self, values = years,
            )
        self.SBoxFYear.grid(
            row = 3, column = 3)
        # End
        self.end_date = None
        self.EndDateLabel = tk.Label(
            self, text = "To:").grid(
            row = 4, column = 0)
        self.SBoxLDay = tk.Spinbox(
            self, values = days,
            )
        self.SBoxLDay.grid(
            row = 4, column = 1)
        self.SBoxLMon = tk.Spinbox(
            self, values = list(self._months),
            )
        self.SBoxLMon.grid(
            row = 4, column = 2)
        self.SBoxLYear = tk.Spinbox(
            self, values = years[::-1],
            )
        self.SBoxLYear.grid(
            row = 4, column = 3)

        # Send Query
        self.AnalyzeBtn = tk.Button(
            self, text = "Lookup!",
            command = self.__QueryHandler
        ).grid(
            row = 5, column = 2)

    def __QueryHandler(self):
        parser = self.SBoxParsers.get()
        author = self.SBoxAuthors.get()
        start_date = (int(self.SBoxFDay.get()),
                      self._months.index(self.SBoxFMon.get()) + 1,
                      int(self.SBoxFYear.get()))
        end_date = (int(self.SBoxLDay.get()),
                      self._months.index(self.SBoxLMon.get()) + 1,
                      int(self.SBoxLYear.get()))
        if parser == self._parsers[0]: # beautifulsoup
            self.parser = self._internal_parser
        elif not self._html_parser: # html, uninitialized
                self._html_parser = HTMLPravdaParser()
                self.parser = self._html_parser
        else: # html, initialized
            self.parser = self._html_parser

        corresponding_articles = self.parser.get_author_columns(author, start_date, end_date)
        positive = self.analyzer.get_author_tone(corresponding_articles)

        self.__show_analysis_results(author, positive)

    def __show_analysis_results(self, author, result):
        self.ResultsWindow = tk.Toplevel(self)
        self.AuthorLabel = tk.Label(
            self.ResultsWindow, text = author)
        self.AuthorLabel.pack()
        self.ResultLabel = tk.Label(
            self.ResultsWindow, text = str(result))
        self.ResultLabel.pack()


    def __init_Analyzer(self):
        self.analyzer = ToneAnalyzer()



if __name__ == "__main__":
    analyzer = PravdaAnalysisUI()
    analyzer.mainloop()
