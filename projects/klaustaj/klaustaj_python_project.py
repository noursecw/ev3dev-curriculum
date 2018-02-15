import tkinter
from tkinter import ttk


def main():
    start = Waypoint(0, 0)
    waypoint = Waypoint(0, 0)

    root = tkinter.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    goto_and_retrieve_button = ttk.Button(frame, text="Go To and Retrieve")
    goto_and_retrieve_button.grid()
    goto_and_retrieve_button['command'] = lambda: goto(waypoint,
                                                       speed_entry.get(),
                                                       retrieve=True)

    goto_button = ttk.Button(frame, text="Go To")
    goto_button.grid()
    goto_button['command'] = lambda: goto(waypoint, speed_entry.get)

    speed_entry = ttk.Entry(frame)
    speed_entry.insert(0, "500")
    speed_entry.grid()

    return_to_base_button = ttk.Button(frame, text="Return to Base")
    return_to_base_button.grid()
    return_to_base_button['command'] = lambda: goto(start, speed_entry.get)

    waypoint_canvas = tkinter.Canvas(frame, width=200, height=150)
    waypoint_canvas.grid()
    waypoint_canvas.bind("<Button-1>", lambda event: handle_mouse_click(
        event, waypoint))

    clear_waypoint_button = ttk.Button(frame, text="Clear Waypoint")
    clear_waypoint_button.grid()
    clear_waypoint_button['command'] = waypoint_canvas.delete("all")

    root.mainloop()


class Waypoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        print()


def goto(waypoint, speed, retrieve=False):
    print('Go To and Retrieve')
    print('waypoint = ', waypoint)
    print('speed = ', speed)
    print('retrieve = ', retrieve)


def handle_mouse_click(click_event, waypoint):
    x = click_event.x
    y = click_event.y
    r = 3
    click_event.widget.delete("all")
    click_event.widget.create_oval(x - r, y - r, x + r, y + r, fill="blue")

    waypoint.x = x
    waypoint.y = y
    # return Waypoint(click_event.x, click_event.y)


main()
