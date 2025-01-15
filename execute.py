import os
import requests
import git
import json
import re
from typing import TypedDict, List, Optional
from datetime import datetime
from colorama import Fore, Style, init
from src import *
import threading
import time
import sys

DEBUG = False

def execute_main_task(user_input):
    main(user_input)

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        cool_output("Welcome I am Erl your personal code generation guru here\nto help get your projects off the ground in no time. 🚀🚀", Fore.MAGENTA)
        cool_output("For API docs see: http://127.0.0.1:5000/apidocs/#/ this is a localised api")
        user_input = input(Fore.YELLOW + "Enter your project requirements: " + Style.RESET_ALL)
        thread = threading.Thread(target=execute_main_task(user_input), daemon=True)
        thread.start()
    except Exception as e:
        if DEBUG is True:
            print(e)
