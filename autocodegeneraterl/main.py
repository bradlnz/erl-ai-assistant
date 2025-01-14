import os
import requests
from datetime import datetime
from .utils import *
from .git_helper import *
from .structure import *
from colorama import Fore

now = datetime.now()
timestamp = now.timestamp()
base_path = f"./generated/GeneratedSystem_{timestamp}"

def main(user_input):
    cool_output("Starting request to API...")
    data_url = f"http://127.0.0.1:5000/files"
    headers = {}
    payload = {"prompt": user_input}
    # try:
    response = requests.post(data_url, json=payload, headers=headers)
    json_data = process_output(response.json())
    create_structure(base_path, json_data)
    push_to_github(base_path)
    # except:
    #     cool_output("Failed to generate code please try again", Fore.RED)