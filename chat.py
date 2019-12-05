import os
from utils import c_utils
import requests
import time
import threading
import json
import sys
#from encrypt import c_encryption
from profanityfilter import ProfanityFilter # this is very basic and not good
import getpass

utils = c_utils()
prev_size = 0
messages = []

class c_chatroom:
  # "global" variables
  site = "https://pychatroombackend--sanjaykdragon.repl.co" # backend - located @ https://repl.it/@sanjaykdragon/mmh-thing-backend

  pf = ProfanityFilter() # obvious - not amazing though, only blocks words if they are alone

  # function name & args - __init__(self)
  # parent / caller - class creation
  # children / called - start_chatroom
  # dependencies - c_utils,  getpass
  # description - sets up user account

  def __init__(self):
    self.username = input("enter your username: ")
    self.username = self.username.strip() #remove whitespace
    self.password = getpass.getpass("password: ")
    query = {"user": self.username, "password" : self.password }
    r = requests.post(self.site + "/login.php", query)
    if r.json()["status"] == "success":
          self.user_index = r.json()["index"]
          utils.print_colored(r.json()["detail"], "green")
          time.sleep(2)
          self.start_chatroom()
    else:
          reason = r.json()["detail"]
          utils.print_colored(f"request failed, {reason}", "red")


  # function name & args - start_chatroom(self, user)
  # user - takes the user's username -> str
  # parent / caller - __init__
  # children / called - get_user_input, check_for_changes
  # dependencies - c_utils, requests, threading 
  # description - sets up the main chatroom, starts required threads, etct

  def start_chatroom(self):
    self.blocked_users = []
    user = self.username
    utils.clear()
    utils.print_colored(f"welcome to the chatroom, {user}", "green")
    query = {"user": user, "message": "has joined the chatroom"}

    r = requests.post(self.site + "/index.php", data=query)

    changes_thread = threading.Thread(target=self.check_for_changes)
    changes_thread.start() #running this separately because it is in a forever loop
    self.get_user_input()
  
  # function name & args - get_user_input(self)
  # parent / caller - start_chatroom
  # children / called - none
  # dependencies - requests, c_encryption (OPTIONAL), c_utils, sys, profanity_filter
  # description - allows the sending of messages, handling of commands & sends the data[messages] to the php server
  
  def get_user_input(self):
    while True:
      to_send = input("enter a message to send: ")
      if len(to_send) == 0:
        continue
    
      is_command = len(to_send) > 1 and to_send[0:1] == "/"
      if is_command:
        #handle commands
        if len(to_send) > 6 and to_send[0:6] == "/block":
            #add a user to block list
            to_block = to_send.replace("/block", "").lower().strip()
            self.blocked_users.append(to_block)
            print(f"added {to_block} to block list.")
            self.redraw_messages()
        if len(to_send) > 8 and to_send[0:8] == "/unblock":
            #add a user to block list
            to_block = to_send.replace("/unblock", "").lower().strip()
            self.blocked_users.remove(to_block)
            print(f"removed {to_block} from block list.")
            self.redraw_messages()
        elif len(to_send) == 3 and to_send == "/lb":
            #list blocked users
            if len(self.blocked_users) == 0:
                print("you have no blocked users")
            else:
                for user in self.blocked_users:
                    print(f"{user} is blocked")
        else:
            query = {"user" : self.username, "password" : self.password, "index" : self.user_index, "cmd" : to_send}
            r = requests.post(self.site + "/admin.php", data=query)
            print(r.text)
            time.sleep(2)
      else:
        #handle chat
        to_send = self.pf.censor(to_send)
        query = {"user" : self.username, "message" : to_send, "password" : self.password, "index": self.user_index}
        r = requests.post(self.site + "/index.php", data=query)
        if r.text == "banned user":
            utils.clear()
            print(self.username + " is a banned username.")
            sys.exit(0)
            return



  # function name & args - check_for_changes(self)
  # parent / caller - start_chatroom
  # children / called - on_size_change
  # dependencies - requests, time, sys, c_utils
  # description - checks for any new messages, and if so, calls the new message handler

  def check_for_changes(self): #run this multithreaded
    self.prev_size = 0
    while True:
      query = {"user" : self.username}
      r = requests.post(self.site + "/get.php", data=query)

      if r.text == "banned user":
          utils.clear()
          print(self.username + " is a banned username.")
          sys.exit(0)
          return

      if len(r.text) != self.prev_size:
        self.on_size_change(r.text)
      time.sleep(3) #sleep for 3 seconds


  # function name & args - on_size_change(self, messages_as_txt)
  # messages_as_txt - takes the "message list" -> str
  # parent / caller - check_for_changes
  # children / called - redraw_messages
  # dependencies - c_utils
  # description - takes the message str, splits it into a list, then calls redraw_messages
  
  def on_size_change(self, messages_as_txt):
    utils.clear()
    self.prev_size = len(messages_as_txt)
    self.messages = messages_as_txt.split("\n") #split by newline

    if len(self.messages) == 0 or self.messages == None: 
      return

    self.redraw_messages()

    print("enter a message to send: ")

  # function name & args - redraw_messages(self)
  # parent / caller - on_size_change, get_user_input
  # children / called - none
  # dependencies - c_utils, c_encryption (OPTIONAL)
  # description - redraws messages from variable "self.messages"

  def redraw_messages(self):
      utils.clear()
      for i in self.messages:

        #make sure its a valid message, not just whitespace
        if len(i.strip()) == 0 or i == None: 
            continue
    
        msg = json.loads(i)
        msg_txt = msg["message"]
        msg_user = msg["user"]
        msg_time = msg["time"]
        if msg_user.lower() in self.blocked_users:
            utils.print_colored(f"--- message from blocked user ({msg_user}) ---", "grey")
        else:
            if "@" + self.username in msg_txt: #user is mentioned
                utils.print_colored(msg_time + " <" + msg_user + "> " + msg_txt, "yellow")
            else:
                if msg_user == "system":
                    utils.print_colored("system: " + msg_txt, "green")
                else:
                    utils.print_colored(msg_time + " <" + msg_user + "> " + msg_txt, msg["color"])
