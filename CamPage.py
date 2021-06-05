import tkinter as tk
import cv2
import PIL
from PIL import Image, ImageTk
import time
import pyautogui
from mediator import process_click

PATH_TO_IMAGE = "img_colormap.gif"


class MainWindow(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)
        self.controller = controller
        self.controller.update_idletasks()

    def Init(self):
        self.update()
        self.cam = VideoInput(self, self.controller)
        self.cam.pack(fill="both", expand=True)
        self.cam.Init()


class VideoInput(tk.Frame):
    def __init__(self, parent, controller, video_source=0, **kw):
        tk.Frame.__init__(self, parent, width=parent.winfo_width(), height=parent.winfo_height(), **kw)
        self.controller = controller
        self.video_source = video_source  # default web-cam = 0
        self.right_click_position = None
        self.color = None
        # open video source (by default this will try to open the computer web-cam)
        # Create a canvas that can fit the above video source size

    def Init(self):
        self.update()
        self.canvas = tk.Canvas(self, width=self.winfo_width(), height=self.winfo_height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.close_popup_colors)
        self.canvas.bind("<Button-3>", self.popup_colors)
        self.cap = MyVideoCapture(self.winfo_width(), self.winfo_height(), self.video_source)
        self.set_image_label()
        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(self, text="Snapshot", font=("Helvetica", "16"), width=30, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update_video()

    def close_popup_colors(self, e):
        self.colors_label.place_forget()

    def popup_colors(self, e):
        self.colors_label.place_forget()
        self.right_click_position = (e.y - self.winfo_y(), e.x - self.winfo_x())
        self.colors_label.place(x=e.x, y=e.y)

    def set_image_label(self):
        # Create a photoimage object of the image in the path
        img = ImageTk.PhotoImage(Image.open(PATH_TO_IMAGE))
        self.colors_label = tk.Label(self, image=img, width=150, height=150)
        self.colors_label.image = img
        self.colors_label.bind("<Button-1>", self.on_click_get_position)

    def on_click_get_position(self, e):
        posXY = pyautogui.position()
        # TODO - process this data
        self.color = pyautogui.pixel(posXY[0], posXY[1])

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.cap.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update_video(self):
        # Get a frame from the video source
        ret, frame = self.cap.get_frame()

        if ret:
            frame = process_click(frame, self.right_click_position, self.color)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(self.delay, self.update_video)

    def on_exit(self):
        self.destroy()


class MyVideoCapture:
    def __init__(self, width, height, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = width
        self.height = height

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                resize = cv2.resize(frame, (self.width, self.height))
                return ret, cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
            else:
                return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()
