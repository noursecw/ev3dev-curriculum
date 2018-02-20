"""
Robot code for csse120 project.
Author: Tiarnan Rice
"""

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
    print("RICET EV3")
    print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")

    robot = robo.Snatch3r()
    command_handler = CommandHandler(robot)
    mqtt_client = com.MqttClient(command_handler)
    command_handler.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()

    while not robot.touch_sensor.is_pressed:
        print('', end='')

    print("Goodbye!")


class CommandHandler:
    """Handles incoming mqtt commands."""
    def __init__(self, robot):
        self.robot = robot
        self.commands = []
        self.mqtt_client = None

    def receive_commands(self, commands):
        """Creates new list to store incoming commands"""
        self.commands = commands
        print(self.commands)

    def run_commands(self):
        """Runs stored commands, checking which command it is then calling
        the appropriate function in robot_controller"""
        beacon = False
        for i in range(len(self.commands)):
            if self.commands[i] == 'forward_10':
                self.forward_10()
            elif self.commands[i] == 'forward_20':
                self.forward_20()
            elif self.commands[i] == 'backward_10':
                self.backward_10()
            elif self.commands[i] == 'backward_20':
                self.backward_20()
            elif self.commands[i] == 'turn_right_90':
                self.turn_right_90()
            elif self.commands[i] == 'turn_left_90':
                self.turn_left_90()
            elif self.commands[i] == 'turn_right_45':
                self.turn_right_45()
            elif self.commands[i] == 'turn_left_45':
                self.turn_left_45()
            elif self.commands[i] == 'turn_180':
                self.turn_180()
            else:
                print('Not a command')

        while not beacon:
            print('searching')
            x = self.robot.pixy.value(1)
            if x < 150:
                self.robot.turn_left(100, 100)
            elif x > 170:
                self.robot.turn_right(100, 100)
            elif x >= 150 and x <= 170:
                self.robot.stop()
                beacon = True

        distance = (self.robot.pixy.value(3) ** 2) * 0.06 + \
                   self.robot.pixy.value(3) * 4.42 - 3.17
        print(distance)

        self.mqtt_client.send_message('on_distance_receive', [distance])

    def forward_10(self):
        self.robot.drive_inches(10, 300)

    def forward_20(self):
        self.robot.drive_inches(20, 300)

    def backward_10(self):
        self.robot.drive_inches(-10, 300)

    def backward_20(self):
        self.robot.drive_inches(-20, 300)

    def turn_right_90(self):
        self.robot.turn_degrees(-90, 300)

    def turn_left_90(self):
        self.robot.turn_degrees(90, 300)

    def turn_right_45(self):
        self.robot.turn_degrees(-45, 300)

    def turn_left_45(self):
        self.robot.turn_degrees(45, 300)

    def turn_180(self):
        self.robot.turn_degrees(180, 300)


main()
