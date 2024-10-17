import tkinter as tk
import os
import json
import twstock
import matplotlib.pyplot as plt
from pylab import mpl
import requests
from bs4 import BeautifulSoup


def _hit11():
    global a
    if entrY11.get() == "":
        return
    a = entrY11.get()
    entrY11.delete(0, "end")
    entrY11.focus()





def _hit2():
    global a, info
    info = twstock.codes[a]
    b = info.name
    stock2330 = twstock.Stock(a)
    stock2330.fetch_from(2022, 1)
    mpl.rcParams['font.family'] = 'Microsoft JhengHei'  # 設定中文字型為微軟正黑體
    mpl.rcParams['axes.unicode_minus'] = False
    plt.title(b, fontsize=24)
    plt.xlabel('after 2022/1', fontsize=14)
    plt.ylabel('price', fontsize=14)
    plt.plot(stock2330.price)
    plt.show()


# 修改 _hit3 函數
def _hit3():
    global a, c, d, q, url1, soup1, rq1, soups1, mysoup1

    url = "https://tw.stock.yahoo.com/quote/" + str(a) + ".TW"
    c = []
    d = []
    rq = requests.get(url).text

    soup = BeautifulSoup(rq, "html5lib")
    soups = soup.find("ul", "My(0) P(0) Wow(bw) Ov(h)")

    for mySoup in soups.find_all("li"):
        try:
            c.append(mySoup.a.text)
            url1 = mySoup.a["href"]
            rq1 = requests.get(url1).text
            soup1 = BeautifulSoup(rq1, "html5lib")
            soups1 = soup1.find("div", "caas-content-wrapper")

            temp_d = []  # 暫時存儲段落內容的列表
            for mysoup1 in soups1.find_all("div", "caas-body"):
                paragraphs = mysoup1.find_all("p")  # 找到所有 <p> 標籤
                for p in paragraphs:
                    temp_d.append(p.text.strip())  # 將每個段落內容加入暫時列表中

            d.append(temp_d)  # 將暫時列表添加到 d 中

        except Exception as e:
            print("Error:", e)
            continue

    wiN3 = tk.Toplevel(wiN)
    wiN3.title("股票新聞!!!")
    wiN3.geometry("800x700+650+200")
    wiN3.configure(bg='yellow')

    # 創建 Listbox 用於顯示新聞標題
    listbox = tk.Listbox(wiN3, bg="lightblue", font=("Arial", 16), width=60, height=20)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 將新聞標題添加到 Listbox 中
    for i, title in enumerate(c):
        listbox.insert(tk.END, title)

    # 綁定事件
    listbox.bind("<Button-1>", lambda event: _view_d_contents(listbox.curselection()))

    # 創建垂直卷軸
    scrollbar = tk.Scrollbar(wiN3, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 綁定卷軸到 Listbox
    listbox.config(yscrollcommand=scrollbar.set)

    # 添加離開按鈕
    btN320 = tk.Button(wiN3, text="離開!!", fg="blue", font=("Arial", 16), width=10, height=2, command=wiN3.destroy)
    btN320.pack()


# 修改 _view_d_contents 函數
def _view_d_contents(selection):
    if selection:
        # 取得相應的內容
        index = selection[0]
        content = d[index]

        # 創建一個新的 Toplevel 窗口
        wiN4 = tk.Toplevel(wiN)
        wiN4.title("內容!!!")
        wiN4.geometry("1500x1000+400+200")
        wiN4.configure(bg='lightgreen')

        # 在新窗口中顯示內容，使用 Label 並在文本中使用 \n 進行換行
        tk.Label(wiN4, text="\n".join(content), bg="lightgreen", font=("Arial", 20), wraplength=1400).pack()




def _hit4():
    qQ=tk.messagebox.askokcancel("提示","確定要結束程式嗎???")
    if qQ:
        ff=open("dd.json","w",encoding="utf-8")
        json.dump(dd,ff,ensure_ascii=False,indent=4)
        wiN.destroy()


if os.path.isfile("dd.json"):
    with open("dd.json", "r", encoding="utf-8") as ff:
        dd = json.load(ff)
else:
    dd = {}

wiN = tk.Tk()
wiN.title("股票!!!")
a = 2330
wiN.configure(bg='lightblue')
wiN.geometry("1000x800+700+300")
wiN.resizable(width=False, height=False)

lbL11 = tk.Label(wiN, text="股票代碼", fg="black", bg="lightblue", font=("Arial", 20), width=70, height=2)
lbL11.pack()

entrY11 = tk.Entry(wiN, font=("Arial", 20), bd=10)
entrY11.pack()
btN11 = tk.Button(wiN, text="查詢", bg="white", font=("Arial", 20), width=10, height=2, command=_hit11)
btN11.pack()
btN2 = tk.Button(wiN, text="股票資訊", bg="lightblue", font=("Arial", 20), width=30, height=2, command=_hit2)
btN2.pack()
btN3 = tk.Button(wiN, text="顯示新聞", bg="lightblue", font=("Arial", 20), width=30, height=2, command=_hit3)
btN3.pack()
btN4 = tk.Button(wiN, text="離開", bg="lightblue", font=("Arial", 20), width=30, height=2, command=_hit4)
btN4.pack()

wiN.mainloop()
