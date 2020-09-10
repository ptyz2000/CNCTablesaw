from TableSaw_Controls_Jeremy_Fielding import calcEntry


class Calculator:
    def __init__(self):
        self.math = ""
        self.buffer = 0

    @staticmethod
    def calc_clicked(button):
        calcEntry.set_text(calcEntry.get_text() + button.get_label())

    @staticmethod
    def clear_entry(entry):
        entry.set_text("")

    def calc_operator(self, button):
        self.math = button.get_label()
        self.buffer = float(calcEntry.get_text())
        calcEntry.set_text("")

    def calc_equal(self, button):
        current = float(calcEntry.get_text())
        if self.math == "+":
            calcEntry.set_text(str(self.buffer + current))
        elif self.math == "-":
            calcEntry.set_text(str(self.buffer - current))
        elif self.math == "*":
            calcEntry.set_text(str(self.buffer * current))
        elif self.math == "/":
            calcEntry.set_text(str(self.buffer / current))
        else:
            return

    @staticmethod
    def inch_to_mm(button):
        calcEntry.set_text(str(float(calcEntry.get_text()) * 25.4))

    @staticmethod
    def mm_to_inch(button):
        calcEntry.set_text(str(float(calcEntry.get_text()) / 25.4))
