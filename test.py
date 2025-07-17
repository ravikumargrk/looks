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
    play = True
    while True:
        if app_front.key_inputs:
            key = app_front.key_inputs.pop(0)
            if key == curses.KEY_CLOSE:
                break
            if key == curses.KEY_BACKSPACE:
                play = False if play else True
                pass
            
        if lines:
            if play:
                app_front.content += [lines.pop(0)]
                app_front.scrolldown()
                time.sleep(1)
        else:
            break
            # if len(app_front.content) > 4:
            #     raise RuntimeError('sample error')

# scroll down button handler
def S_button_click():
    myApp.content += [str(myApp.get_current_size())]
    pass

def pause():
    myApp.key_inputs.append(curses.KEY_BACKSPACE)
    # myApp.content += ['pause hit!']

myApp = app(
    'text reader', 
    appService, 
    buttons=[('S', S_button_click), ('P', pause)]
) 

myApp.activate()
