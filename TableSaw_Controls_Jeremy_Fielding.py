# Written By: Jeremy Fielding
# Project based on Youtube Video https://youtu.be/JEImn7s7x1o
from Calculator import Calculator
from Movement import Movement
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def move_fence(entry):
    currentFence.set_text(str(movement.move_fence(float(entry.get_text()), float(currentFence.get_text()))))


def change_angle(entry):
    currentAngle.set_text(str(movement.change_angle(float(entry.get_text()), float(currentAngle.get_text()))))


def move_blade(entry):
    currentBlade.set_text(str(movement.move_blade(float(entry.get_text()), float(currentBlade.get_text()))))


def move_num(entry):
    entry.set_text(calcEntry.get_text())
    calcEntry.set_text("")


def angle_45(entry):
    entry.set_text("45")


def angle_0(entry):
    entry.set_text("0")


def blade_0(entry):
    entry.set_text("0")


def blade_1(entry):
    entry.set_text("1")


if __name__ == '__main__':

    movement = Movement()
    calculator = Calculator()

    handlers = {
        "gtk_main_quit": Gtk.main_quit,
        "on_Calc_clicked": Calculator.calc_clicked,
        "Clear_clicked": Calculator.clear_entry,
        "on_Calc_operator": calculator.calc_operator,
        "on_Calc_equals_clicked": calculator.calc_equal,
        "on_In_to_mm_clicked": Calculator.inch_to_mm,
        "on_mm_to_in_clicked": Calculator.mm_to_inch,
        "Move_num_clicked": move_num,
        "on_Angle_go_45_clicked": angle_45,
        "on_Angle_go_0_clicked": angle_0,
        "on_Blade_go_0_clicked": blade_0,
        "on_Blade_go_1_clicked": blade_1,
        "on_Fence_mv_clicked": move_fence,
        "on_Angle_mv_clicked": change_angle,
        "on_Blade_mv_clicked": move_blade
    }

    builder = Gtk.Builder()
    builder.add_from_file("Saw control.glade")
    builder.connect_signals(handlers)

    calcEntry = builder.get_object("Calc_entry")

    currentFence = builder.get_object("Fence_pos")
    currentAngle = builder.get_object("Angle_pos")
    currentBlade = builder.get_object("Blade_pos")

    currentFence.set_text("0.0")
    currentAngle.set_text("0.0")
    currentBlade.set_text("0.0")

    window = builder.get_object("Saw")
    window.maximize()
    window.show_all()

    Gtk.main()
