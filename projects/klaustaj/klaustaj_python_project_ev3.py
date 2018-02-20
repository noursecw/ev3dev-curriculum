"""
Aaron Klaustermeier Final Project EV3 Code

This code runs commands sent through mqtt by the pc and continuously sends
the IR sensor readings to the pc.
"""
import mqtt_remote_method_calls as com
import robot_controller as robo
import time
import ev3dev.ev3 as ev3


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    ev3.Sound.beep()

    while not robot.touch_sensor.is_pressed:
        mqtt_client.send_message("get_ir_dist", [int(
            robot.ir_sensor.proximity)])

        time.sleep(0.01)


main()