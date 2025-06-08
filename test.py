import curses
from looks import app

# example text file
with open('random_text_file.txt', 'r') as f:
    buffer_test = f.read()
    f.close()

lines = buffer_test.splitlines()
import time
def appService(app_front):
    # type: (app) -> None
    while True:
        if app_front.key_inputs:
            key = app_front.key_inputs.pop(0)
            if key == curses.KEY_CLOSE:
                break
        if lines:
            app_front.content += [lines.pop(0)]
            app_front.scrolldown()
            time.sleep(0.5)

# scroll down button handler
def S_button_click():
    myApp.scrolldown()
    pass

myApp = app(
    'text reader', 
    appService, 
    buttons=[('S', S_button_click)], 
    content=buffer_test.splitlines()
) 

myApp.activate()
