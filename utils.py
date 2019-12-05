import os
import random as r
import time

from termcolor import colored


class c_utils:

  # function name & args - print_colored(self, msg, color)
  # msg - message to color -> str
  # color - color of the message -> str
  # parent / caller - none
  # children / called - none
  # dependencies - termcolor
  # description - prints a colored message

  def print_colored(self, msg, color):
    print(colored(msg, color))

  # function name & args - clear(self)
  # parent / caller - none
  # children / called - none
  # dependencies - os
  # description - clears the screen - although this is not cross platform compliant.

  def clear(self):
    os.system("clear") #not cross platform compliant