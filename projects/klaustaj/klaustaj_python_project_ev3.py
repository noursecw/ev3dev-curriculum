import mqtt_remote_method_calls as com
import robot_controller as robo
import time


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    while not robot.touch_sensor.is_pressed:
        mqtt_client.send_message("pixy_coords", [robot.pixy.value(
            1), robot.pixy.value(2)])

        time.sleep(0.01)


main()
