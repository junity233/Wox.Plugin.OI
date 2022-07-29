from wox import *
import webbrowser
import requests
import json

def MakeOpenUrlAction(title,subtitle,url):
    return {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath":"logo.png",
                "JsonRPCAction":{
                    "method": "openUrl",
                    "parameters":[url],
                    "dontHideAfterAction":True
                }
    }

class Main(Wox):
    def search_page(self,text):
        res = requests.get("https://search.oi-wiki.org:8443",
            params={"s":text},
            headers={
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
                })

        if res.status_code != 200:
            return []
        
        res = json.loads(res.text)

        result = []
        for i in res:
            title = i["title"]
            subtitle = ""
            if "highlight" in i:
                subtitle = i["highlight"][0].replace("<em>","").replace("</em>","")
            else:
                subtitle = i["title"]
            
            url = "https://oiwiki.org"+i["url"]
            result.append(MakeOpenUrlAction(title,subtitle,url))

        return result

    def query(self,text):
        
        if text.strip() == "":
            return [MakeOpenUrlAction("打开OI Wiki","在浏览器中打开OI Wiki","https://oiwiki.org")]
        else:
            return self.search_page(text)
    
    def openUrl(self,url):
        webbrowser.open(url)

if __name__ == "__main__":
    Main()