"""

Author: Tiarnan Rice
"""

import tkinter
from tkinter import ttk

import random

import mqtt_remote_method_calls as com


# class EventHandler(object):
class UIhandler(object):
    def __init__(self):
        self.commands = []
        self.commandlist = ['forward_10', 'forward_20',
                            'turn_right_90', 'turn_right_45',
                            'turn_left_90', 'turn_left_45', 'turn_180',
                            'backward_10', 'backward_20']

    def new_commands(self, event):
        print('new commands')
        self.commands = []
        for _ in range(5):
            x = random.randrange(0, 8)
            self.commands.append(self.commandlist[x])
        print(self.commands)

    def on_distance_recieve(self, distance):
        print("Made it to ", distance, " inches away")

    def send_commands(self, mqtt_client):
        print("Sending commands")
        mqtt_client.send_message('recieve_commands', [self.commands])

    def run_commands(self, mqtt_client):
        print("Running commands")
        mqtt_client.send_message('run_commands', [])


def main():
    handler = UIhandler()
    mqtt_client = com.MqttClient(handler)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title = "ricet pc"

    main_frame = ttk.Frame(root, padding=5, borderwidth=10)
    main_frame.grid()

    instructions = ttk.Label(main_frame,
                             text="Try to get as close to the beacon "
                                  "as possible!")
    instructions.grid(pady=10)

    newcommands = ttk.Button(main_frame, padding=4, text='New commands')
    newcommands.bind("<Button-1>", lambda event: handler.new_commands(event))
    newcommands.grid(sticky='W')

    sendcommands = ttk.Button(main_frame, padding=4, text='Send commands')
    sendcommands.bind("<Button-1>", lambda event: handler.send_commands(event))
    sendcommands.grid(sticky='W')

    root.mainloop()


main()
