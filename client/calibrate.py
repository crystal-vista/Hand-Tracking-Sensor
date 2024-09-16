from multiprocessing import Process
from tkinter import *
from tkinter import ttk

from client_config import host, port
from tracker_loop import tracker_loop
from socket_client import SocketClient

def run_cv():
    tracker_loop()

def run_calibration_gui(client: SocketClient):
    def set_position(axis):
        x = horizontal_slider.get()
        y = vertical_slider.get()
        if axis == "horizontal":
            print(f"horizontal angle: {x}")
            sb_horizontal.set(x)
        elif axis == "vertical":
            print(f"vertical angle: {y}")
            sb_vertical.set(y)
        client.send_state(x, y, True)

    def print_position():
        print(f"vertical: {vertical_slider.get()}, horizontal: {horizontal_slider.get()}")
    
    def spinbox_change(axis):
        if axis == "horizontal":
            horizontal_slider.set(sb_horizontal.get())
        elif axis == "vertical":
            vertical_slider.set(sb_vertical.get())
        print("spibox", axis)

    root = Tk()

    # MENU - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - >
    menubar = Menu(root)

    menubar.add_radiobutton(label='Print coordinates', command=print_position)

    root.config(menu=menubar)

    # CONTENT - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - >
    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N,E,S,W))
    
    # Horizontal Section
    horizontal_section = ttk.Frame(mainframe)
    horizontal_section.grid(column=0, row=0, pady=(10,0))

    ttk.Label(horizontal_section, text="Horizontal").grid(column=0, row=0)
    sb_horizontal = ttk.Spinbox(horizontal_section, from_=0.0, to=1.0, increment=0.05, command=lambda _=None: spinbox_change("horizontal"))
    sb_horizontal.grid(column=1, row=0, padx=(5,0))
    sb_horizontal.bind('<Return>', lambda _=None: spinbox_change("horizontal"))

    # Vertical Section
    vertical_section = ttk.Frame(mainframe)
    vertical_section.grid(column=1, row=0, pady=(10,0), padx=(10,0))

    ttk.Label(vertical_section, text="Vertical").grid(column=0, row=0)
    sb_vertical = ttk.Spinbox(vertical_section, from_=0.0, to=1.0, increment=0.05, command=lambda _=None: spinbox_change("vertical"))
    sb_vertical.grid(column=1, row=0, padx=(5,0))
    sb_vertical.bind('<Return>', lambda _=None: spinbox_change("vertical"))

    horizontal_slider = ttk.Scale(mainframe, orient=HORIZONTAL, from_=0, to=1, value=0.5, command=lambda _: set_position("horizontal"))
    horizontal_slider.grid(column=0, row=1, pady=10, padx=(20, 10), sticky=(W,E))

    vertical_slider = ttk.Scale(mainframe, orient=VERTICAL, from_=1, to=0, value=0.5, command=lambda _: set_position("vertical"))
    vertical_slider.grid(column=1, row=1, pady=10, padx=(5,0), sticky=(N,S))

    ttk.Sizegrip(root).grid(column=999, row=999, sticky=(S,E))

    root.title('Manual Calibration Tool')
    root.minsize(400, 400)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe.rowconfigure(0, weight=1)
    mainframe.rowconfigure(1, weight=2)
    mainframe.columnconfigure(0, weight=1)

    root.geometry('620x500')
    root.mainloop()


if __name__ == "__main__":
    with SocketClient(host=host, port=port) as client:
        p = Process(target=run_cv)
        p.start()
        run_calibration_gui(client)
        p.join()

