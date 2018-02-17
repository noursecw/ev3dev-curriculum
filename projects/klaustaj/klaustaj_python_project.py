import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    start = Waypoint(200, 450)
    waypoint = Waypoint(0, 0)

    root = tkinter.Tk()
    root.title('Autonomous Retrieval Robot Command Window')
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    goto_and_retrieve_button = ttk.Button(frame, text="Go To and Retrieve")
    goto_and_retrieve_button.grid(row=2, column=3)
    goto_and_retrieve_button['command'] = lambda: goto(waypoint,
                                                       start,
                                                       speed_entry.get(),
                                                       retrieve=True)

    goto_button = ttk.Button(frame, text="Go To")
    goto_button.grid(row=2, column=4)
    goto_button['command'] = lambda: goto(waypoint, start, speed_entry.get())

    speed_label = ttk.Label(frame, text='Speed:')
    speed_label.grid(row=2, column=1)

    speed_entry = ttk.Entry(frame, width=5)
    speed_entry.insert(0, "500")
    speed_entry.grid(row=2, column=2)

    return_to_base_button = ttk.Button(frame, text="Return to Base")
    return_to_base_button.grid(row=2, column=5)
    return_to_base_button['command'] = lambda: goto(start, waypoint,
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


class Waypoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Waypoint({: .1f}, {: .1f})'.format(self.x, self.y)


def handle_mouse_click(click_event, waypoint):
    x = click_event.x
    y = click_event.y
    r = 3
    click_event.widget.delete("all")
    click_event.widget.create_oval(x - r, y - r, x + r, y + r, fill="blue")

    waypoint.x = x
    waypoint.y = y


def goto(wp, start, speed, retrieve=False):
    """
    Recieves a waypoint and speed. Robot then attempts to travel to waypoint in
    a straight line, but swerves to avoid obstacles when they are detected with
    the pixy camera.
    """
    # print('Go To and Retrieve')
    # print('waypoint = ', waypoint)
    # print('speed = ', speed)
    # print('retrieve = ', retrieve)

    turn_degrees(angle_to_wp(wp, start))

    while distance_to_wp() > threshold

        if pixy
            drive_forward()


def turn_degrees(mqtt_client, angle, speed):


def drive_forward():


def angle_to_wp(wp, start):
    delta_x = wp.x - start.x
    delta_y = wp.y - start.y
    return math.tan(delta_x / delta_y)


def distance_to_wp():



main()
