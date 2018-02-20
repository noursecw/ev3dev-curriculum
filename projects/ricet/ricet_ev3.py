import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    command_handler = CommandHandler(robot)
    mqtt_client = com.MqttClient(command_handler)
    mqtt_client.connect_to_pc()


class CommandHandler:
    def __init__(self, robot):
        self.robot = robot

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


main()
