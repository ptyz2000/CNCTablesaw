# Written By: Jeremy Fielding
# Project based on Youtube Video https://youtu.be/JEImn7s7x1o
import Movement
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

math = ""
buffer = 0


Movement = Movement.Movement()


def move_fence(entry):
    currentFence.set_text(str(Movement.move_fence(float(entry.get_text()), float(currentFence.get_text()))))


def change_angle(entry):
    currentAngle.set_text(str(Movement.change_angle(float(entry.get_text()), float(currentAngle.get_text()))))


def move_blade(entry):
    currentBlade.set_text(str(Movement.move_blade(float(entry.get_text()), float(currentBlade.get_text()))))


def calc_clicked(button):
    calcEntry.set_text(calcEntry.get_text() + button.get_label())


def clear_entry(entry):
    entry.set_text("")


def calc_operator(button):
    global math
    math = button.get_label()
    global buffer
    buffer = float(calcEntry.get_text())
    calcEntry.set_text("")


def calc_equal(button):
    current = float(calcEntry.get_text())
    if math == "+":
        calcEntry.set_text(str(buffer + current))
    elif math == "-":
        calcEntry.set_text(str(buffer - current))
    elif math == "*":
        calcEntry.set_text(str(buffer * current))
    elif math == "/":
        calcEntry.set_text(str(buffer / current))
    else:
        return


def inch_to_mm(button):
    calcEntry.set_text(str(float(calcEntry.get_text()) * 25.4))


def mm_to_inch(button):
    calcEntry.set_text(str(float(calcEntry.get_text()) / 25.4))


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


handlers = {
    "gtk_main_quit": Gtk.main_quit,
    "on_Calc_clicked": calc_clicked,
    "Clear_clicked": clear_entry,
    "on_Calc_operator": calc_operator,
    "on_Calc_equals_clicked": calc_equal,
    "on_In_to_mm_clicked": inch_to_mm,
    "on_mm_to_in_clicked": mm_to_inch,
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
currentFence.set_text("0.0")
currentAngle = builder.get_object("Angle_pos")
currentAngle.set_text("0.0")
currentBlade = builder.get_object("Blade_pos")
currentBlade.set_text("0.0")
window = builder.get_object("Saw")
window.maximize()
window.show_all()
Gtk.main()
