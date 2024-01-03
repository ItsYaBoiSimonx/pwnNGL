import datetime, os, httpx, random, threading, time
from colorama import Fore, Style
from pystyle import Colorate, Colors, Center
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




username = input(yellowint + " Enter the username of the NGL link - ")
question = input(yellowint + " Enter the message you want to send through - ")
num_threads = int(input(yellowint + " Enter the number of threads - "))



# Add a variable to store the current proxy index
counter = 0
# Modify the sendmsg function to handle rate limiting and proxy rotation
def sendmsg():
    global username, question, counter, proxies

    while True:
        try:
            proxy = str(random.choice(proxies))
            ssss = {
                "http://": f"http://{proxy}",
                "https://": f"http://{proxy}"
            }
            dataToSubmit = {
                    "username": username,
                    "question": question,
                    "deviceId": deviceid(),
                }
            client = httpx.Client(headers=headers, proxies=ssss)
            postresp = client.post("https://ngl.link/api/submit",data=dataToSubmit)
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
                error(f"Failed to send message using {proxy}. Error {postresp.status_code}", Fore.RESET)
                time.sleep(5)
        except Exception as e:
            if "403" or "winerror" in str(e):
                pass
            else:
                error(f"{str(e)}")


def run_in_threads(num_threads, func):
    threads = []
    for i in range(int(num_threads)):
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

while True:
    run_in_threads(num_threads, sendmsg)