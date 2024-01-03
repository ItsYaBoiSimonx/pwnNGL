import requests
import concurrent.futures
import os
import datetime
import sys
import time
valid = []
amtValids = 0
checked = 0
proxy_file = r"C:\Users\simone\Desktop\guilded serx\proxy fucking\proxies.txt" 
threads = 200

def count_lines_in_file(file_path):
    try:
        with open(file_path, "r") as file:
            line_count = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        return 0 
    
proxiestocheck = count_lines_in_file(proxy_file)

def set_console_window_size(width, height):
    os.system(f"mode con: cols={width} lines={height}")

def colorize(text, color_code):
    return f"\033[{color_code}{text}\033[0m"

def warning(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    colored_timestamp = colorize(timestamp, "33m")  # 33m is the ANSI color code for yellow
    textsss = colorize("Warning!", "33m")  # 32m is the ANSI color code for green
    print(f"{colored_timestamp} {textsss} {message.capitalize()}.")

def success(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    colored_timestamp = colorize(timestamp, "32m")
    textsss = colorize("Success!", "32m")  # 32m is the ANSI color code for green
    print(f"{colored_timestamp} {textsss} {message.capitalize()}.")

def error(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    colored_timestamp = colorize(timestamp, "31m")  # 31m is the ANSI color code for red
    textsss = colorize("Error!", "31m")  # 32m is the ANSI color code for green
    print(f"{colored_timestamp} {textsss} {message.capitalize()}.")

os.system('cls' if os.name == 'nt' else 'clear')
set_console_window_size(90,25)

try:
    with open(proxy_file, "r"):
        pass  # File exists, do nothing
        success("Found proxies file!")
except FileNotFoundError:
    with open(proxy_file, "w"):
        warning("Proxy file not found! Creating one") # File doesn't exist, create it
        sys.exit()
def is_proxy_working(proxy):
    try:
        test_url = "https://www.example.com"
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        response = session.get(test_url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        return False

# File path containing the list of proxies
proxy_file = r"C:\Users\simone\Desktop\guilded serx\proxy fucking\proxies.txt"

# Read the list of proxies from the file
with open(proxy_file, 'r') as file:
    proxies = file.read().splitlines()


# Function to check proxies in parallel
def check_proxies(proxy_list):
    working_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        # Submit proxy checking tasks to the executor
        future_to_proxy = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxy_list}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            if future.result():
                working_proxies.append(proxy)
                success(f"{proxy} is working")
            else:
                error(f"{proxy} is not working")
    return working_proxies

# Check proxies in parallel and get the list of working proxies
working_proxies = check_proxies(proxies.copy())  # Make a copy of the list to avoid modifying the original
with open(proxy_file, 'w') as file:
    pass 

with open(proxy_file, 'w') as file:
    for proxy in working_proxies:
        file.write(f"{proxy}\n")
        success("Written proxies to file")
    