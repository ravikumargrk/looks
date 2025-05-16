from looks import app
import curses

# test 

import os 
def t_button_click():
    os.system('date >> t_button_click_time')
    pass

def appService(key):
    # type (int) -> None
    if key == curses.KEY_DOWN:
        myApp.update_content(myApp.content, 1, 0)

    if key == curses.KEY_UP:
        myApp.update_content(myApp.content, -1, 0)

    if key == curses.KEY_RIGHT:
        myApp.update_content(myApp.content, 0, 1)

    if key == curses.KEY_LEFT:
        myApp.update_content(myApp.content, 0, -1)

with open('loremipsum', 'r') as f:
    buffer_test = f.read()
    f.close()

myApp = app('fvi text editor', appService, buttons=[('T', t_button_click)], content=buffer_test) # type: app
myApp.activate()

# only in freebsd
import os 
os.system('clear')