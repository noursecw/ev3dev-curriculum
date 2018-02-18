"""Accepts human input via MQTT or IR remote for drive and arm functions. When complete, the beacon button on the IR
    remote will repeat the human input autonomously. If an obstacle presents itself, the robot will avoid it and resume
    its original path. As the robot operates, it wil, play tones based on values of the color sensor."""

import robot_controller_noursecw as robo
import ev3dev.ev3 as ev3
import math

robot = robo.Snatch3r


def main():


def mqtt_control():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


def play_note(color):
    """takes a color (type = int) and plays a note. Returns nothing."""
    freqs = [130.81, 146.83, 164.81, 196, 220, 261.63]  # major pentatonic, C3-C4
    if color == ev3.ColorSensor.COLOR_RED:
        ev3.Sound.tone(freqs[1])
    elif color == ev3.ColorSensor.COLOR_YELLOW:
        ev3.Sound.tone(freqs[2])
    elif color == ev3.ColorSensor.COLOR_GREEN:
        ev3.Sound.tone(freqs[3])
    elif color == ev3.ColorSensor.COLOR_BLUE:
        ev3.Sound.tone(freqs[4])
    elif color == ev3.ColorSensor.COLOR_BROWN:
        ev3.Sound.tone(freqs[5])
    elif color == ev3.ColorSensor.COLOR_BLACK:
        ev3.Sound.tone(freqs[6])


main()
