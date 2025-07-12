# looks - Terminal UI framework
# Copyright (C) 2025 Ravi Kumar
# This file is part of the 'looks' project and is licensed under the GNU GPL v3.
# See the LICENSE file for more details.

# last updated: 
# date -r looks.pyc
# Sun May  8 06:30:00 UTC 2025

import traceback
import threading
import curses
import time

# disable Ctrl+Z to send sigstop
import signal
signal.signal(signal.SIGTSTP, signal.SIG_IGN)

# disable Ctrl+S and Ctrl+Q which pauses the terminal 
import os
os.system("stty -ixon")

TOP_PAD = 2
BOT_PAD = 2
LFT_PAD = 1
RGT_PAD = 1

class app(object):
    def __init__(self, title, service, buttons = [], content=[]):
        # type: (str, function, list[tuple], list[str]) -> None
        self.title = title
        self.buttons = [('X', )]
        self.service = service
        self.buttons += buttons
        self.content = content
        self.pad = None
        self.pad_line = 0

        self.view_row = 0
        self.view_col = 0

        self.key_inputs = []

        self.exit_log = ''
    
    # def update_content(self, content, d_view_row, d_view_col):
    #     # type: (str, int, int) -> None

    #     """
    #     Update pad content if content changes or just move the window 
    #     """
    #     if (content != self.content) or self.pad==None:
    #         self.content = content
    #         buffer_rows = len(self.content.splitlines())+10
    #         buffer_cols = max([0] + [len(s) for s in self.content.splitlines()])+10 # max(<iter>) fails when <iter> becomes empty.
    #         if self.pad:
    #             self.pad.clear()
    #         self.pad = curses.newpad(buffer_rows, buffer_cols)
    #         self.pad.clear()
    #         for row, line in enumerate(self.content.splitlines()):
    #             self.pad.addstr(row, 0, line)
            
    #     self.view_col = (self.view_col + d_view_col) if (self.view_col + d_view_col) >= 0 else 0
    #     self.view_row = (self.view_row + d_view_row) if (self.view_row + d_view_row) >= 0 else 0

    #     term_rows, term_cols = self.stdscr.getmaxyx()
    #     self.pad.refresh(self.view_row, self.view_col, 2, 2, term_rows-3, term_cols-3)

    def update(self, d_view_row=0, d_view_col=0):
        # type: (int, int) -> None
        # write last n lines of self.content
        term_rows, term_cols = self.stdscr.getmaxyx()
        row_strt = TOP_PAD 
        row_stop = term_rows - BOT_PAD
        N_ROWS = term_rows - TOP_PAD - BOT_PAD

        col_strt = 1 + LFT_PAD
        col_stop = term_cols - RGT_PAD
        N = term_cols - LFT_PAD - RGT_PAD - 1

        # print first few lines 
        show_lines = self.content[self.view_row : N_ROWS+self.view_row]
        if not show_lines:
            show_lines = ['']
        max_width = max(len(w) for w in show_lines)
        max_width = max(max_width - (N - 1), 0)
        max_rows  = max(len(self.content) - N_ROWS + 1, 0)

        self.view_col = min(max(self.view_col + d_view_col, 0), max_width)
        self.view_row = min(max(self.view_row + d_view_row, 0), max_rows )

        for row_idx in range(row_strt, row_stop):
            self.stdscr.addnstr(row_idx, col_strt, ' '*N, N, self.A_NORMAL)
            idx = (row_idx-row_strt)
            if idx < len(show_lines):
                line = show_lines[idx][self.view_col:]
                self.stdscr.addnstr(row_idx, col_strt, line, N, self.A_NORMAL)
            row_idx += 1
        
        # upon load, write the first lines from top.
        # self.stdscr.redrawwin()

    def scrolldown(self):
        term_rows, term_cols = self.stdscr.getmaxyx()
        row_strt = TOP_PAD 
        row_stop = term_rows - BOT_PAD
        N_ROWS = term_rows - TOP_PAD - BOT_PAD

        self.update(N_ROWS, 0)

    def service_wrapper(self, *args, **kwargs):
        try:
            self.service(*args, **kwargs)
        except Exception as e:
            tb_lines = traceback.format_exc().splitlines()
            tb_lines = tb_lines[0:1] + tb_lines[3:]
            self.exit_log = '\n'.join(tb_lines)

    def activate(self):
        self.thread = threading.Thread(target=self.service_wrapper, args=(self,))
        self.thread.setDaemon(True)

        curses.wrapper(self.main)
        print(self.exit_log)


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
        # self.update_content(self.content, 0, 0)
        self.update()
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

        # window invert colour
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.A_NORMAL = curses.color_pair(4)

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

        # self.stdscr.refresh() # no need to refresh after draw

        # start background service
        self.thread.start()

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
                            # how to exit gracefully ?
                            self.key_inputs.append(curses.KEY_CLOSE)
                        else:
                            if button_id < len(self.buttons):
                                foo = self.buttons[button_id][1]
                                foo()
                        pass
                    # self.stdscr.addstr(5, 5, str(button_id))

                if key == curses.KEY_RESIZE:
                    self.stdscr.clear()
                    self.draw()
                
                if not self.thread.is_alive():
                    break
                # send other keys direct to app service.
                else:
                    # send keys to app function to update content
                    # run in seperate thread.
                    if key != -1:
                        self.key_inputs.append(key)
                
                # sleep(REFRESH_RATE)
            except KeyboardInterrupt:
                pass
                # self.exit_log += 'Keyboard Interrupt'
                # break
        
        # mainloop for logging keystrokes
        return 0


# add __name___ = '__main__' case
# display output from stdin 