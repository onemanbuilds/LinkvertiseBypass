from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count,Timer
from time import sleep
from datetime import datetime
from base64 import b64encode
import requests
import json

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def ReadJson(self,filename,method):
        with open(filename,method) as f:
            return json.load(f)

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('[Data]/useragents.txt','r')
        return choice(useragents)

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
        proxies = {}
        if self.use_proxy == 1:
            if self.proxy_type == 1:
                proxies = {
                    "http":"http://{0}".format(choice(proxies_file)),
                    "https":"https://{0}".format(choice(proxies_file))
                }
            elif self.proxy_type == 2:
                proxies = {
                    "http":"socks4://{0}".format(choice(proxies_file)),
                    "https":"socks4://{0}".format(choice(proxies_file))
                }
            else:
                proxies = {
                    "http":"socks5://{0}".format(choice(proxies_file)),
                    "https":"socks5://{0}".format(choice(proxies_file))
                }
        else:
            proxies = {
                    "http":None,
                    "https":None
            }
        return proxies

    def CalculateCpm(self):
        self.cpm = self.maxcpm * 60
        self.maxcpm = 0
        Timer(1.0, self.CalculateCpm).start()

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'[One Man Builds Linkvertise Bypass Tool] ^| HITS: {self.hits} ^| BADS: {self.bads} ^| CPM: {self.cpm} ^| WEBHOOK RETRIES: {self.webhook_retries} ^| RETRIES: {self.retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.SetTitle('[One Man Builds Linkvertise Bypass Tool]')
        self.clear()
        self.title = Style.BRIGHT+Fore.GREEN+"""                                        
                                  ╔═════════════════════════════════════════════════╗    
                                             ╦  ╦╔╗╔╦╔═╦  ╦╔═╗╦═╗╔╦╗╦╔═╗╔═╗
                                             ║  ║║║║╠╩╗╚╗╔╝║╣ ╠╦╝ ║ ║╚═╗║╣ 
                                             ╩═╝╩╝╚╝╩ ╩ ╚╝ ╚═╝╩╚═ ╩ ╩╚═╝╚═╝
                                  ╚═════════════════════════════════════════════════╝

                
        """
        print(self.title)
        self.hits = 0
        self.bads = 0
        self.retries = 0
        self.webhook_retries = 0
        self.cpm = 0
        self.maxcpm = 0
        self.lock = Lock()
        self.session = requests.Session()

        config = self.ReadJson('[Data]/configs.json','r')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads_num = config['threads']
        self.salt = config['salt']
        self.webhook_enable = config['webhook_enable']
        self.webhook_url = config['webhook_url']

        print('')

    def SendWebhook(self,title,message,icon_url,thumbnail_url,proxy,useragent):
        try:
            timestamp = str(datetime.utcnow())

            message_to_send = {"embeds": [{"title": title,"description": message,"color": 65362,"author": {"name": "AUTHOR'S DISCORD SERVER [CLICK HERE]","url": "https://discord.gg/9bHfzyCjPQ","icon_url": icon_url},"footer": {"text": "MADE BY ONEMANBUILDS","icon_url": icon_url},"thumbnail": {"url": thumbnail_url},"timestamp": timestamp}]}
            
            headers = {
                'User-Agent':useragent,
                'Pragma':'no-cache',
                'Accept':'*/*',
                'Content-Type':'application/json'
            }

            payload = json.dumps(message_to_send)

            response = self.session.post(self.webhook_url,data=payload,headers=headers,proxies=proxy)

            if response.text == "":
                pass
            elif "You are being rate limited." in response.text:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
            else:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
        except:
            self.webhook_retries += 1
            self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)

    def Bypass(self,link):
        try:
            useragent = self.GetRandomUserAgent()
            headers = {
                'Host':'publisher.linkvertise.com',
                'Connection':'keep-alive',
                'sec-ch-ua':'"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile':'?0',
                'Accept':'*/*',
                'Sec-Fetch-Site':'cross-site',
                'Sec-Fetch-Mode':'cors',
                'Sec-Fetch-Dest':'empty',
                'Accept-Language':'en-US,en;q=0.9',
                'User-Agent':useragent
            }

            proxy = self.GetRandomProxy()
            id = link.split('/')[3]
            name = link.split('/')[4]
            id_name = f'{id}/{name}'
            
            start_link = link

            api_link = f'https://publisher.linkvertise.com/api/v1/redirect/link/static/{id_name}'
            
            response = self.session.get(api_link,headers=headers,proxies=proxy)
            
            self.maxcpm += 1

            if 'Es ist ein technischer Fehler aufgetreten.' in response.text or '<title>Linkvertise - Earn Money with Links | Monetization done right</title>' in response.text:
                self.bads += 1
                self.PrintText(Fore.WHITE,Fore.RED,'BAD',start_link)
                with open('[Data]/[Results]/bads.txt','a',encoding='utf8') as f:
                    f.write(f'{start_link}\n')
            elif '"success":true,"' in response.text:
                link_id = response.json()['data']['link']['id']
                link_id_salt = f'{link_id}{self.salt}'
                link_id_salt = link_id_salt[1:len(link_id_salt)]
                link_id_salt_b64 = b64encode(link_id_salt.encode())
                
                api_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/{0}/target?serial=eyJ0aW1lc3RhbXAiOjE2MTEzNTQyODUyNjMsInJhbmRvbSI6IjY1NDgzMDciLCJsaW5rX2lkIjoy{1}'.format(id_name,link_id_salt_b64.decode('utf-8'))
                response = self.session.get(api_link,headers=headers,proxies=proxy)
            
                valid_link = response.json()['data']['target'].replace('\\','')
                self.hits += 1
                self.PrintText(Fore.WHITE,Fore.GREEN,'HIT',valid_link)
                with open('[Data]/[Results]/hits.txt','a',encoding='utf8') as f:
                    f.write(f'{valid_link}\n')
                if self.webhook_enable == 1:
                    self.SendWebhook('Linkvertise Bypass',valid_link,'https://cdn.discordapp.com/attachments/776819723731206164/796935218166497352/onemanbuilds_new_logo_final.png','https://ps.w.org/linkvertise-script-api/assets/icon-256x256.png?rev=2080593',proxy,useragent)
            else:
                self.retries += 1
                self.Bypass(link)
        except:
            self.retries += 1
            self.Bypass(link)

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        self.CalculateCpm()
        links = self.ReadFile('[Data]/links.txt','r')
        for link in links:
            Run = True
            while Run:
                if active_count()<=self.threads_num:
                    Thread(target=self.Bypass,args=(link,)).start()
                    Run = False

if __name__ == '__main__':
    main = Main()
    main.Start()