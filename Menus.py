import tkinter as tk


class ToolBar(tk.Frame):
    def __init__(self, parent, controller, pages, **kw):
        tk.Frame.__init__(self, parent, **kw)
        self.parent = parent
        self.controller = controller
        self.buttons = {}
        self.pages = pages
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.controls_buttons()
        self.file_label()
        self.settings_label()
        self.page_label()

    def file_label(self):
        file_menu = tk.Menubutton(self, text="File", width=10, background="grey28", font=("Times", "12", "bold italic"))
        file_menu.menu = tk.Menu(file_menu, tearoff=0)
        file_menu["menu"] = file_menu.menu
        ToolBar.react_button('white', "grey28", file_menu.menu, file_menu)
        file_menu.menu.add_cascade(label="Courses")
        file_menu.menu.add_cascade(label="Courses")
        file_menu.menu.add_separator()
        file_menu.menu.add_command(label="Exit", command=self.controller.on_exit)
        file_menu.grid(row=0, column=3, sticky="nsew")

    def settings_label(self):
        file_menu = tk.Menubutton(self, text="Settings", width=10, background="grey28", font=("Times", "12", "bold italic"))
        file_menu.menu = tk.Menu(file_menu, tearoff=0)
        file_menu["menu"] = file_menu.menu
        ToolBar.react_button('white', "grey28", file_menu.menu, file_menu)
        file_menu.menu.add_cascade(label="Advanced")
        file_menu.menu.add_cascade(label="Privacy")
        file_menu.menu.add_cascade(label="Copyright")
        file_menu.grid(row=0, column=4, sticky="nsew")

    def page_label(self):
        self.file_menu = tk.Menubutton(self, text="Pages", width=10, background="grey28", font=("Times", "12", "bold italic"))
        self.file_menu.menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu["menu"] = self.file_menu.menu
        for page in self.pages.keys():
            self.file_menu.menu.add_command(label=page, command=lambda x=page: self.controller.show_frame(x))
        self.file_menu.grid(row=0, column=5, sticky="nsew")

    def controls_buttons(self):
        exit_button = tk.Button(self, text='r', font=('webdings', 8), width=2, relief='flat',
                                    background="grey28", activebackground="red", command=self.controller.on_exit)
        self.buttons['exit_button'] = exit_button
        exit_button.grid(row=0, column=0)
        ToolBar.react_button('red', "grey28", exit_button, exit_button)

        min_button = tk.Button(self, text='0', font=('webdings', 8, 'bold'), width=2,
                                    background="grey28", relief='flat',
                                    command=self.controller.minimize)
        self.buttons['min_button'] = min_button
        min_button.grid(row=0, column=1)
        ToolBar.react_button('white', "grey28", min_button, min_button)
        expand_button = tk.Button(self, text='1', font=('webdings', 8, 'bold'), width=2,
                                      background="grey28", relief='flat',
                                      command=self.controller.maximize)
        self.buttons['expand_button'] = expand_button
        expand_button.grid(row=0, column=2)
        ToolBar.react_button('white', "grey28", expand_button, expand_button)

    @staticmethod
    def react_button(on_color, off_color, widget, connect_to_b):
        def on_enter(b):
            b['background'] = on_color

        def on_leave(b):
            b['background'] = off_color

        widget.bind("<Enter>", lambda x=None: on_enter(connect_to_b))
        widget.bind("<Leave>", lambda x=None: on_leave(connect_to_b))


class PopupBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.menu = tk.Menu(self.parent, tearoff=0)
        self.popup_menu()
        self.x_root = None
        self.y_root = None

    def popup_menu(self):
        self.menu.add_command(label="Color 1", command=self.bell)
        self.menu.add_command(label="Color 2", command=self.bell)
        self.menu.add_command(label="Color 3", command=self.bell)
        # self.parent.bind("<Button-3>", self.showMenu)

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

