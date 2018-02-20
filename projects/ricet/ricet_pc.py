"""

Author: Tiarnan Rice
"""

import tkinter
from tkinter import ttk
from tkinter import messagebox

import random

import mqtt_remote_method_calls as com


class UIhandler(object):
    def __init__(self):
        self.commands = []
        self.commandlist = ['forward_10', 'forward_20',
                            'turn_right_90', 'turn_right_45',
                            'turn_left_90', 'turn_left_45', 'turn_180',
                            'backward_10', 'backward_20']
        self.new_commands(event=None, uicommands=None)

    def new_commands(self, event, uicommands):
        print('new commands')
        self.commands = []
        for _ in range(5):
            x = random.randrange(0, 8)
            self.commands.append(self.commandlist[x])
        print(self.commands)

        if uicommands is not None:
            uicommands.set_commands()

    def on_distance_recieve(self, distance):
        print("Made it to ", distance, " inches away")
        messagebox.showinfo(title='Congratulations!', message='You made '
                                                              'it to %d inches away!' % distance)

    def send_commands(self, event, mqtt_client, uicommands):
        print("Sending commands")
        send_commands = []
        for i in range(len(uicommands.commandVals)):
            send_commands.append(uicommands.commandVals[i].get())

        mqtt_client.send_message('receive_commands', send_commands)

    def run_commands(self, event, mqtt_client):
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

    uicommands = UIcommands(handler, main_frame)

    instructions = ttk.Label(main_frame,
                             text="Try to get as close to the beacon "
                                  "as possible!")
    instructions.grid(pady=10, row=1)

    newcommands = ttk.Button(main_frame, padding=4, text='New commands')
    newcommands.bind("<Button-1>", lambda event: handler.new_commands(event,
                                                                      uicommands))
    newcommands.grid(sticky='W', pady=10, row=2)

    sendcommands = ttk.Button(main_frame, padding=4, text='Send commands')
    sendcommands.bind("<Button-1>", lambda event: handler.send_commands(
        event, mqtt_client, uicommands))
    sendcommands.grid(row=4, sticky='W', pady=10)

    runcommands = ttk.Button(main_frame, padding=4, text='Run')
    runcommands.bind("<Button-1>",
                     lambda event: handler.run_commands(event, mqtt_client))
    runcommands.grid(row=5, sticky='W', pady=10)

    root.mainloop()


class UIcommands():
    def __init__(self, handler, frame):
        self.frame = frame
        self.handler = handler
        self.c1 = tkinter.StringVar(frame)
        self.c1.set(handler.commands[0])
        self.command1 = tkinter.OptionMenu(frame, self.c1, *handler.commands)
        self.command1.grid(row=3, pady=10, column=0)

        self.c2 = tkinter.StringVar(frame)
        self.c2.set(handler.commands[1])
        self.command2 = tkinter.OptionMenu(frame, self.c2, *handler.commands)
        self.command2.grid(row=3, pady=10, column=1)

        self.c3 = tkinter.StringVar(frame)
        self.c3.set(handler.commands[2])
        self.command3 = tkinter.OptionMenu(frame, self.c3, *handler.commands)
        self.command3.grid(row=3, pady=10, column=2)

        self.c4 = tkinter.StringVar(frame)
        self.c4.set(handler.commands[3])
        self.command4 = tkinter.OptionMenu(frame, self.c4, *handler.commands)
        self.command4.grid(row=3, pady=10, column=3)

        self.c5 = tkinter.StringVar(frame)
        self.c5.set(handler.commands[4])
        self.command5 = tkinter.OptionMenu(frame, self.c5, *handler.commands)
        self.command5.grid(row=3, pady=10, column=4)

        self.commands = [self.command1, self.command2, self.command3,
                         self.command4, self.command5]
        self.commandVals = [self.c1, self.c2, self.c3, self.c4, self.c5]

    def set_commands(self):
        print('set commands ui')
        self.c1.set(self.handler.commands[0])
        self.command1 = tkinter.OptionMenu(self.frame, self.c1,
                                           *self.handler.commands)
        self.command1.grid(row=3, pady=10, column=0)

        self.c2.set(self.handler.commands[1])
        self.command2 = tkinter.OptionMenu(self.frame, self.c2,
                                           *self.handler.commands)
        self.command2.grid(row=3, pady=10, column=1)

        self.c3.set(self.handler.commands[2])
        self.command3 = tkinter.OptionMenu(self.frame, self.c3,
                                           *self.handler.commands)
        self.command3.grid(row=3, pady=10, column=2)

        self.c4.set(self.handler.commands[3])
        self.command4 = tkinter.OptionMenu(self.frame, self.c4,
                                           *self.handler.commands)
        self.command4.grid(row=3, pady=10, column=3)

        self.c5.set(self.handler.commands[4])
        self.command5 = tkinter.OptionMenu(self.frame, self.c5,
                                           *self.handler.commands)
        self.command5.grid(row=3, pady=10, column=4)

        self.commands = [self.command1, self.command2, self.command3,
                         self.command4, self.command5]
        self.commandVals = [self.c1, self.c2, self.c3, self.c4, self.c5]


main()
