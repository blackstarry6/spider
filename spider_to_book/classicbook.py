import concurrent.futures
import requests
import re

import concurrent.futures
import time
from tqdm import tqdm
import csv
import random

# 随机 User-Agent 列表，避免被网站屏蔽
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64",
    # 可以根据需要添加更多的 User-Agent
]


#获取网页
def request_web(url,retries=3):
    headers = {
        'User-Agent': random.choice(USER_AGENTS)  # 随机选择一个 User-Agent
    }
    try:
        response = requests.get(url,headers=headers,timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(e)
        return None

#解析网页获取书籍基本信息和章节信息

#书名，作者，书籍类型
#
#
#网页解析
def parse_result(html):
    html=re.sub(r'[\t\n]', '',html)
    pattern=re.compile(r'<div class="book-describe">.*?<h1>(.*?)</h1>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>.*?</p>.*?<p>.*?</p>.*?<p>.*?</p>.*?<p>(.*?)</p>.*?<div class="describe-html"><p>(.*?)</p>.*?<h2 class="ac clearfix">',re.S)
    results=pattern.findall(html)
    with open('output.txt', 'w', encoding='utf-8') as f:
        for tup in results:
            for item in tup:
                f.write(item + '\n')  # 每个元素单独一行
            f.write('\n')  # 元组之间加一个空行

    print("数据已写入文件")
   
#数据写入文件
def write_item_to_file(item):
    print('开始写入数据 ====> ' + str(item))
    with open('book1.txt', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

#目标地址页面的获取，解析和数据写入
def main():
    url='https://www.kunnu.com/dongwunongchang/'
    html = request_web(url)
    parse_result(html)  # 解析过滤我们想要的信息


if __name__ == "__main__":
    main()
    

