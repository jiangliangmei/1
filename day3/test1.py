import requests
from bs4 import BeautifulSoup
import time
import random

url = 'https://movie.douban.com/top250'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Referer': 'https://movie.douban.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find_all('div', class_='item')
    movie_info_list = []

    for index, movie in enumerate(movies[:10]):
        title = movie.find('span', class_='title').text
        rating = movie.find('span', class_='rating_num').text

        try:
            bd = movie.find('div', class_='bd').text.strip()
            director = bd.split('\n')[1].strip().split(' ')[0].replace('导演:', '').strip()
            actor = bd.split('\n')[1].strip().split(' ')[1].replace('主演:', '').strip()
        except (IndexError, AttributeError):
            director, actor = '', ''

        movie_info = {
            '排名': index + 1,
            '电影名称': title,
            '评分': rating,
            '导演': director,
            '主演': actor
        }
        movie_info_list.append(movie_info)
        time.sleep(random.uniform(1, 3))  # 添加延迟

    for info in movie_info_list:
        print(info)
else:
    print(f"请求失败，状态码：{response.status_code}")
    print("响应内容:", response.text)  # 打印详细错误信息