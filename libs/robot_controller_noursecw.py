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
    """Commands for the Snatch3r robot that might be useful in many different programs.
        Use *_amnesia methods for memory replay to avoid infinite loops."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)  # output D for broken robot
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor(ev3.INPUT_1)
        self.running = False
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.memory = []  # format: [(action type, time, (parameters))]

        assert self.pixy
        assert self.ir_sensor
        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor
        # assert self.touch_sensor

    def drive_inches(self, inches_target, speed_deg_per_second):  # action type: 1
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

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):  # 2
        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        self.memory += [(2, time.time(), degrees_to_turn, turn_speed_sp)]

        left_sp = turn_speed_sp
        right_sp = turn_speed_sp

        d = 4.7
        turn_sp = d * degrees_to_turn

        self.left_motor.run_to_rel_pos(position_sp=turn_sp,
                                       speed_sp=left_sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.run_to_rel_pos(position_sp=turn_sp,
                                        speed_sp=right_sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_calibration(self):  # 3
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

    def arm_up(self):  # 4
        """
        Moves the Snatch3r arm to the up position.
        """

        self.memory += [(4, time.time())]

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_up_amnesia(self):  # 4
        """
        Moves the Snatch3r arm to the up position.
        Does not record action to memory.
        """
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):  # 5
        """
        Moves the Snatch3r arm to the down position.
        """

        self.memory += [(5, time.time())]

        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes
        # running
        ev3.Sound.beep()

    def arm_down_amnesia(self):  # 5
        """
        Moves the Snatch3r arm to the down position. Does not record action to memory.
        """
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes
        # running
        ev3.Sound.beep()

    def loop_forever(self):  # 6
        """provides a running variable to loop code until self.running is set to False"""
        self.running = True
        rc1 = ev3.RemoteControl(channel=1)
        while self.running:
            time.sleep(0.1)
            if rc1.beacon:
                self.running = False
                break

    def shutdown(self):  # 7
        """Halts all motors on the EV3 Robot and setes running variable to False"""

        self.memory += [(7, time.time())]

        self.running = False
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def shutdown_amnesia(self):  # 7
        """Halts all motors on the EV3 Robot and setes running variable to False. Does not record action to memory"""

        self.running = False
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def drive_forward(self, left_speed, right_speed):  # 8
        """Drives the robot forward with each motor moving at the specified speed.
            Both speed parameters should be positive."""

        self.memory += [(8, time.time(), left_speed, right_speed)]

        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def drive_forward_amnesia(self, left_speed, right_speed):  # 8
        """Drives the robot forward with each motor moving at the specified speed.
            Both speed parameters should be positive. Does not record action to memory."""

        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def drive_backwards(self, left_speed, right_speed):  # 9
        """Drives the robot backward with each tread moving at the specified speed.
            Both speed parameters should be positive."""

        self.memory += [(9, time.time(), left_speed, right_speed)]

        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def turn_right(self, left_speed, right_speed):  # 10
        """Turns Robot in place to the right; both speed parameters should be positive"""

        self.memory += [(9, time.time(), left_speed, right_speed)]

        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def turn_left(self, left_speed, right_speed):  # 11
        """Turns Robot in place to the left; both speed parameters should be positive"""

        self.memory += [(10, time.time(), left_speed, right_speed)]

        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def stop(self):  # 11
        """Halts all motors on the robot. Does not set running variable to False."""

        self.memory += [(11, time.time())]

        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def stop_amnesia(self):  # 11
        """Halts all motors on the robot. Does not set running variable to False. Does not record action to memory."""
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def drive_timed(self, left_speed, right_speed, running_time):
        """drives for the specified amount of time and then halts. DOES NOT record to memory."""
        ti = time.time()
        while (running_time - (time.time() - ti)) > 0:  # (while elapsed time is less than the running time)
            # print("driving")
            self.drive_forward_amnesia(left_speed, right_speed)
            time.sleep(0.01)
        self.stop_amnesia()

    def stop_timed(self, stop_time):
        """stops for the specified amount of time; used in playback. Does not record action to memory."""
        ti = time.time()
        while (stop_time - (time.time() - ti)) > 0:  # (while elapsed time is less than the running time)
            # print("driving")
            self.stop_amnesia()
            time.sleep(0.01)


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

    def memory_replay(self):
        """repeats the actions performed by the user."""
        mem = self.memory
        length = len(mem)
        # time_elapsed = 0
        for k in range(length):
            action = mem[k]

            if action[0] == 4:
                self.arm_up_amnesia()
            elif action[0] == 5:
                self.arm_down_amnesia()
            elif action[0] == 7:
                self.shutdown_amnesia()
            elif action[0] == 8:  # drive_forward handles all drive actions by alteration of the speed signs.
                # print("replay drive")
                running_time = mem[k + 1][1] - action[1]  # time until next action
                # print(action[1], mem[k + 1][1], running_time, action[2], action[3])
                self.drive_timed(action[2], action[3], running_time)
            elif action[0] == 11:
                if action.index != len(mem) - 1:  # (if the stop action is not the final action)
                    stop_time = mem[k + 1][1] - action[1]  # time until next action
                    self.stop_timed(stop_time)
                else:
                    self.stop_amnesia()


        ev3.Sound.beep()
        self.stop_amnesia()
