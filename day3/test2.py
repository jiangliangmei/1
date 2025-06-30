import requests
from lxml import html

url = "https://we.51job.com/pc/search?jobArea=090200&keyword=java&searchType=2&sortType=0&metro="
response = requests.get(url)
tree = html.fromstring(response.content)

# 定位到职位列表项
job_items = tree.xpath('//div[@class="info"]')  # 假设职位列表项的类名为'info'

for item in job_items:
    # 提取职位名称、公司名称、工作地点、薪资等信息
    job_title = item.xpath('.//span[@class="job-title"]/text()')[0]
    company_name = item.xpath('.//a[@class="company-name"]/text()')[0]
    location = item.xpath('.//span[@class="location"]/text()')[0]
    salary = item.xpath('.//span[@class="salary"]/text()')[0]

    # 打印或保存提取的信息
    print(f"职位名称：{job_title}, 公司名称：{company_name}, 工作地点：{location}, 薪资：{salary}")