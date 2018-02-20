"""

Author: Tiarnan Rice
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


# class EventHandler(object):


def main():
    root = tkinter.Tk()
    root.title = "ricet pc"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800,
                            height=500)
    canvas.grid(columnspan=2)

    root.mainloop()


main()
