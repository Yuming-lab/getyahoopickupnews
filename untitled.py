import re
from bs4 import BeautifulSoup as BS
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

url = "https://news.yahoo.co.jp/"
homepage = requests.get(url)
homepage_soup = BS(homepage.text, "html.parser")
elements = homepage_soup.find_all(href = re.compile( "news.yahoo.co.jp/pickup/"))
pickup_links = [element.attrs["href"] for element in elements]

for pickup_link in pickup_links:
    pickuppage = requests.get(pickup_link)
    pickuppage_soup = BS(pickuppage.text, "html.parser")
    pickuppage_element = pickuppage_soup.find("div", class_= "sc-gdv5m1-8 eMtbmz")
    detail_link = pickuppage_element.contents[0].attrs["href"]
    detail_content = requests.get(detail_link)
    detail_soup = BS(detail_content.text, "html.parser")
    
    print(detail_soup.title.text)
    print(detail_link)
    
    detail_element = detail_soup.find(class_= re.compile("article_body highLightSearchTarget"))
    print(detail_element.text if hasattr(detail_element, "text") else "", end = "\n\n\n\n")

    thumbnail_div = detail_soup.find("div", class_=re.compile("thumbnail"))
    if thumbnail_div:
        img_tags = thumbnail_div.find_all("img")
    for img in img_tags:
        img_url = img.get("src")
        if img_url:
            img_response = requests.get(img_url)
            img_data = Image.open(BytesIO(img_response.content))
            plt.imshow(img_data)
            plt.axis("off")
            plt.show()

    print("\n\n\n")


from tkinter import messagebox

messagebox.showinfo('実行ファイル', '実行ファイルの動作確認が完了しました！')