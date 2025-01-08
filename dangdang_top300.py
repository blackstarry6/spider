import concurrent.futures
import requests
import re

import concurrent.futures
import time
from tqdm import tqdm
import csv
import pandas as pd

#获取当当网网页
def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(e)
        return None

#网页解析
def parse_result(html):
    pattern = re.compile(
        r'<li.*?list_num.*?(\d+)\.</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span class="price_n">(.*?)</span>.*?</li>', re.S)
#页号，书籍图片地址，书名
#推荐比例，作者，五星评分次数
#价格
    items = re.findall(pattern, html)
    for item in items:
        yield (
            item[0],
            item[1],
            item[2],
            item[3],
            item[4],
            item[5],
            item[6]
        )


#迭代器数据写入文件
def write_item_to_file(data_iterator):
    with open('output.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data_iterator)

#目标地址页面的获取和解析
def main(page):
    try:
        url = 'http://bang.dangdang.com/books/fivestars/1-' + str(page)
        html = request_dandan(url)
        items = parse_result(html)  # 解析过滤我们想要的信息
        return items
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

#获取总分页数
def get_pagination_num():
    url='http://bang.dangdang.com/books/fivestars/'
    html=request_dandan(url)
    pattern = re.compile(r'<div class="paginating".*?(\d+)</a></li><li class="next">',re.S)
    items=re.findall(pattern,html)
    return int(items[0])

if __name__ == "__main__":
    start_time=time.time()

    header=["range","image","title","recommend","author","postive_times","price"]
    with open('output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
    
        # 写入第一行说明
        writer.writerow(header)

    #线程池并发处理
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(main, i+1) for i in range(get_pagination_num())]
        for future in tqdm(concurrent.futures.as_completed(futures),total=len(futures)):
            items = future.result()
            if items:
                    write_item_to_file(items)
    

    # 读取 CSV 文件
    df = pd.read_csv('output.csv')

    # 按 "range" 列进行升序排序
    df.sort_values(by='range', ascending=True).to_csv('output.csv', index=False)
    
    end_time=time.time()
    print("Complete!Cost:{:.2f}秒".format(end_time-start_time))
