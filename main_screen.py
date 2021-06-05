import matplotlib
from matplotlib import style
import tkinter as tk
import CamPage, Menus

WIDTH = 1300
HEIGHT = 700
MAIN_WINDOW = "MainWindow"

style.use("ggplot")
matplotlib.use("TkAgg")


class MainScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_withdraw()
        self.Init()
        self.controls_frame()
        self.popup_menu = Menus.PopupBar(self)
        self.set_frames()

    ''' Setting Main Tk window size & styles '''

    def Init(self):
        self.bind('<Escape>', lambda e: self.on_exit())
        self.x_start_at = (self.winfo_screenwidth() / 2) - (WIDTH / 2)
        self.y_start_at = (self.winfo_screenheight() / 2) - (HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, self.x_start_at, self.y_start_at))
        self.update()
        self.canvas = tk.Canvas(self, width=self.winfo_width(), height=self.winfo_height())
        self.canvas.grid_rowconfigure(0, weight=0)
        self.canvas.grid_rowconfigure(1, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.pages = {MAIN_WINDOW: CamPage.MainWindow, "Credits": CreditWindow}
        self.overrideredirect(True)
        self.canvas.pack(fill="both", expand=True)
        self.overrideredirect(True)
        self['highlightthickness'] = 2

    '''Layout of the Tk window'''

    def controls_frame(self):
        self.update()
        self.control_fr = Menus.ToolBar(self.canvas, self, self.pages, width=self.canvas.winfo_width(), height=33, bd=0,
                                        bg='#201F29', relief='groove')
        self.control_fr.grid_rowconfigure(0, weight=1)
        self.control_fr.grid(row=0, sticky="nsew")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        # TODO - exception when doubleclick and moving the screen together
        x1 = self.x
        y1 = self.y
        x2 = event.x
        y2 = event.y
        deltax = x2 - x1
        deltay = y2 - y1
        a = self.winfo_x() + deltax
        b = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (a, b))

    def on_exit(self):
        self.destroy()

    def run(self):
        self.wm_deiconify()
        self.mainloop()

    def set_frames(self):
        self.frames = {}
        self.labels = {}
        self.update()
        for page_name, page_frame in self.pages.items():
            frame = page_frame(self.canvas, self, relief='flat', bg='#201F29', height=(self.canvas.winfo_height() - 33),
                               width=self.canvas.winfo_width())
            frame.grid(row=1, sticky="nsew")
            frame.Init()
            self.frames[page_name] = frame
            frame.bind("<ButtonPress-1>", self.start_move)
            frame.bind("<ButtonRelease-1>", self.stop_move)
            frame.bind("<B1-Motion>", self.on_motion)
            frame.bind("<Double-Button-1>", lambda x=None: self.maximize())
            label = tk.Label(self.control_fr, text=page_name, font=("Helvetica", "16"), bg='grey40')
            self.labels[page_name] = label
            label.grid(row=0, column=6, sticky="nsew")

        self.show_frame(MAIN_WINDOW)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        label = self.labels[page_name]
        label.tkraise()
        frame.tkraise()

    def minimize(self):
        self.overrideredirect(False)
        self.wm_state('iconic')
        self.overrideredirect(True)

    def maximize(self):
        self.overrideredirect(False)
        if self.control_fr.buttons["expand_button"].cget('text') == '1':
            self.wm_attributes('-fullscreen', True)
            self.control_fr.buttons["expand_button"].config(text='2')
        else:
            self.wm_attributes('-fullscreen', False)
            self.control_fr.buttons["expand_button"].config(text='1')

        self.overrideredirect(True)


class CreditWindow(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)
        self.controller = controller

    def Init(self):
        pass





