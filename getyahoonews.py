import re
from bs4 import BeautifulSoup as BS
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd

url = "https://news.yahoo.co.jp/"
homepage = requests.get(url)
homepage_soup = BS(homepage.text, "html.parser")
elements = homepage_soup.find_all(href = re.compile( "news.yahoo.co.jp/pickup/"))
pickup_links = [element.attrs["href"] for element in elements]

news_list = []  #Excel に書くための入れ物

for pickup_link in pickup_links:
    pickuppage = requests.get(pickup_link)
    pickuppage_soup = BS(pickuppage.text, "html.parser")
    pickuppage_element = pickuppage_soup.find("div", class_= "sc-gdv5m1-8 eMtbmz")
    detail_link = pickuppage_element.contents[0].attrs["href"]
    detail_content = requests.get(detail_link)
    detail_soup = BS(detail_content.text, "html.parser")
    
    title = detail_soup.title.text if detail_soup.title else ""
    body_element = detail_soup.find(class_= re.compile("article_body highLightSearchTarget"))
    body = body_element.text.strip() if hasattr(body_element, "text") else ""

    print(title)
    print(detail_link)
    print(body, end = "\n\n\n\n")

    # ★ここで1ニュースぶんをリストに追加
    news_list.append({
        "タイトル": title,
        "URL": detail_link,
        "本文": body
    })

    print("\n\n\n")

# ★ループが終わったら Excel 出力
df = pd.DataFrame(news_list)
save_path = r"C:\Users\yumin\OneDrive\デスクトップ\プロフラム\getyahoopickupnews\yahoo_news.xlsx"
df.to_excel(save_path, index=False)

from tkinter import messagebox
messagebox.showinfo('実行ファイル', '実行ファイルの動作確認が完了しました！')
