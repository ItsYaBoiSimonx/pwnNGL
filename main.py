try:
    import datetime, os, httpx, random, threading, time, json
    from colorama import Fore
    from pystyle import Colorate, Colors, Center
except ImportError:
    os.system("pip3 install datetime")
    os.system("pip3 install os")
    os.system("pip3 install httpx")
    os.system("pip3 install threading")
    os.system("pip3 install time")
    os.system("pip3 install pystyle")
    os.system("pip3 install colorama")
    os.system("pip3 install json")


headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
}

with open('proxies.txt', "r") as file:
    proxies = [line.strip() for line in file]

def set_console_window_size(width, height):
    os.system(f"mode con: cols={width} lines={height}")
def colorize(text, color_code):
    return f"\033[{color_code}{text}\033[0m"

def warning(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    textsssss = colorize("Warning!", "33m")
    colored_timestamp = colorize(timestamp, "33m")  # 33m is the ANSI color code for yellow
    print(f"{colored_timestamp} {textsssss} {message.capitalize()}.")

def success(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    textsssss = colorize("Success!", "32m")
    colored_timestamp = colorize(timestamp, "32m")  # 32m is the ANSI color code for green
    print(f"{colored_timestamp} {textsssss} {message.capitalize()}.")

def error(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    colored_timestamp = colorize(timestamp, "31m")
    textsssss = colorize("Error!", "31m")  # 31m is the ANSI color code for red
    print(f"{colored_timestamp} {textsssss} {message.capitalize()}.")


os.system('cls' if os.name == 'nt' else 'clear')
set_console_window_size(120,25)

redmen =  '[' + Fore.RED + '-' + Fore.RESET + ']'
greenpl =  '[' + Fore.GREEN + '+' + Fore.RESET + ']'
yellowint = '[' + Fore.YELLOW + '?' + Fore.RESET + ']'

print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter('''

                                  $$\   $$\  $$$$$$\  $$\       
                                  $$$\  $$ |$$  __$$\ $$ |      
$$$$$$\  $$\  $$\  $$\ $$$$$$$\   $$$$\ $$ |$$ /  \__|$$ |      
$$  __$$\ $$ | $$ | $$ |$$  __$$\ $$ $$\$$ |$$ |$$$$\ $$ |      
$$ /  $$ |$$ | $$ | $$ |$$ |  $$ |$$ \$$$$ |$$ |\_$$ |$$ |      
$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |\$$$ |$$ |  $$ |$$ |      
$$$$$$$  |\$$$$$\$$$$  |$$ |  $$ |$$ | \$$ |\$$$$$$  |$$$$$$$$\ 
$$  ____/  \_____\____/ \__|  \__|\__|  \__| \______/ \________|
$$ |                                                            
$$ |                                                            
\__|
                                  
    ⌜―――――――――――――――――――――――――――――――――――――――――――――――――――――⌝
    ┇      [Github]  https://github.com/ItsYaBoiSimonx    ┇
    ┇      [Telegram] @StraightSW                         ┇
    ⌞―――――――――――――――――――――――――――――――――――――――――――――――――――――⌟
                          
                                                                                ''')))

def deviceid():
    return "".join(
        random.choice("0123456789abcdefghijklmnopqrstuvwxyz-") for i in range(36)
    )


def load_config(filename):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Config file not found. Creating a new one.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON. Check the format of the config file.")
        return {}

config = load_config("config.json")

username = config["username"]
question = config["message"]
num_threads = config["num_threads"] 
# It's recommended to keep num_threads at 350 through the config.json file
# If you have a lower end PC, just lower it until it works well enough.
# Although expect the message sending process to be slower.


# Add a variable to store the current proxy index
counter = 0
# Modify the sendmsg function to handle rate limiting and proxy rotation
def sendmsg():
    global username, question, counter, proxies

    while True:
        try:
            # Define proxies and their structure
            proxy = str(random.choice(proxies))
            proxyStructure = {
                "http://": f"http://{proxy}",
                "https://": f"http://{proxy}"
            }
            # Start up the HTTPX session
            session = httpx.Client(headers=headers, proxies=proxyStructure)
            # Define the request data

            dataToSubmit = {
                "username": username,
                "question": question,
                "deviceId": deviceid(),
            }
            # Handle all possible outcomes.
            postresp = session.post("https://ngl.link/api/submit",data=dataToSubmit)
            if postresp.status_code == 200:
                counter += 1
                os.system(f'title pwnNGL -=- Messages sent : {counter}')
                success(f"Sent '{question}' to victim using {proxy}, {counter} messages sent.")

            elif postresp.status_code == 404:
                error(f"User {username} does not exist")
                exit()

            elif postresp.status_code == 429:
                warning(f"Proxy {proxy} was ratelimited, sleeping for 10 seconds")

            elif postresp.status_code == 504 or 403:
                error(f"Bad proxy! {proxy}, removing")
                proxies.remove(proxy)

            else:
                error(f"Failed to send message using {proxy} report this error through Github pull requests! - Error {postresp.status_code}", Fore.RESET)
                time.sleep(5)

        except Exception as e:
            if "403" or "winerror" in str(e):
                pass
            else:
                print(f"{str(e)}")


def run_in_threads(num_threads, func):
    threads = []
    for i in range(int(num_threads)):
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

# Run the function in threads
run_in_threads(num_threads, sendmsg)