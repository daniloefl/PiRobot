#!/usr/bin/env python

from robot import Robot
import time

import curses


def main(win):
  r = Robot()

  win.keypad(True)
  win.nodelay(True)
  key = -1
  oldkey = -1
  win.clear()
  win.addstr("Key: ")
  try:
    while True:
      try:
        key = win.getch()
        if key == -1:
          key = oldkey
      except KeyboardInterrupt:
        print("You pressed Ctrl+C. Stopping and exiting.")
        break
      #win.clear()
      win.addstr(0,0,'Press a key.')
      win.addstr(1,0,'Use the arrows to move.')
      win.addstr(2,0,'Use d to get the distance to the next object ahead.')
      win.addstr(3,0,'Use q to quit.')
      win.addstr(5,0,'Status:')
      if key == curses.KEY_UP:
        r.forwards()
        time.sleep(0.1)
        r.stop()
        key = -1
        oldkey = -1
        win.addstr(5,8,'Moved forward.')
      elif key == curses.KEY_DOWN:
        r.backwards()
        time.sleep(0.1)
        r.stop()
        key = -1
        oldkey = -1
        win.addstr(5,8,'Moved backwards.')
      elif key == curses.KEY_LEFT:
        r.left()
        time.sleep(0.1)
        r.stop()
        key = -1
        oldkey = -1
        win.addstr(5, 8, 'Turned left.')
      elif key == curses.KEY_RIGHT:
        r.right()
        time.sleep(0.1)
        r.stop()
        key = -1
        oldkey = -1
        win.addstr(5, 8, 'Turned right.')
      elif key == ord('d') or key == ord('D'):
        d = r.distance()
        oldkey = key
        win.addstr(5, 8, "Distance from next object ahead: %.3f cm " % (d*1e2))
      elif key == ord('q') or key == ord('Q'):
        win.addstr(8, 0, 'Quitting, as requested.')
        time.sleep(1)
        break
      else:
        pass
  except KeyboardInterrupt:
    print("You pressed Ctrl+C. Stopping and exiting.")

  r.cleanup()


curses.wrapper(main)

