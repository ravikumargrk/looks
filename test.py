from looks import app
import curses

# test 

import os 
# def t_button_click():
#     with open('t_button_click', 'a') as f:
#         f.write('\nCurrent keys:\n')
#         f.writelines([str(k)+'\n' for k in myApp.key_inputs])
#         f.write('-'*50)
#     pass

def t_button_click():
    myApp.scrolldown()
    pass

with open('loremipsum', 'r') as f:
    buffer_test = f.read()
    f.close()

def appService(app_front):
    # type: (app) -> None
    while True:
        if app_front.key_inputs:
            key = app_front.key_inputs.pop(0)
            if key == curses.KEY_CLOSE:
                break
            if key == curses.KEY_DOWN:
                app_front.update(1, 0)
            if key == curses.KEY_UP:
                app_front.update(-1, 0)
            if key == curses.KEY_RIGHT:
                app_front.update(0, 1)
            if key == curses.KEY_LEFT:
                app_front.update(0, -1)

# lines = buffer_test.splitlines()
# def appService(app_front):
#     # type: (app) -> None
#     while True:
#         if app_front.key_inputs:
#             key = app_front.key_inputs.pop(0)
#             if key == curses.KEY_CLOSE:
#                 break
#             if lines:
#                 app_front.content += [lines.pop(0)]
#                 app_front.scrolldown()

myApp = app('fvi text editor', appService, buttons=[('T', t_button_click)], content=buffer_test.splitlines()) # type: app
myApp.activate()


# only in freebsd
# import os 
# os.system('clear')