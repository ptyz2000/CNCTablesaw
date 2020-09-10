# Written By: Jeremy Fielding
# Project based on Youtube Video https://youtu.be/JEImn7s7x1o
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from time import sleep
import RPi.GPIO as GPIO

math = ""
buffer = 0

GPIO.setwarnings(False)

# setup pins
# Fence position outputs
DIR_f = 000  # Direction GPIO Pin for Fence
STEP_f = 000  # Step GPIO Pin
MAX_f = 99  # this is the dimension that should be displayed when the fence is on the max limit sensor
MIN_f = 0  # this is the dimension that should be displayed when the fence is on the min limit sensor
CW_f = 0  # Clockwise Rotation
CCW_f = 1  # Counterclockwise Rotation
# blade Angle outputs
DIR_a = 000  # Direction GPIO Pin
STEP_a = 0000  # Step GPIO Pin
MAX_a = 99
MIN_a = 0
CW_a = 0  # Clockwise Rotation
CCW_a = 1  # Counterclockwise Rotation
# blade height outputs
DIR_h = 000  # Direction GPIO Pin
STEP_h = 000  # Step GPIO Pin
MAX_h = 99
MIN_h = 0
CW_h = 0  # Clockwise Rotation
CCW_h = 1  # Counterclockwise Rotation

# Sensor inputs
fencezero = 00  # GPIO Pin
fenceendpos = 00  # fence end of travel right side of blade
# fenceendnegative = 000  # fence end of travel negative if setup for other side of blade
heightzero = 0
heightend = 99
angle0 = 0
angle45 = 99
# estop = 22    #estop input stops all movement

# defining speed for motors
# Fence
RPM_f = 500
steps_per_revolution_f = 400
fdelay = 1 / ((RPM_f * steps_per_revolution_f) / 60)
stp_per_inch_f = 129.912814
# blade angle
RPM_a = 400
steps_per_revolution_a = 400
adelay = 1 / ((RPM_a * steps_per_revolution_a) / 60)
stp_per_inch_a = 147.853
# blade height
RPM_h = 900
steps_per_revolution_h = 400
hdelay = 1 / ((RPM_h * steps_per_revolution_h) / 60)
stp_per_inch_h = 6080


def move_fence(entry):
    # setup variables
    start_position = float(currentFence.get_text())
    new_position = float(entry.get_text())

    # task to complete first
    entry.set_text("")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIR_f, GPIO.OUT)
    GPIO.setup(STEP_f, GPIO.OUT)
    GPIO.setup(fencezero, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(fenceendpos, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(estop, GPIO.IN)

    if float(start_position) < float(new_position):
        dis_to_move = float(new_position) - float(start_position)

        move_fence_steps = int(stp_per_inch_f * float(dis_to_move))

        for steps in range(move_fence_steps):
            if GPIO.input(fenceendpos):
                currentFence.set_text(str(MAX_f))
                break
            GPIO.output(DIR_f, CW_f)
            GPIO.output(STEP_f, GPIO.HIGH)
            sleep(fdelay)
            GPIO.output(STEP_f, GPIO.LOW)
            sleep(fdelay)
            currentFence.set_text(str(new_position))

    elif start_position > new_position:
        dis_to_move = start_position - new_position

        move_fence_steps = int(stp_per_inch_f * dis_to_move)
        for steps in range(move_fence_steps):
            if GPIO.input(fencezero):
                currentFence.set_text(str(MIN_f))
                break
            GPIO.output(DIR_f, CCW_f)
            GPIO.output(STEP_f, GPIO.HIGH)
            sleep(fdelay)
            GPIO.output(STEP_f, GPIO.LOW)
            sleep(fdelay)
            currentFence.set_text(str(new_position))
    elif start_position == new_position:
        return

    # reset things for next function
    GPIO.cleanup()


def change_angle(entry):
    # setup variables
    start_position = float(currentAngle.get_text())
    new_position = float(entry.get_text())

    # task to complete first
    entry.set_text("")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIR_a, GPIO.OUT)
    GPIO.setup(STEP_a, GPIO.OUT)
    GPIO.setup(angle0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(angle45, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    if float(start_position) < float(new_position):
        dis_to_move = float(new_position) - float(start_position)

        move_angle_steps = int(stp_per_inch_a * float(dis_to_move))

        for steps in range(move_angle_steps):
            if GPIO.input(angle45):
                currentAngle.set_text(str(MIN_a))
                break
            GPIO.output(DIR_a, CW_a)
            GPIO.output(STEP_a, GPIO.HIGH)
            sleep(adelay)
            GPIO.output(STEP_a, GPIO.LOW)
            sleep(adelay)
            currentAngle.set_text(str(new_position))

    elif float(start_position) > float(new_position):
        dis_to_move = float(start_position) - float(new_position)

        move_angle_steps = int(stp_per_inch_a * float(dis_to_move))
        for steps in range(move_angle_steps):
            if GPIO.input(angle0):
                currentAngle.set_text(str(MAX_a))
                break
            GPIO.output(DIR_a, CCW_a)
            GPIO.output(STEP_a, GPIO.HIGH)
            sleep(adelay)
            GPIO.output(STEP_a, GPIO.LOW)
            sleep(adelay)
            currentAngle.set_text(str(new_position))

    elif start_position == new_position:
        return

    # reset things for next function
    GPIO.cleanup()
    # C_angle_e.delete(0,END)
    # C_angle_e.insert(0, str(new_position))


def move_blade(entry):
    # setup variables
    start_position = float(currentBlade.get_text())
    new_position = float(entry.get_text())

    # task to complete first
    entry.set_text("")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIR_h, GPIO.OUT)
    GPIO.setup(STEP_h, GPIO.OUT)
    GPIO.setup(heightzero, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(heightend, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    if float(start_position) < float(new_position):
        dis_to_move = float(new_position) - float(start_position)

        move_height_steps = int(stp_per_inch_h * float(dis_to_move))

        for steps in range(move_height_steps):
            if GPIO.input(heightend):
                currentBlade.set_text(str(MAX_h))
                break
            GPIO.output(DIR_h, CW_h)
            GPIO.output(STEP_h, GPIO.HIGH)
            sleep(hdelay)
            GPIO.output(STEP_h, GPIO.LOW)
            sleep(hdelay)
            currentBlade.set_text(str(new_position))

    elif float(start_position) > float(new_position):
        dis_to_move = float(start_position) - float(new_position)

        move_height_steps = int(stp_per_inch_h * float(dis_to_move))
        for steps in range(move_height_steps):
            if GPIO.input(heightzero):
                currentBlade.set_text(str(MIN_h))
                break
            GPIO.output(DIR_h, CCW_h)
            GPIO.output(STEP_h, GPIO.HIGH)
            sleep(hdelay)
            GPIO.output(STEP_h, GPIO.LOW)
            sleep(hdelay)
            currentBlade.set_text(str(new_position))

    elif start_position == new_position:
        return

    GPIO.cleanup()
    # C_height_e.delete(0,END)
    # C_height_e.insert(0, str(new_position))


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
window.show_all()
Gtk.main()
