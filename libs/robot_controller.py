"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    # DONE: Implement the Snatch3r class as needed when working the sandox
    # exercises
    # (and delete these comments)
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor(ev3.INPUT_1)
        self.running = False
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        assert self.pixy
        assert self.ir_sensor
        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor
        # assert self.touch_sensor

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives forward or backwards at the specified speed for the number of inches.
         If inches_target is negative, it drives backwards. """
        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        left_sp = speed_deg_per_second
        right_sp = left_sp
        d = inches_target
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = d * degrees_per_inch
        self.left_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=left_sp,
            stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=right_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        left_sp = turn_speed_sp
        right_sp = turn_speed_sp

        d = 4.7
        turn_sp = d * degrees_to_turn

        self.left_motor.run_to_rel_pos(position_sp=-turn_sp,
                                       speed_sp=left_sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.run_to_rel_pos(position_sp=turn_sp,
                                        speed_sp=right_sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # ev3.Sound.beep().wait()

    def arm_calibration(self):
        """
        Runs the arm up until the touch sensor is hit then back to the bottom again, beeping at both locations.
        Once back at in the bottom position, gripper open, set the absolute encoder position to 0.  You are calibrated!
        The Snatch3r arm needs to move 14.2 revolutions to travel from the touch sensor to the open position.

        """
        self.arm_motor.run_forever(speed_sp=900)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0
        # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        """
        Moves the Snatch3r arm to the up position.

        """
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        """
        Moves the Snatch3r arm to the down position.
        """
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes
        # running
        ev3.Sound.beep()

    def loop_forever(self):
        """provides a running variable to loop code until self.running is set to False"""
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        """Halts all motors on the EV3 Robot and setes running variable to False"""
        self.running = False
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def drive_forward(self, left_speed, right_speed):
        """Drives the robot forward with each motor moving at the specified speed.
            Both speed parameters should be positive."""
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def drive_backwards(self, left_speed, right_speed):
        """Drives the robot backward with each tread moving at the specified speed.
            Both speed parameters should be positive."""
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def turn_right(self, left_speed, right_speed):
        """Turns Robot in place to the right; both speed parameters should be positive"""
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def turn_left(self, left_speed, right_speed):
        """Turns Robot in place to the left; both speed parameters should be positive"""
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def stop(self):
        """Halts all motors on the robot. Does not set running variable to False."""
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def seek_beacon(self):
        """
            Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
            If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

            """
        beacon_seeker = ev3.BeaconSeeker()  # Assumes remote is set to channel 1

        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if abs(current_distance) <= 1:
                        self.drive_inches(4.5, forward_speed)
                        # self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
                        # self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

                        return True
                    if abs(current_distance) > 1:
                        print('forward')
                        self.drive_forward(forward_speed, forward_speed)

                elif 2 < abs(current_heading) < 10:
                    if current_heading < -0.5:
                        print("left")
                        self.turn_left(turn_speed, forward_speed)
                    if current_heading > 0.5:
                        print("right")
                        self.turn_right(forward_speed, turn_speed)

                elif abs(current_heading) >= 10:
                    print("heading is too far off")

            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False
