"""
looks - module for a simple TUI framework 
with buttons, close button, a modifiable text area. 
"""
# last updated: 
# date -r looks.pyc
# Sun May  4 17:50:13 UTC 2025

# Needs:
#   print function -- 
#       # option to autoscroll

import curses

class app(object):
    def __init__(self, title, service, buttons = [], content=''):
        # type: (str, function, list[tuple], str) -> None
        self.title = title
        self.buttons = [('X', )]
        self.service = service
        self.buttons += buttons
        self.content = content
        self.pad = None

        self.view_row = 0
        self.view_col = 0
    
    def update_content(self, content, d_view_row, d_view_col):
        # type: (str, int, int) -> None

        """
        Update pad content if content changes or just move the window 
        """
        if (content != self.content) or self.pad==None:
            self.content = content
            buffer_rows = len(self.content.splitlines())+10
            buffer_cols = max([0] + [len(s) for s in self.content.splitlines()])+10 # max(<iter>) fails when <iter> becomes empty.
            if self.pad:
                self.pad.clear()
            self.pad = curses.newpad(buffer_rows, buffer_cols)
            self.pad.clear()
            for row, line in enumerate(self.content.splitlines()):
                self.pad.addstr(row, 0, line)
            
        self.view_col = (self.view_col + d_view_col) if (self.view_col + d_view_col) >= 0 else 0
        self.view_row = (self.view_row + d_view_row) if (self.view_row + d_view_row) >= 0 else 0

        term_rows, term_cols = self.stdscr.getmaxyx()
        self.pad.refresh(self.view_row, self.view_col, 2, 2, term_rows-3, term_cols-3)

    def printLine(self, text):  
        pass

    def activate(self):
        curses.wrapper(self.main)

    def rectangle(self, uly, ulx, lry, lrx):
        """Draw a rectangle with corners at the provided upper-left
        and lower-right coordinates.
        """
        win = self.stdscr
        win.vline(uly+1, ulx, '|', lry - uly - 1)
        win.hline(uly, ulx+1, '-', lrx - ulx - 1)
        win.hline(lry, ulx+1, '-', lrx - ulx - 1)
        win.vline(uly+1, lrx, '|', lry - uly - 1)
        win.addch(uly, ulx, '+')
        win.addch(uly, lrx, '+')
        win.addch(lry, lrx, '+')
        win.addch(lry, ulx, '+')

    def draw(self):
        # get size
        term_rows, term_cols = self.stdscr.getmaxyx()
        
        # background
        self.stdscr.bkgd(' ', self.A_BKGD)

        # panel border
        self.rectangle(1, 0, term_rows-2, term_cols-1)

        # title
        self.stdscr.addstr(0, 1, self.title)

        # Buttons
        # close button -- draws over title if needed
        self.stdscr.addstr(0, term_cols-5, '[ X ]', self.A_CLOSE)
        # draw other buttons if any
        for idx, b_info in enumerate(self.buttons[1:]):
            b_text = b_info[0]
            self.stdscr.addstr(0, term_cols-5*(idx+2), '[ '+b_text+' ]', self.A_BUTN)

        # draw textboxes if any
        self.stdscr.refresh()

        # draw content
        self.update_content(self.content, 0, 0)
        
        # finishing

    def main(self, stdscr):
        # type: (curses.window) -> None
        self.stdscr = stdscr

        # window frame colour
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.A_BKGD = curses.color_pair(1)
        # close window colour
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        self.A_CLOSE = curses.color_pair(2)

        # window invert colour
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
        self.A_BUTN = curses.color_pair(3)

        # init mouse
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

        # no delay --
        self.stdscr.nodelay(True)

        self.stdscr.clear() # dangerous! overlays everyting else
        self.stdscr.refresh() # dont refresh main window again

        ###############################################################################
        # UI
        
        # disable cursor -- temporary
        # curses.curs_set(0)

        # create pad for display content

        # draw everything relative to term_size on draw()
        # in the main loop
        # instead of detecting the difference from old and new term size
        # just always draw to term size when not equal

        self.stdscr.clear()
        self.draw()

        # make a text box

        # self.stdscr.refresh() # no need to refresh after draw
        
        # mainloop for detecting term size change
        while True:
            try:
                key = self.stdscr.getch()
                
                if key == curses.KEY_MOUSE: # mouse event
                    _, col, row, _, _ = curses.getmouse()
                    # add condition for left click and left hold only
                    _, term_cols = self.stdscr.getmaxyx()
                    
                    if (row == 0):
                        button_id = (term_cols - col - 1)//5
                        if button_id == 0: # close is the first button
                            break
                        else:
                            if button_id < len(self.buttons):
                                foo = self.buttons[button_id][1]
                                foo()
                        pass
                    # self.stdscr.addstr(5, 5, str(button_id))

                if key == curses.KEY_RESIZE:
                    self.stdscr.clear()
                    self.draw()
                
                # send other keys direct to app.
                else:
                    # send keys to app function to update content
                    self.service(key)

                # sleep(REFRESH_RATE)
            except KeyboardInterrupt:
                break
        
        # mainloop for logging keystrokes


