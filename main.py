import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
init()

start_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

header = {
    "Referer": "https://linkvertise.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

hwid = input(Fore.YELLOW + "[INFO] Enter your hwid: ")

if not hwid.startswith("https://flux.li/android/external/start.php?HWID="):
    url = f"https://flux.li/android/external/start.php?HWID={hwid}"
else:
    url = hwid

check_1 = "https://flux.li/android/external/check1.php"
key_url = "https://flux.li/android/external/main.php"

session = requests.Session()

response = session.get(url, headers=start_header).text
if "You will be redirected in" in response:
    session.get(check_1, headers=header)
    key = BeautifulSoup(str(session.get(key_url, headers=header).text), 'html.parser').find_all(attrs={"data-aos": "fade-left"})[2].text.strip()
    print(Fore.GREEN + f"[SUCCESS] Your key: {key}")
else:
    print(Fore.RED + "[ERROR] Can't get key!")
