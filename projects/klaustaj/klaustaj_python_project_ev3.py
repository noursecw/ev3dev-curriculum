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
        mqtt_client.send_message("pixy_coords", [int(robot.pixy.value(1)),
                                                 int(robot.pixy.value(2))])

        mqtt_client.send_message("ir_dist", [int(robot.pixy.value(
            1)), int(robot.pixy.value(2))])

        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


main()
