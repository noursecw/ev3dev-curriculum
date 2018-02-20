"""

Author: Tiarnan Rice
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


# class EventHandler(object):
class UIhandler(object):
    def new_commands(self, event):
        print('new commands')


def main():
    handler = UIhandler()
    root = tkinter.Tk()
    root.title = "ricet pc"

    main_frame = ttk.Frame(root, padding=5, borderwidth=10)
    main_frame.grid()

    instructions = ttk.Label(main_frame,
                             text="Try to get as close to the beacon "
                                  "as possible!")
    instructions.grid(pady=10)

    button = ttk.Button(main_frame, padding=4, text='New commands')
    button.bind("<Button-1>", lambda event: handler.new_commands(event))
    button.grid(sticky='W')
    

    root.mainloop()


main()
