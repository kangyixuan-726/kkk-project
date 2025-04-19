import requests
url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    html_content = response.text
else:
    print(f"请求失败，状态码：{response.status_code}")
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, "html.parser")

# 提取所有电影条目
movie_items = soup.find_all("div", class_="item")

movies = []
for item in movie_items:
    # 电影标题
    title = item.find("span", class_="title").text.strip()
    # 评分
    rating = item.find("span", class_="rating_num").text.strip()
    # 导演和年份
    info = item.find("div", class_="bd").find("p").text.strip().split("\n")[0]
    # 链接
    link = item.find("a")["href"]
    
    movies.append({
        "标题": title,
        "评分": rating,
        "信息": info,
        "链接": link
    })

# 打印前3条数据
print(movies[:3])
import time

all_movies = []

for page in range(0, 10):  # 抓取前10页（250条数据）
    start = page * 25
    url = f"https://movie.douban.com/top250?start={start}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_items = soup.find_all("div", class_="item")
    
    # 提取当前页数据（复用步骤3.1的代码）
    # ...（省略提取代码，同上）
    
    all_movies.extend(movies)
    time.sleep(2)  # 防止请求频率过高被封IP
import pandas as pd
df = pd.DataFrame(all_movies)
df.to_csv("douban_top250.csv", index=False, encoding="utf-8-sig")

import asyncio
from pyppeteer import launch
async def main():
       browser = await launch()
       page = await browser.newPage()
       await page.goto('https://www.baidu.com')
       await page.screenshot({'path': 'screenshot.png'})
       await browser.close()

asyncio.get_event_loop().run_until_complete(main())