import tkinter as tk
from tkinter import messagebox
import random
import math

class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animation Creator")
        
        # Create a frame for the left panel (controls)
        self.left_frame = tk.Frame(root, width=200, bg="#f0f0f0", padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame for the main panel (animation display)
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create the main canvas for animations
        self.main_canvas = tk.Canvas(self.main_frame, bg="white", width=800, height=600)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize shape options
        self.shape_options = ["Rectangle", "Oval", "Line"]
        self.animation_options = ["Sine Wave", "Curve", "Zigzag"]
        self.speed_options = ["1x", "1.5x", "2x"]

        # Create StringVar for dropdown selections
        self.selected_shape = tk.StringVar(value=self.shape_options[0])
        self.selected_animation = tk.StringVar(value=self.animation_options[0])
        self.selected_speed = tk.StringVar(value=self.speed_options[0])

        # Add buttons to the left panel
        self.shape_frame = tk.LabelFrame(self.left_frame, text="Select Shape", bg="#e0e0e0", padx=10, pady=10)
        self.shape_frame.pack(pady=10, fill=tk.X)

        self.rectangle_button = tk.Button(self.shape_frame, text="Rectangle", command=lambda: self.display_shape("Rectangle"))
        self.rectangle_button.pack(pady=5)

        self.oval_button = tk.Button(self.shape_frame, text="Oval", command=lambda: self.display_shape("Oval"))
        self.oval_button.pack(pady=5)

        self.line_button = tk.Button(self.shape_frame, text="Line", command=lambda: self.display_shape("Line"))
        self.line_button.pack(pady=5)
        
        self.change_color_button = tk.Button(self.left_frame, text="Change Color", command=self.change_color)
        self.change_color_button.pack(pady=10)
       
        self.animate_color_button = tk.Button(self.left_frame, text="Animate Color", command=self.animate_color)
        self.animate_color_button.pack(pady=10)

        # Animation selection dropdown
        self.animation_menu = tk.OptionMenu(self.left_frame, self.selected_animation, *self.animation_options)
        self.animation_menu.pack(pady=10)

        # Speed control section
        self.speed_frame = tk.LabelFrame(self.left_frame, text="Animation Speed", bg="#e0e0e0", padx=10, pady=10)
        self.speed_frame.pack(pady=10, fill=tk.X)

        self.speed_var = tk.StringVar(value=self.speed_options[0])
        self.speed_1x = tk.Radiobutton(self.speed_frame, text="1x", variable=self.speed_var, value="1x", bg="#e0e0e0")
        self.speed_1_5x = tk.Radiobutton(self.speed_frame, text="1.5x", variable=self.speed_var, value="1.5x", bg="#e0e0e0")
        self.speed_2x = tk.Radiobutton(self.speed_frame, text="2x", variable=self.speed_var, value="2x", bg="#e0e0e0")

        self.speed_1x.pack(anchor=tk.W)
        self.speed_1_5x.pack(anchor=tk.W)
        self.speed_2x.pack(anchor=tk.W)

        # Toggle button for smooth transitions
        self.smooth_transition_var = tk.BooleanVar(value=False)
        self.smooth_transition_toggle = tk.Checkbutton(self.left_frame, text="Smooth Transitions", variable=self.smooth_transition_var, bg="#f0f0f0")
        self.smooth_transition_toggle.pack(pady=10)

        self.stop_animation_button = tk.Button(self.left_frame, text="Stop Animation", command=self.stop_animation)
        self.stop_animation_button.pack(pady=10)

        self.start_again_button = tk.Button(self.left_frame, text="Start Again", command=self.start_again)
        self.start_again_button.pack(pady=10)

        self.color_change_interval = 100  # Interval in milliseconds for color animation
        self.animating_color = False
        self.animating = False
        self.animation_speed = 1.0
        self.shape_id = None
        self.current_shape = None
        self.color = "blue"

    def display_shape(self, shape):
        self.main_canvas.delete("all")  # Clear previous shape
        if shape == "Rectangle":
            self.shape_id = self.main_canvas.create_rectangle(50, 50, 150, 150, fill=self.color)
        elif shape == "Oval":
            self.shape_id = self.main_canvas.create_oval(50, 50, 150, 150, fill=self.color)
        elif shape == "Line":
            self.shape_id = self.main_canvas.create_line(50, 50, 150, 150, fill=self.color, width=3)
        self.current_shape = shape
        self.animate_shape()  # Automatically start animation

    def change_color(self):
        self.color = self.random_color()
        if self.shape_id:
            self.main_canvas.itemconfig(self.shape_id, fill=self.color)

    def animate_shape(self):
        if self.shape_id and self.current_shape:
            self.animation_speed = self.get_animation_speed()
            animation_type = self.selected_animation.get()
            self.animating = True
            if animation_type == "Sine Wave":
                self.animate_sine_wave()
            elif animation_type == "Curve":
                self.animate_curve()
            elif animation_type == "Zigzag":
                self.animate_zigzag()
            else:
                messagebox.showerror("Invalid Animation Type", "Please choose a valid animation type.")
        else:
            messagebox.showerror("Animation Error", "Please select a shape first.")

    def get_animation_speed(self):
        speed = self.speed_var.get()
        if speed == "1x":
            return 1.0
        elif speed == "1.5x":
            return 1.5
        elif speed == "2x":
            return 2.0
        return 1.0

    def animate_sine_wave(self):
        if self.shape_id and self.animating:
            width = self.main_canvas.winfo_width()
            amplitude = 50
            frequency = 0.1
            speed = self.animation_speed
            step = int(10 / speed)
            delay = int(40 / speed)

            for t in range(0, width, step):
                if not self.animating:
                    break
                x = t
                y = amplitude * math.sin(frequency * t) + 200  # 200 is the vertical center
                if x + 100 > width:
                    x = width - 100
                if y + 100 > self.main_canvas.winfo_height():
                    y = self.main_canvas.winfo_height() - 100
                if self.current_shape == "Rectangle":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                elif self.current_shape == "Oval":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                elif self.current_shape == "Line":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                self.root.update()
                self.root.after(delay)

    def animate_curve(self):
        if self.shape_id and self.animating:
            width = self.main_canvas.winfo_width()
            height = self.main_canvas.winfo_height()
            speed = self.animation_speed
            step = int(10 / speed)
            delay = int(40 / speed)

            for t in range(0, width, step):
                if not self.animating:
                    break
                x = t
                y = 0.01 * (x - width / 2) ** 2 + height / 2  # Parabolic curve
                if x + 100 > width:
                    x = width - 100
                if y + 100 > height:
                    y = height - 100
                if self.current_shape == "Rectangle":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                elif self.current_shape == "Oval":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                elif self.current_shape == "Line":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                self.root.update()
                self.root.after(delay)

    def animate_zigzag(self):
        if self.shape_id and self.animating:
            width = self.main_canvas.winfo_width()
            height = self.main_canvas.winfo_height()
            speed = self.animation_speed
            step = int(10 / speed)
            delay = int(100 / speed)

            for t in range(0, width, step):
                if not self.animating:
                    break
                x = t
                y = (t // 20) % 2 * height / 2  # Zigzag pattern
                if x + 100 > width:
                    x = width - 100
                if y + 100 > height:
                    y = height - 100
                if self.current_shape == "Rectangle":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                elif self.current_shape == "Oval":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                elif self.current_shape == "Line":
                    self.main_canvas.coords(self.shape_id, x, y, x + 100, y + 100)
                self.root.update()
                self.root.after(delay)

    def animate_color(self):
        if self.shape_id:
            self.animating_color = True
            self._animate_color_step()

    def _animate_color_step(self):
        if self.animating_color:
            new_color = self.random_color()
            self.main_canvas.itemconfig(self.shape_id, fill=new_color)
            self.root.after(self.color_change_interval, self._animate_color_step)

    def start_again(self):
        self.main_canvas.delete("all")
        self.shape_id = None
        self.current_shape = None
        self.animating = False
        self.animating_color = False

    def stop_animation(self):
        self.animating = False
        self.animating_color = False

    def random_color(self):
        return f'#{random.randint(0, 0xFFFFFF):06x}'

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()
