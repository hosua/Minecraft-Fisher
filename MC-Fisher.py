# For larger scale projects, I really should learn to use classes... lol
from PIL import ImageGrab, ImageTk, Image
import keyboard
import pyautogui
import tkinter as tk
import os
import time, datetime
import text_redirect as TR
import sys


# GUI stuff
TITLE = "Minecraft-Fisher - Made by Hoswoo"
DARK_BLUE = '#0A3D62'
LIGHT_BLUE = "#7ddeff"
DARK_GREY = "#2C3335"
CONSOLE_BG = '#A1AAB5'
FONT_BIG = ('calibre', 12, 'bold')
FONT = ('calibre', 10, 'bold')
FONT_CONSOLE = ('Times', 10, 'normal')
SIZE = ("400x500")
root = tk.Tk()
root.configure(bg=DARK_BLUE)
root.title(TITLE)
root.geometry(SIZE)
root_dir = os.getcwd()

# GUI Console
console_frame = tk.Frame(root, bg=DARK_BLUE, height=250, width=200)
console_sub_frame = tk.Frame(console_frame, bg=DARK_BLUE)
console_text = tk.Text(root, height=12,
                       width=60, bg=CONSOLE_BG, fg=DARK_GREY, font=FONT_CONSOLE)
console_text.config(state="disabled")
console_text.see("end")

sys.stdout = TR.TextRedirector(console_text)    # Send console output to textbox instead of actual console.
# sys.stderr = TR.TextRedirector(console_text)  # Errors will output in console

print("PLEASE READ BEFORE USING:\n")
print("The bot works by detecting a specific shade of red on the bobber. With that being said...")
print("Before you use the bot, you should turn your brightness all the way up.")
print("You will also have to map your right-mouse-click to 'r'. (This was a workaround due to the mouse input causing issues)")
print("For best results, ensure you are in a very well lit area and that the fish bobber appears within your capture region!")
print("NOTE: If your health hearts are in the capture region, it will falsely detect the bobber.")
# Global constants
BOBBER_COLOR = (208, 41, 41, 255)
BOBBER_COLOR_NIGHT = (206, 40, 39, 255)


region_var = tk.StringVar()
region_var.set(300) # Default to 300, should work for most people.
BOX_SIZE = int(region_var.get()) # get box size from spinbox
FILENAME = "pic.png"


x = 0
y = 0

def grab_image():
    global x, y
    #image = ImageGrab.grab(bbox=(x-(BOX_SIZE/2), y-(BOX_SIZE/2), x+(BOX_SIZE/2), y+(BOX_SIZE/2)))  
    image = ImageGrab.grab(bbox=(x-(BOX_SIZE/2), y-(BOX_SIZE/2), x+(BOX_SIZE/2), y+(BOX_SIZE/2)))  
    data = list(image.getdata())
    image.save(FILENAME)

    return data





def validate(user_input):   # I don't really remember how to get validation to properly work.. so I'm just not gonna allow
    # users to type anything lol
    # Sourced from https://www.geeksforgeeks.org/python-tkinter-spinbox-range-validation/
    if user_input:
        #print("Typing not allowed")
        return False

region_label = tk.Label(root, text="Region size",
                      bg=DARK_BLUE, fg=LIGHT_BLUE, font=FONT)
region_spinbox = tk.Spinbox(root, from_=25, to=1000,
                            increment=25, textvariable=region_var, width=6)

range_validation = root.register(validate)
region_spinbox.config(validate="key", validatecommand=(range_validation, '% P'))    # Absolutely no idea how this works lol

pic_frame = tk.Frame(root, bg="#FFFFFF", height=BOX_SIZE, width=BOX_SIZE)
#img = ImageTk.PhotoImage(Image.open(FILENAME))
pic_frame_label = tk.Label(pic_frame)

pic_frame_label.pack()
pic_frame.pack()

running = False      
times_not_detected = 0

def loop_action():
    timestamp = "(" + '{:%H:%M:%S}'.format(datetime.datetime.now()) + ")" 
    def check_for_bobber():
        img = Image.open(FILENAME)
        img = img.convert("RGBA")
        data = list(img.getdata())
        # print(data)
        if BOBBER_COLOR_NIGHT in data or BOBBER_COLOR in data:
            print(timestamp + " Bobber detected")
            return True
        else:
            print(timestamp + " Bobber not detected")
            keyboard.press_and_release("r")
            return False
    console_text.see("end")
    grab_image()
    img = ImageTk.PhotoImage(Image.open(FILENAME))  # set image to grabbed image
    pic_frame_label.configure(image=img)    # configure label to show new image
    pic_frame_label.image = img
    return check_for_bobber()   # Return True if bobber is detected and False if not.

def screenshot_loop(event=None):    # Do this while running
    global running, times_not_detected
    if running:
        bobber_detected = loop_action()
        if not bobber_detected:
            if times_not_detected != 2:  # Delay for recast
                time.sleep(1.0)
            else:
                pass
            times_not_detected += 1
        else:
            times_not_detected = 0
            

            
        root.after(100, screenshot_loop)

def start_task(event=None):
    global BOX_SIZE
    global running
    global x,y 
    BOX_SIZE = int(region_var.get()) # get box size from spinbox
    x = pyautogui.position()[0]
    y = pyautogui.position()[1]
    if running is False:
        print("(" + '{:%H:%M:%S}'.format(datetime.datetime.now()) + ") Starting...\n")
        running = True
        screenshot_loop()
    else:
        print("(" + '{:%H:%M:%S}'.format(datetime.datetime.now()) + ") I'm already running!...\n")

def stop_task(event=None):
    global running, times_not_detected
    if running is True:
        print("(" + '{:%H:%M:%S}'.format(datetime.datetime.now()) + ") Stopping...\n")
        running = False
        times_not_detected = 0

start_btn = tk.Button(root, text="Start (~)", bg=DARK_GREY,
                     fg=LIGHT_BLUE, command=start_task, width=10)
stop_btn = tk.Button(root, text="Stop (F1)", bg=DARK_GREY,
                     fg=LIGHT_BLUE, command=stop_task, width=10)
region_label.pack()                     
region_spinbox.pack()
start_btn.pack()
stop_btn.pack()
console_frame.pack()
console_sub_frame.pack()
console_text.pack()
keyboard.add_hotkey('`', start_task)
keyboard.add_hotkey('F1', stop_task)
root.mainloop()

