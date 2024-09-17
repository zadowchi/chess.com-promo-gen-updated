import requests
import random
import os
import threading
import string

from pystyle import Colors
from tls_client import Session
from concurrent.futures import ThreadPoolExecutor

from modules.utils import *
from modules.ui import Logger

class ChessGen:

    def __init__(self):

        self.email = "".join(random.choices(string.ascii_lowercase, k=10)) + "@gmail.com"
        self.username = "".join(random.choices(string.ascii_lowercase, k=10))

        self.session = Session(client_identifier="chrome120")

        self.session.proxies = get_formatted_proxy(random.choice(proxies)) if proxies else None

        self.random_string = f"dd5ff8110f6b4e0687137443f{random.randint(1000000, 9999999)}"
        

    def _get_access_token(self) -> str:

        headers = {
            'Host': 'api.chess.com',
            'User-Agent': 'Chesscom-Android/4.6.34-googleplay (Android/13; Galaxy S9; en_US; contact #android in Slack)',
            'X-Client-Version': 'Android4.6.34',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'signed': 'Android4.6.34',
        }

        data = {
            'skillLevel': '1',
            'deviceId': self.random_string,
            'clientId': '1bc9f2f2-4961-11ed-8971-f9a8d47c7a48',
        }

        response = self.session.post('https://api.chess.com/v1/users/guest-login', params=params, headers=headers, data=data)

        try:
                
            access_token = response.json()["data"]["oauth"]["access_token"]

            return access_token
        
        except:
            Logger.Log("ERROR", "Failed to Fetch Access Token", Colors.red, status_code = str(response.status_code))

            Counter.Failed += 1

    def generate_account(self, access_token: str) -> str:

        headers = {
            'Host': 'api.chess.com',
            'User-Agent': 'Chesscom-Android/4.6.34-googleplay (Android/13; Galaxy S9; en_US; contact #android in Slack)',
            'X-Client-Version': 'Android4.6.34',
            'Accept-Language': 'en-US',
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'signed': 'Android4.6.34',
        }

        data = {
            'username': self.username,
            'password': 'Zadow@6969',
            'email': self.email,
            'deviceId': self.random_string,
            'bucketingId': self.random_string ,
            'clientId': '1bc9f2f2-4961-11ed-8971-f9a8d47c7a48',
            'onboardingType': 'september2022',
        }

        response = self.session.post('https://api.chess.com/v1/users', params=params, headers=headers, data=data)

        try:

            Counter.Registered += 1

            uuid = response.json()["data"]["uuid"]

            Logger.Log("CREATED", "Account Registered", Colors.blue, email = self.email, uuid = uuid)

            return uuid

        except:
            
            Logger.Log("ERROR", "Failed to Register Account", Colors.red, status_code = str(response.status_code))

            Counter.Failed += 1
        
    def fetch_promo(self, uuid: str) -> str:

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US;q=0.8, en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.chess.com',
            'priority': 'u=1, i',
            'referer': 'https://www.chess.com/play/computer/discord-wumpus?utm_source=chesscom&utm_medium=homepagebanner&utm_campaign=discord2024',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

        json_data = {
            'userUuid': uuid,
            'campaignId': '4daf403e-66eb-11ef-96ab-ad0a069940ce',
        }

        response = self.session.post(
            'https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode',
            headers=headers,
            json=json_data,
        )
        
        if "codeValue" in response.json():
            code = response.json()["codeValue"]

            Logger.Log("SUCCESS", "Promo Code Fetched", Colors.green, code = code)

            with open("output/promos.txt", "a") as f:
                f.write("https://discord.com/billing/promotions/" + code + "\n")

            Counter.PromosFetched += 1

        else:
            Logger.Log("ERROR", "Failed to Fetch Promo", Colors.red, status_code = str(response.status_code))

            Counter.Failed += 1

    def start(self):

        access = self._get_access_token()

        if not access:
            return

        uuid = self.generate_account(access)

        if uuid:
            self.fetch_promo(uuid)



def start_thread():

    while True:

        Chess = ChessGen()
        Chess.start()

os.system("cls" if os.name == "nt" else "clear")

try:

    proxies = open("input/proxies.txt", "r").read().splitlines()

except:
    Logger.Log("ERROR", "Failed to Load Proxies / Files Are Missing", Colors.red)

    os._exit(0)

threading.Thread(target=title_set_loop).start()

ThreadCount = int(Logger.w_Input("Enter Thread Count: "))

with ThreadPoolExecutor(max_workers=ThreadCount) as executor:
    for _ in range(int(ThreadCount)):
        executor.submit(start_thread)
