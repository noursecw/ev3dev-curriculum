#!/usr/bin/env python3
"""
This script utilizes code from sandbox/noursecw/mqtt/m5_pc_remote_drive.py (altered to momentary buttons)
 Running it allows remote control of the EV3 robot via GUI utilizing MQTT.
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class DataContainer:
    """allows access to variables in main() without resorting to global declarations."""
    def __init__(self):
        self.right_speed_entry = None
        self.left_speed_entry = None
        self.mqtt_client = None


def main():
    dc = DataContainer

    dc.mqtt_client = com.MqttClient()
    dc.mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    dc.left_speed_entry = ttk.Entry(main_frame, width=8)
    dc.left_speed_entry.insert(0, "600")
    dc.left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    dc.right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    dc.right_speed_entry.insert(0, "600")
    dc.right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button.bind('<ButtonPress-1>', drive_forward_event)
    forward_button.bind('<ButtonRelease-1>', stop_event)

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button.bind('<ButtonPress-1>', drive_left_event)
    left_button.bind('<ButtonRelease-1>', stop_event)

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stop(dc.mqtt_client)
    root.bind('<space>', lambda event: stop(dc.mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button.bind('<ButtonPress-1>', drive_right_event)
    right_button.bind('<ButtonRelease-1>', stop_event)

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button.bind('<ButtonPress-1>', drive_back_event)
    back_button.bind('<ButtonRelease-1>', stop_event)

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(dc.mqtt_client)
    root.bind('<u>', lambda event: send_up(dc.mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(dc.mqtt_client)
    root.bind('<j>', lambda event: send_down(dc.mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(dc.mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(dc.mqtt_client, True))

    root.mainloop()


# event handlers for momentary buttons:


def drive_forward_event(event):
    dc = DataContainer
    # print("drive forward")
    drive_forward(dc.mqtt_client, dc.left_speed_entry, dc.right_speed_entry)


def drive_back_event(event):
    dc = DataContainer
    # print("drive backward")
    drive_backwards(dc.mqtt_client, dc.left_speed_entry, dc.right_speed_entry)


def drive_right_event(event):
    dc = DataContainer
    # print("turn right")
    turn_right(dc.mqtt_client, dc.left_speed_entry, dc.right_speed_entry)


def drive_left_event(event):
    dc = DataContainer
    # print("turn left")
    turn_left(dc.mqtt_client, dc.left_speed_entry, dc.right_speed_entry)


def stop_event(event):
    dc = DataContainer
    # print("stop")
    stop(dc.mqtt_client)

# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------

def drive_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive forward")
    mqtt_client.send_message("drive_forward", [int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])


def turn_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("turn left")
    mqtt_client.send_message("drive_forward", [-int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])


def stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def turn_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("turn right")
    mqtt_client.send_message("drive_forward", [int(left_speed_entry.get()),
                                               -int(right_speed_entry.get())])


def drive_backwards(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive_backwards")
    mqtt_client.send_message("drive_forward", [-int(left_speed_entry.get()),
                                               -int(right_speed_entry.get())])


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
