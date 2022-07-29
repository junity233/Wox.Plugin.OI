from wox import *
import webbrowser
import requests
import json

def MakeOpenUrlAction(title,subtitle,url):
    return {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath":"logo.jpg",
                "JsonRPCAction":{
                    "method": "openUrl",
                    "parameters":[url],
                    "dontHideAfterAction":True
                }
    }

def MakeOpenProblemAction(problem):
    difficulty_str = ["暂无评定","入门","普及-","普及/提高-","普及+/提高","提高+/省选-","省选/NOI-","NOI/NOI+/CTSC"]

    pid = problem["pid"]
    title = problem["title"]
    difficulty = problem["difficulty"]
    fullScore = problem["fullScore"]
    totalSubmit = problem["totalSubmit"]
    totalAccepted = problem["totalAccepted"]

    return {
                "Title": f"{problem['pid']} {problem['title']}",
                "SubTitle": f"难度:{difficulty_str[difficulty]} 总分:{fullScore} 提交数:{totalSubmit} 通过数:{totalAccepted} 通过率:{totalAccepted/totalSubmit*100:.2f}%",
                "IcoPath":"logo.jpg",
                "JsonRPCAction":{
                    "method": "openProblem",
                    "parameters":[problem['pid']],
                    "dontHideAfterAction":True
                }
    }

class Main(Wox):
    def search_problem(self,text):
        res = requests.get("https://www.luogu.com.cn/problem/list",
            params={"keyword":text,"_contentOnly":1},
            headers={
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
                });
        res_data= json.loads(res.text)

        result = []

        if res_data["code"] !=200:
            return []
        
        currentData=res_data["currentData"]

        for problem in currentData["problems"]["result"]:
            result.append(MakeOpenProblemAction(problem))
        
        return result


    def query(self,text):
        texts = []
        result = []
        
        for i in text.strip().split(" "):
            if i.replace(" ","") != "":
                texts.append(i)

        if len(texts) >= 1:
            command = texts[0]
            if command == "jump" and len(texts) >= 2:
                problem = texts[1]
                result.append(MakeOpenUrlAction(f"打开题目 {problem}",f"在浏览器中打开题目 {problem}",f"https://www.luogu.com.cn/problem/{problem}"))
            elif command == "search":
                if len(texts) >= 2:
                    problem = texts[1]
                    for i in self.search_problem(problem):
                        result.append(i)
            elif command == "class":
                result.append(MakeOpenUrlAction("打开洛谷网校","在浏览器中打开洛谷网校","https://class.luogu.com.cn/"))
                    
        else:
            result.append(MakeOpenUrlAction("打开洛谷主页","在浏览器中打开洛谷主页","https://www.luogu.com.cn/"))

        return result
    
    def openUrl(self,url):
        webbrowser.open(url)

    def openProblem(self,pid):
        webbrowser.open(f"https://www.luogu.com.cn/problem/{pid}")

if __name__ == "__main__":
    Main()