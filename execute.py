import os
import requests
import git
import json
import re
from typing import TypedDict, List, Optional
from datetime import datetime
from colorama import Fore, Style, init
from autocodegeneraterl import *

# Set your OpenAI API key and GitHub credentials
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    cool_output("Welcome I am Erl your personal code generation guru here\nto help get your projects off the ground in no time. 🚀🚀", Fore.MAGENTA)
    user_input = input(Fore.YELLOW + "Enter your project requirements: " + Style.RESET_ALL)
    main(user_input)