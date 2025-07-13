import os,json,random,re
from time import sleep
try :
     import requests
     from colorama import init, Fore
     from bs4 import BeautifulSoup as bs
except ImportError:
     print(f"[!] Installing module…")
     os.system("pip install -r requirements.txt")
     print(f"\r[√] Module has ben installed")
     sleep(1)
     os.system("python run.py")
     exit()

# Color
init(autoreset=True)
L = "\033[1;97m"
W = Fore.WHITE
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
M = Fore.MAGENTA
RGB = random.choice([G,Y,C,M])
D = f"{RGB}[√]{W} "
F = f"{RGB}[!]{W} "
P = f"{RGB}[?]{W} "
E = f"{RGB}[X]{W} "
# MainCode

def clear():
    os.system("clear")

def baris():
    print(f"{Fore.RED}－{W}"*27)

def banner():
    clear()
    baris()
    print(f"""{L}{RGB}   
              ╔╦╗┬┬┌─╔╦╗┌─┐┌─┐┬  ┌─┐
               ║ │├┴┐ ║ │ ││ ││  └─┐
               ╩ ┴┴ ┴ ╩ └─┘└─┘┴─┘└─┘{W}
             Tiktok auto likes & views
             {RGB}https://github.com/AinxBOT{W}""")
    baris()

def countdown(waktu):
    for i in range(waktu, 0, -1):
        print(f"\r{F}Waiting in {RGB}{i} {W}sec...",end="",flush=True)
        sleep(1)

def back():
    while True:
         lagi = input(f"{P}Back to menu or Exit? {RGB}(Y/N){W} : {RGB}")
         if lagi.lower() == "y":
            os.system("python run.py")
            break
         elif lagi.lower() == "n":
            exit(f"{E}Program closed")
         else:
            print(f"{F}Wrong input")

class Tiktok:
    def __init__(self,useragent,cookie):
        self.agent = useragent
        self.cookie = {"cookie":cookie}
        self.header_logintk = {"method":"GET","authority":"www.tiktok.com","path":"/login/","scheme":"https","sec-ch-ua":'"Not;A=Brand";v="99", "Android WebView";v="139", "Chromium";v="139"',"sec-ch-ua-mobile":"?1","sec-ch-ua-platform":'"Android"',"upgrade-insecure-requests":"1","user-agent":self.agent,"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","x-requested-with":"com.rajeliker","sec-fetch-site":"none","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7","priority":"u=0, i"}
        self.ses = requests.Session()
    def login_tiktok(self):
        self.ses.headers.update(self.header_logintk)
        self.ses.get("https://www.tiktok.com/login/",cookies = self.cookie)
        self.ses.headers.clear()
        self.ses.headers.update({"user-agent":self.agent,"accept":"application/json, text/plain, */*","accept-encoding":"gzip","cookie":self.cookie["cookie"],"host":"www.tiktok.com","referer":"https://www.tiktok.com/"})
        log = self.ses.get("https://www.tiktok.com")
        if '<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">{' in str(log.text):
           if "tt_chain_token=" not in str(self.cookie["cookie"]):
               self.cookie["cookie"] += (";" if not self.cookie["cookie"].endswith(";") else "") + f"tt_chain_token={log.cookies['tt_chain_token']}"
           data_script = json.loads(bs(log.text,"html.parser").find("script",id="__UNIVERSAL_DATA_FOR_REHYDRATION__").text)["__DEFAULT_SCOPE__"]["webapp.app-context"]
           user = data_script["user"]
           return {"token":user["secUid"],"uid":user["uid"],"name":user["nickName"],"username":user["uniqueId"],"image":user["avatarUri"][0],"ua":data_script["userAgent"],"kukis":self.cookie["cookie"]}
        else:
           exit(f"{F}Account checkpoint or not found")
    def getpostid(self,datapanel,posturl):
        if "vm.tiktok.com" in str(posturl):
            head = {"user-agent":self.agent,"accept":"application/json, text/plain, */*","accept-encoding":"gzip","cookie":datapanel["cookies"],"host":"vm.tiktok.com","referer":"https://www.tiktok.com/"}
            req = self.ses.get(posturl, headers = head, allow_redirects = True)
            if "https://t.tiktok.com/" in str(req.url):
               head.clear()
               head.update({"user-agent":"Dart/3.6 (dart:io)","accept":"application/json, text/plain, */*","accept-encoding":"gzip","referer":"https://www.tiktok.com/","host":"t.tiktok.com"})
               res = self.ses.get(req.url, headers = head, allow_redirects=True)
               if "https://www.tiktok.com/@" in str(res.url):
                  head.update({"host":"www.tiktok.com"})
                  last = bs(self.ses.get(res.url,headers = head).text,"html.parser").find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
                  if last:
                     try:
                         data_script = json.loads(last.text)["__DEFAULT_SCOPE__"]["webapp.video-detail"]['itemInfo']['itemStruct']
                     except KeyError:
                         data_script = json.loads(last.text)["__DEFAULT_SCOPE__"]["webapp.reflow.video.detail"]['itemInfo']['itemStruct']
                     idpost = data_script["video"]["id"]
                     datapost = data_script["stats"]
                     authorpost = data_script["author"]
                     return {"pid":idpost,"like":datapost["diggCount"],"views":datapost["playCount"],"author":authorpost["nickname"],"uid":authorpost["uniqueId"],"url":posturl}
                  else:
                     exit(f"{F}Failed get postdata")
               else:
                  exit(f"{F}Failed get postdata")
            else:
               exit(f"{F}Failed get postdata")
        elif "vt.tiktok.com" in str(posturl):
            head = {"user-agent":self.agent,"accept":"application/json, text/plain, */*","accept-encoding":"gzip","cookie":datapanel["cookies"],"host":"vt.tiktok.com","referer":"https://www.tiktok.com/"}
            req = self.ses.get(posturl, headers = head, allow_redirects = True)
            if "www.tiktok.com/@" in str(req.url):
               head.clear()
               head.update({"user-agent":"Dart/3.6 (dart:io)","accept":"application/json, text/plain, */*","accept-encoding":"gzip","referer":"https://www.tiktok.com/","host":"www.tiktok.com"})
               last = bs(self.ses.get(req.url,headers = head).text,"html.parser").find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
               if last:
                  try:
                      data_script = json.loads(last.text)["__DEFAULT_SCOPE__"]["webapp.video-detail"]['itemInfo']['itemStruct']
                  except KeyError:
                      data_script = json.loads(last.text)["__DEFAULT_SCOPE__"]["webapp.reflow.video.detail"]['itemInfo']['itemStruct']
                  idpost = data_script["video"]["id"]
                  datapost = data_script["stats"]
                  authorpost = data_script["author"]
                  return {"pid":idpost,"like":datapost["diggCount"],"views":datapost["playCount"],"author":authorpost["nickname"],"uid":authorpost["uniqueId"],"url":posturl}
               else:
                  exit(f"{F}Failed get postdata")
            else:
              exit(f"{F}Failed get postdata")
        else:
            exit(f"{F}Only for links : {RGB}(vt.tiktok.com) {W}or {RGB}(vm.tiktok.com){W}")

class Panel:
    def __init__(self,data_tiktok,sesi):
        self.info = data_tiktok
        self.bearer = sesi
        self.header = {"user-agent":"Dart/3.6 (dart:io)","cache-control":"no-cache","accept-encoding":"gzip","authorization":self.bearer,"host":"rajeliker.autolikerlive.com","pragma":"no-cache","content-type":"application/json"}
        self.api = "https://rajeliker.autolikerlive.com/api/v1/"
        self.ses = requests.Session()
    def loginpanel(self):
        refer = self.info["uid"][:-1] + ("1" if self.info["uid"][-1] == "0" else "0")
        data_login = json.dumps({"id":self.info["uid"],"name":self.info["name"],"token":self.info["token"],"cookies":self.info["kukis"],"fcm":"Still need to check how to get it","loginType": "tt","refer_id":refer,"ua":self.info["ua"],"profilePic":self.info["image"]})
        req = self.ses.post(f"{self.api}login", data = data_login, headers = self.header)
        if not '{"id":' in str(req.text):
           exit(f"{F}Failed login panel")
        else:
           data_panel = json.loads(req.text)
           with open("useragent.txt","w") as ug:
                ug.write(self.info["ua"])
           with open("authorization.txt","w") as au:
                au.write("Bearer "+data_panel["session"])
           with open("cookies.txt","w") as cs:
                cs.write(data_panel["cookies"])
           return data_panel
    def getservices(self,datapanel):
        self.header.update({"authorization":f'Bearer {datapanel["session"]}'})
        actid = []
        req = requests.post(f"{self.api}getServices",data = json.dumps({"loginType": "tt"}), headers = self.header).text
        if '[{"id":' in str(req):
           for x in json.loads(req):
               actid.append(x["id"])
        return actid
    def refresh(self,datapanel):
        self.header.update({"authorization":f'Bearer {datapanel["session"]}'})
        token = self.ses.post(f"{self.api}refresh", headers = self.header).text
        if '{"adToken"' in str(token):
           return json.loads(token)["adToken"]
        else:
           exit(f"{F}Refresh failed,session limited")
    def mycredit(self,datapanel):
        self.header.update({"authorization":f'Bearer {datapanel["session"]}'})
        req = requests.post(f"{self.api}getCredits", headers = self.header).text
        if '{"credits":' in str(req):
           print(f"{RGB}[$] {W}Credits  : {RGB}{json.loads(req)['credits']}")
        else:
           exit(f"{F}Failed get credits info")
    def earning(self,datapanel):
        done = 0
        die = 0
        self.header.update({"authorization":f'Bearer {datapanel["session"]}'})
        earndata = {"loginType":"tt","adtoken":datapanel["adToken"]}
        req = requests.post(f"{self.api}earnAdCredit", data = json.dumps(earndata), headers = self.header).text
        if '{"success":true,"message":"Credit Earned Success"}' in str(req):
           done +=1
        else:
           die +=1
           earndata.update({"adtoken":info.refresh(datapanel)})
           requests.post(f"{self.api}earnAdCredit", data = json.dumps(earndata), headers = self.header)
    def addvl(self, datapanel, datapost, action_type, last_count):
        self.header.update({"authorization": f'Bearer {datapanel["session"]}'})
        sid = info.getservices(datapanel)
        sid_used = sid[0] if action_type == "views" else sid[1]
        actdata = json.dumps({"post_id": datapost["pid"],"service_id": sid_used,"reaction_id": "1635855486666999","limit": 1,"url": datapost["url"]})
        req = self.ses.post(f"{self.api}send", data=actdata, headers=self.header).text
        if "error" in req:
           for i in range(20):
               info.earning(datapanel)
               percent = (i + 1) * 5
               print(f"\r{F}Earning credits... {RGB}[{percent}%]{W}", end="", flush=True)
               sleep(1.5)
           print(f"\r{RGB}[↓] {W}Continue add {action_type}...", end=" "*15, flush=True)
        elif "Action sent successfully" in req or "success" in req:
           print(f"\r{D}Success add {action_type}", end=" "*10, flush=True)
           sleep(60 if action_type == "views" else 5)
           dump = login.getpostid(datapanel, datapost["url"])
           updated = dump["views"] if action_type == "views" else dump["like"]
           if updated > last_count:
              print(f"\n{RGB}[+] {W}Update {action_type} : {RGB}{updated}{W}")
              baris()
              return updated
           elif action_type == "likes":
              print(f"\n{F}Please check the post in a few hours.")
              baris()
           else:
              return last_count
        else:
           exit(f"\n{E}Session limited")

def dummyinfo():
    print(f"{RGB}[-] {W}Login as : {RGB}{data_panel['name']}\n{RGB}[-] {W}UID      : {RGB}{data_panel['id']}")
    info.mycredit(data_panel)
    baris()

def menu():
    while True:
        banner()
        dummyinfo()
        print(f"{RGB}01). {W}Add views\n{RGB}02). {W}Add likes\n{RGB}03). {W}Earn credits\n{RGB}00). {W}Exit")
        pilih = input(f"{P} >> {RGB}")
        baris()
        if pilih in ["01","1"]:
           url = input(f"{P}Post link : {RGB}")
           dump = login.getpostid(data_panel,url)
           print(f"{RGB}>> {W}Get data post {RGB}<<\n>> {W}From     : {RGB}{dump['author']}\n>> {W}Username : {RGB}{dump['uid']}\n>> {W}PostID   : {RGB}{dump['pid']}\n>> {W}Current views : {RGB}{dump['views']}")
           last_views = dump["views"]
           print(f"{F}CTRL C for stop")
           baris()
           while True:
                countdown(random.choice([5,7,9]))
                info.addvl(data_panel,dump,"views",last_views)
           break
        elif pilih in ["02","2"]:
           print(f"{F}Notes : {RGB}Likes may be delayed! \nUsually appear after 1–2 hours or longer.\nPlease keep checking your post,\nor open TikTok app to refresh.")
           baris()
           url = input(f"{P}Post link : {RGB}")
           dump = login.getpostid(data_panel,url)
           print(f"{RGB}>> {W}Get data post {RGB}<<\n>> {W}From     : {RGB}{dump['author']}\n>> {W}Username : {RGB}{dump['uid']}\n>> {W}PostID   : {RGB}{dump['pid']}\n>> {W}Current likes : {RGB}{dump['like']}")
           last_likes = dump["like"]
           print(f"{F}CTRL C for stop")
           baris()
           while True:
                countdown(30)
                info.addvl(data_panel,dump,"likes",last_likes)
           break
        elif pilih in ["03","3"]:
           print(f"{F}CTRL C for stop")
           baris()
           while True:
              countdown(10)
              info.earning(data_panel)
              print(f"\r{D}Earning credits...",end=" "*10,flush=True)
              print()
              info.mycredit(data_panel)
           baris()
           break
        elif pilih in ["00","0"]:
              exit(f"{F}Byee bro, dont forget sub my channel(^‿^)")
        else:
           print(f"{E}Wrong input")
           sleep(1)
if __name__=="__main__":
    try:
        try:
            ua = open("useragent.txt","r").read()
        except FileNotFoundError:
            banner()
            ua = input(f"{P}User agent : {RGB}")
        try:
            ck = open("cookies.txt","r").read()
        except FileNotFoundError:
            banner()
            ck = input(f"{F}Notes : {RGB}Use dummy account\n{P}Cookies : {RGB}")
        try :
            auth = open("authorization.txt","r").read()
        except FileNotFoundError:
            tkt = Tiktok(ua,ck)
            usr = tkt.login_tiktok()
            log = Panel(usr,"Bearer ")
            bear = log.loginpanel()["session"]
            auth = f"Bearer {bear}"
        login = Tiktok(ua,ck)
        user = login.login_tiktok()
        info = Panel(user,auth)
        data_panel = info.loginpanel()
        menu()
    except KeyboardInterrupt:
        print(f"\n{F}Program stopped")
        back()
    except requests.exceptions.ConnectionError:
        exit(f"\n{F}Check your connection and run again program")
    except Exception as e:
        exit(f"\n{F}Unexpected error : {RGB}{e}")
