import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import math
import time
import rosegraphics as rg


class MyDelegate(object):
    def __init__(self):
        self.pixy_x = 0
        self.pixy_y = 0
        self.ir_dist = 0

    def pixy_coords(self, x, y):
        self.pixy_x = x
        self.pixy_y = y

    def ir_dist(self, dist):
        self.ir_dist = dist


def main():
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
                                          start, speed_entry)

    speed_label = ttk.Label(frame, text='Speed:')
    speed_label.grid(row=2, column=1)

    speed_entry = ttk.Entry(frame, width=5)
    speed_entry.insert(0, "500")
    speed_entry.grid(row=2, column=2)

    return_to_base_button = ttk.Button(frame, text="Return to Start")
    return_to_base_button.grid(row=2, column=5)
    return_to_base_button['command'] = lambda: goto(mqtt_client, my_delegate,
                                                    start, waypoint,
                                                    speed_entry)

    width = 400
    height = 500
    waypoint_canvas = tkinter.Canvas(frame, width=width, height=height)
    waypoint_canvas.config(background='gray')
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


def goto(mqtt_client, my_delegate, wp, start, speed_entry):
    """
    Recieves a waypoint and speed. Robot then attempts to travel to waypoint in
    a straight line, but swerves to avoid obstacles when they are detected with
    the pixy camera.
    """
    # print('Go To and Retrieve')
    # print('waypoint = ', wp)
    # print('speed = ', speed)
    # print('retrieve = ', retrieve)

    window = rg.RoseWindow(400, 500)

    v_robot = Robot(wp, start)

    threshold = 50
    target_threshold = 5
    avoid_dist = 20

    while True:
        turn_degrees(mqtt_client, v_robot.angle_to_wp() - v_robot.angle,
                     speed_entry)
        v_robot.angle = v_robot.angle_to_wp()

        while (abs(my_delegate.pixy_x - 160) < threshold) & (
                    my_delegate.ir_dist > avoid_dist):
            drive_forward(mqtt_client, speed_entry)

            delta_t = 0.1
            time.sleep(delta_t)

            cl = v_robot.cl.clone  # for v_robot graphic
            v_robot.update_cl(speed_entry, delta_t)

            line = rg.Line(cl, v_robot.cl)  # for v_robot graphic
            line.attach_to(window)  # for v_robot graphic
            window.render()  # for v_robot graphic

            if v_robot.distance_to_wp() < target_threshold:
                print("Waypoint Reached")
                return

        # if abs(my_delegate.pixy_x - 160) < threshold:
        #     if my_delegate.pixy_x <= 160:
        #         avoid(mqtt_client, my_delegate, v_robot, speed, 1,
        #               threshold, window)
        #
        #     if my_delegate.pixy_x > 160:
        #         avoid(mqtt_client, my_delegate, v_robot, speed, -1,
        #               threshold, window)

        if v_robot.distance_to_wp() < target_threshold:
            print("Waypoint Reached")
            return


def avoid(mqtt_client, my_delegate, v_robot, speed, angle_increment,
          threshold, window):
    while abs(my_delegate.pixy_x - 160) < threshold:
        turn_degrees(mqtt_client, angle_increment, speed)
        v_robot.angle = v_robot.angle + angle_increment

    while abs(v_robot.angle - v_robot.angle_to_wp) > 3:
        drive_forward(mqtt_client, speed)

        delta_t = 1
        time.sleep(delta_t)

        cl = v_robot.cl.clone()  # for v_robot graphic
        v_robot.update_cl(speed, delta_t)

        line = rg.Line(cl, v_robot.cl)  # for v_robot graphic
        line.attach_to(window)  # for v_robot graphic
        window.render()  # for v_robot graphic

        while abs(my_delegate.pixy_x - 160) > threshold:
            turn_degrees(mqtt_client, -angle_increment, speed)
            v_robot.angle = v_robot.angle - angle_increment

            if abs(v_robot.angle - v_robot.angle_to_wp) > 3:
                break


def turn_degrees(mqtt_client, angle, speed_entry):
    print('turn_degrees')
    mqtt_client.send_message("turn_degrees", [angle, int(speed_entry.get())])


def drive_forward(mqtt_client, speed_entry):
    mqtt_client.send_message("drive_forward", [int(speed_entry.get())])


main()
