import mqtt_remote_method_calls as com
import robot_controller as robo


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
    print("RICET EV3")
    print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")

    robot = robo.Snatch3r()
    dc = DataContainer()
    command_handler = CommandHandler(robot)
    mqtt_client = com.MqttClient(command_handler)
    mqtt_client.connect_to_pc()

    while not robot.touch_sensor.is_pressed and dc.running:
        print('running')

    print("Goodbye!")


class CommandHandler:
    def __init__(self, robot):
        self.robot = robot
        self.commands = []

    def receive_commands(self, commands):
        self.commands = commands
        print(self.commands)

    def run_commands(self):
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
            x = self.robot.pixy.value(1)
            if x < 150:
                self.robot.turn_left(100, 100)
            elif x > 170:
                self.robot.turn_right(100, 100)
            elif x >= 150 and x <= 170:
                self.robot.stop()
                beacon = True

        distance = self.robot.pixy.value(3) * 1

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
