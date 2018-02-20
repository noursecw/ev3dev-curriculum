"""
This project is an autonomous retrieval/waypoint robot. A waypont is input
to the GUI and, when the 'Go To' button is pressed, the robot wil travel to
that point, steering to avoid obstacles in its path.
"""


import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import math
import time


class MyDelegate(object):
    def __init__(self):
        self.ir_dist = 0

    def get_ir_dist(self, dist):
        self.ir_dist = dist
        print(self.ir_dist)


def main():
    """
    Tkinter code for the robot GUI.
    """
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    start = Point(200, 450)
    waypoint = Point(0, 0)

    root = tkinter.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    goto_button = ttk.Button(frame, text="Go To")
    goto_button.grid(row=2, column=4)
    goto_button['command'] = lambda: goto(mqtt_client, my_delegate, waypoint,
                                          start, int(speed_entry.get()))

    speed_label = ttk.Label(frame, text='Speed:')
    speed_label.grid(row=2, column=1)

    speed_entry = ttk.Entry(frame, width=5)
    speed_entry.insert(0, "500")
    speed_entry.grid(row=2, column=2)

    width = 400
    height = 500
    waypoint_canvas = tkinter.Canvas(frame, width=width, height=height)
    waypoint_canvas.config(background='DarkOrange3')
    waypoint_canvas.grid(columnspan=5, row=3, column=1)
    waypoint_canvas.bind("<Button-1>", lambda event: handle_mouse_click(
        event, waypoint))

    clear_waypoint_button = ttk.Button(frame, text="Clear Waypoint")
    clear_waypoint_button.grid(row=4, column=5)
    clear_waypoint_button['command'] = lambda: waypoint_canvas.delete("all")

    root.mainloop()


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Waypoint({: .1f}, {: .1f})'.format(self.x, self.y)

    def clone(self):
        return Point(self.x, self.y)


def handle_mouse_click(click_event, waypoint):
    x = click_event.x
    y = click_event.y
    r = 3
    click_event.widget.delete("all")
    click_event.widget.create_oval(x - r, y - r, x + r, y + r, fill="blue")

    waypoint.x = x
    waypoint.y = y


class Robot(object):
    def __init__(self, start, wp):
        self.angle = 0
        self.cl = start.clone()
        self.start = start.clone()
        self.wp = wp.clone()

    def angle_to_wp(self):
        delta_x = self.wp.x - self.cl.x
        delta_y = self.wp.y - self.cl.y
        print(math.tan(delta_x / delta_y))
        return math.tan(delta_x / delta_y)

    def distance_to_wp(self):
        delta_x = self.wp.x - self.cl.x
        delta_y = self.wp.y - self.cl.y
        return math.sqrt(delta_x ** 2 + delta_y ** 2)

    def update_cl(self, speed, delta_t):
        speed_inps = 0.0103 * speed + 0.3152
        delta_x = speed_inps * delta_t * math.sin(self.angle)
        delta_y = speed_inps * delta_t * math.cos(self.angle)
        self.cl.x = self.cl.x + delta_x
        self.cl.y = self.cl.y + delta_y


def goto(mqtt_client, my_delegate, wp, start, speed):
    """
    Recieves a waypoint and speed. Robot then attempts to travel to waypoint in
    a straight line, but swerves to avoid obstacles when they are detected with
    the pixy camera.
    """
    # print('Go To')
    # print('waypoint = ', wp)
    # print('speed = ', speed)

    v_robot = Robot(wp, start)

    threshold = 40
    target_dist = 10

    while True:
        turn_degrees(mqtt_client, v_robot.angle_to_wp() - v_robot.angle,
                     speed)

        time.sleep(3)

        v_robot.angle = v_robot.angle_to_wp()

        drive_forward(mqtt_client, speed)

        while True:
            print('looking for object')

            if my_delegate.ir_dist < threshold:
                avoid(mqtt_client, my_delegate, v_robot, speed,
                      threshold)
                break

            delta_t = 0.1
            time.sleep(delta_t)
            v_robot.update_cl(speed, delta_t)

            if v_robot.distance_to_wp() < target_dist:
                print("Waypoint Reached")
                return


def avoid(mqtt_client, my_delegate, v_robot, speed, threshold):
    """
    This is called when the robot detects an object in the way. It steeres
    until it doesnt see it, then it steers a little further, drives forward,
    and exits the function.
    
    :param mqtt_client:
    :param my_delegate:
    :param v_robot:
    :param speed:
    :param threshold:
    :return:
    """
    while my_delegate.ir_dist < threshold:
        turn_degrees(mqtt_client, 10, speed)
        v_robot.angle = v_robot.angle + 10

    turn_degrees(mqtt_client, 10, speed)
    v_robot.angle = v_robot.angle + 10

    drive_forward(mqtt_client, speed)
    time.sleep(3)
    v_robot.update_cl(speed, 3)


def turn_degrees(mqtt_client, angle, speed):
    print('turn_degrees')
    mqtt_client.send_message("turn_degrees", [angle, int(speed)])


def drive_forward(mqtt_client, speed):
    print('drive_forward')
    mqtt_client.send_message("drive_forward",
                             [int(speed), int(speed)])


main()
