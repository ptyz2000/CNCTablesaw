import RPi.GPIO as GPIO
from time import sleep


class Movement:
    def __init__(self):
        GPIO.setwarnings(False)

        # setup pins
        # Fence position outputs
        self.DIR_f = 000  # Direction GPIO Pin for Fence
        self.STEP_f = 000  # Step GPIO Pin
        self.MAX_f = 99  # this is the dimension that should be displayed when the fence is on the max limit sensor
        self.MIN_f = 0  # this is the dimension that should be displayed when the fence is on the min limit sensor
        self.CW_f = 0  # Clockwise Rotation
        self.CCW_f = 1  # Counterclockwise Rotation
        # blade Angle outputs
        self.DIR_a = 000  # Direction GPIO Pin
        self.STEP_a = 0000  # Step GPIO Pin
        self.MAX_a = 99
        self.MIN_a = 0
        self.CW_a = 0  # Clockwise Rotation
        self.CCW_a = 1  # Counterclockwise Rotation
        # blade height outputs
        self.DIR_h = 000  # Direction GPIO Pin
        self.STEP_h = 000  # Step GPIO Pin
        self.MAX_h = 99
        self.MIN_h = 0
        self.CW_h = 0  # Clockwise Rotation
        self.CCW_h = 1  # Counterclockwise Rotation

        # Sensor inputs
        self.fencezero = 00  # GPIO Pin
        self.fenceendpos = 00  # fence end of travel right side of blade
        # fenceendnegative = 000  # fence end of travel negative if setup for other side of blade
        self.heightzero = 0
        self.heightend = 99
        self.angle0 = 0
        self.angle45 = 99
        # estop = 22    #estop input stops all movement

        # defining speed for motors
        # Fence
        self.RPM_f = 500
        self.steps_per_revolution_f = 400
        self.fdelay = 1 / ((self.RPM_f * self.steps_per_revolution_f) / 60)
        self.stp_per_inch_f = 129.912814
        # blade angle
        self.RPM_a = 400
        self.steps_per_revolution_a = 400
        self.adelay = 1 / ((self.RPM_a * self.steps_per_revolution_a) / 60)
        self.stp_per_inch_a = 147.853
        # blade height
        self.RPM_h = 900
        self.steps_per_revolution_h = 400
        self.hdelay = 1 / ((self.RPM_h * self.steps_per_revolution_h) / 60)
        self.stp_per_inch_h = 6080

    def move_fence(self, new_position, start_position):

        # task to complete first
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.DIR_f, GPIO.OUT)
        GPIO.setup(self.STEP_f, GPIO.OUT)
        GPIO.setup(self.fencezero, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.fenceendpos, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # GPIO.setup(estop, GPIO.IN)

        if float(start_position) < float(new_position):
            dis_to_move = float(new_position) - float(start_position)

            move_fence_steps = int(self.stp_per_inch_f * float(dis_to_move))

            for steps in range(move_fence_steps):
                if GPIO.input(self.fenceendpos):
                    GPIO.cleanup()
                    return self.MAX_f
                GPIO.output(self.DIR_f, self.CW_f)
                GPIO.output(self.STEP_f, GPIO.HIGH)
                sleep(self.fdelay)
                GPIO.output(self.STEP_f, GPIO.LOW)
                sleep(self.fdelay)
                GPIO.cleanup()
                return new_position

        elif start_position > new_position:
            dis_to_move = start_position - new_position

            move_fence_steps = int(self.stp_per_inch_f * dis_to_move)
            for steps in range(move_fence_steps):
                if GPIO.input(self.fencezero):
                    GPIO.cleanup()
                    return self.MIN_f
                GPIO.output(self.DIR_f, self.CCW_f)
                GPIO.output(self.STEP_f, GPIO.HIGH)
                sleep(self.fdelay)
                GPIO.output(self.STEP_f, GPIO.LOW)
                sleep(self.fdelay)
                GPIO.cleanup()
                return new_position
        elif start_position == new_position:
            return new_position

        # reset things for next function
        GPIO.cleanup()

    def change_angle(self, new_position, start_position):
        # setup variables

        # task to complete first
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.DIR_a, GPIO.OUT)
        GPIO.setup(self.STEP_a, GPIO.OUT)
        GPIO.setup(self.angle0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.angle45, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        if float(start_position) < float(new_position):
            dis_to_move = float(new_position) - float(start_position)

            move_angle_steps = int(self.stp_per_inch_a * float(dis_to_move))

            for steps in range(move_angle_steps):
                if GPIO.input(self.angle45):
                    GPIO.cleanup()
                    return self.MIN_a
                GPIO.output(self.DIR_a, self.CW_a)
                GPIO.output(self.STEP_a, GPIO.HIGH)
                sleep(self.adelay)
                GPIO.output(self.STEP_a, GPIO.LOW)
                sleep(self.adelay)
                GPIO.cleanup()
                return new_position

        elif float(start_position) > float(new_position):
            dis_to_move = float(start_position) - float(new_position)

            move_angle_steps = int(self.stp_per_inch_a * float(dis_to_move))
            for steps in range(move_angle_steps):
                if GPIO.input(self.angle0):
                    GPIO.cleanup()
                    return self.MAX_a
                GPIO.output(self.DIR_a, self.CCW_a)
                GPIO.output(self.STEP_a, GPIO.HIGH)
                sleep(self.adelay)
                GPIO.output(self.STEP_a, GPIO.LOW)
                sleep(self.adelay)
                GPIO.cleanup()
                return new_position

        elif start_position == new_position:
            return new_position

        # reset things for next function
        GPIO.cleanup()
        # C_angle_e.delete(0,END)
        # C_angle_e.insert(0, str(new_position))

    def move_blade(self, new_position, start_position):
        # setup variables

        # task to complete first
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.DIR_h, GPIO.OUT)
        GPIO.setup(self.STEP_h, GPIO.OUT)
        GPIO.setup(self.heightzero, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.heightend, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        if float(start_position) < float(new_position):
            dis_to_move = float(new_position) - float(start_position)

            move_height_steps = int(self.stp_per_inch_h * float(dis_to_move))

            for steps in range(move_height_steps):
                if GPIO.input(self.heightend):
                    GPIO.cleanup()
                    return self.MAX_h
                GPIO.output(self.DIR_h, self.CW_h)
                GPIO.output(self.STEP_h, GPIO.HIGH)
                sleep(self.hdelay)
                GPIO.output(self.STEP_h, GPIO.LOW)
                sleep(self.hdelay)
                GPIO.cleanup()
                return new_position

        elif float(start_position) > float(new_position):
            dis_to_move = float(start_position) - float(new_position)

            move_height_steps = int(self.stp_per_inch_h * float(dis_to_move))
            for steps in range(move_height_steps):
                if GPIO.input(self.heightzero):
                    GPIO.cleanup()
                    return self.MIN_h
                GPIO.output(self.DIR_h, self.CCW_h)
                GPIO.output(self.STEP_h, GPIO.HIGH)
                sleep(self.hdelay)
                GPIO.output(self.STEP_h, GPIO.LOW)
                sleep(self.hdelay)
                GPIO.cleanup()
                return new_position

        elif start_position == new_position:
            return new_position

        # C_height_e.delete(0,END)
        # C_height_e.insert(0, str(new_position))
