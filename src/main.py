import os
import requests
from datetime import datetime
from .utils import *
from .git import *
from .structure import *
from colorama import Fore
import sys
import time
import threading

now = datetime.now()
timestamp = now.timestamp()
base_path = f"./generated/GeneratedSystem_{timestamp}"

def main(user_input):
    try:
        cool_output("[🔨] Starting code creation...")
        data_url = f"http://127.0.0.1:5000/files"
        headers = {}
        payload = {"prompt": user_input}
        # try:
        cool_output("[🔍] Sending request for code creation...")
        thread = threading.Thread(target=display_loading_animation, daemon=True)
        thread.start()
        response = requests.post(data_url, json=payload, headers=headers)
        cool_output(response.text)
        json_data = process_output(response.text)
        set_animation_loading(False)
        cool_output("[🔨] Creating folder structure locally...")
        create_structure(base_path, json_data)
        push_to_github(base_path)

    except Exception as e:
        cool_output(f"[🚨] Failed to complete code generation", Fore.RED)
        set_animation_loading(False)
        raise Exception(e)