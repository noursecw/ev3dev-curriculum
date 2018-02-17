import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import math
import time


class MyDelegate(object):
    def __init__(self):
        self.pixy_x = 0
        self.pixy_y = 0

    def pixy_coords(self, x, y):
        self.pixy_x = x
        self.pixy_y = y


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    start = Point(200, 450)
    waypoint = Point(0, 0)

    root = tkinter.Tk()
    root.title('Autonomous Retrieval Robot Command Window')
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    goto_and_retrieve_button = ttk.Button(frame, text="Go To and Retrieve")
    goto_and_retrieve_button.grid(row=2, column=3)
    goto_and_retrieve_button['command'] = lambda: goto(my_delegate, waypoint,
                                                       start,
                                                       speed_entry.get(),
                                                       retrieve=True)

    goto_button = ttk.Button(frame, text="Go To")
    goto_button.grid(row=2, column=4)
    goto_button['command'] = lambda: goto(my_delegate, waypoint, start,
                                          speed_entry.get())

    speed_label = ttk.Label(frame, text='Speed:')
    speed_label.grid(row=2, column=1)

    speed_entry = ttk.Entry(frame, width=5)
    speed_entry.insert(0, "500")
    speed_entry.grid(row=2, column=2)

    return_to_base_button = ttk.Button(frame, text="Return to Base")
    return_to_base_button.grid(row=2, column=5)
    return_to_base_button['command'] = lambda: goto(my_delegate, start,
                                                    waypoint,
                                                    speed_entry.get())

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


class Robot(object):
    def __init__(self, start, wp):
        self.angle = 0
        self.cl = start.clone()
        self.start = start.clone()
        self.wp = wp.clone()

        delta_x = wp.x - start.x
        delta_y = wp.y - start.y
        self.wp_angle = math.tan(delta_x / delta_y)

    def angle_to_wp(self):
        delta_x = self.wp.x - self.cl.x
        delta_y = self.wp.y - self.cl.y
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


def handle_mouse_click(click_event, waypoint):
    x = click_event.x
    y = click_event.y
    r = 3
    click_event.widget.delete("all")
    click_event.widget.create_oval(x - r, y - r, x + r, y + r, fill="blue")

    waypoint.x = x
    waypoint.y = y


def goto(my_delegate, wp, start, speed, retrieve=False):
    """
    Recieves a waypoint and speed. Robot then attempts to travel to waypoint in
    a straight line, but swerves to avoid obstacles when they are detected with
    the pixy camera.
    """
    # print('Go To and Retrieve')
    # print('waypoint = ', waypoint)
    # print('speed = ', speed)
    # print('retrieve = ', retrieve)
    threshold = 50

    v_robot = Robot(wp, start)

    while True:
        turn_degrees(angle_to_wp(wp, start))

        while not abs(my_delegate.pixy_x - 160) < threshold:
            drive_forward()

            time.sleep(0.1)
            current_location.update()

            if distance_to_wp()

        while True:
            if


def turn_degrees(mqtt_client, angle, speed):


def drive_forward():



main()
