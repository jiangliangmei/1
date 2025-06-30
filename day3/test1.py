import requests
from bs4 import BeautifulSoup

# 目标网址
url = 'https://movie.douban.com/top250'
# 模拟浏览器请求头
headers = {
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 发送请求获取网页内容
response = requests.get(url, headers=headers)
if response.status_code == 200:
    # 使用BeautifulSoup解析网页
    soup = BeautifulSoup(response.text, 'html.parser')
    # 查找所有电影项，class为item的div标签包含了每部电影的信息
    movies = soup.find_all('div', class_='item')
    movie_info_list = []
    for index, movie in enumerate(movies[:10]):
        title = movie.find('span', class_='title').text
        rating = movie.find('span', class_='rating_num').text
        # 查找导演和主演信息，可能存在部分电影信息不全的情况，需做异常处理
        try:
            director_actor = movie.find('p', class_='').text.strip()
            director = director_actor.split('/')[0].replace('导演:', '').strip()
            actor = director_actor.split('/')[1].replace('主演:', '').strip()
        except IndexError:
            director = ''
            actor = ''
        movie_info = {
            '排名': index + 1,
            '电影名称': title,
            '评分': rating,
            '导演': director,
            '主演': actor
        }
        movie_info_list.append(movie_info)
    for info in movie_info_list:
        print(info)
else:
    print(f"请求失败，状态码：{response.status_code}")