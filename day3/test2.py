import requests
from lxml import html

import time


url = "https://we.51job.com/pc/search?jobArea=090200&keyword=java&searchType=2&sortType=0&metro="
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.51job.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

response = requests.get(url, headers=headers)
print(f"状态码: {response.status_code}")
print(f"响应内容长度: {len(response.content)}")

# 保存HTML用于调试
with open('51job.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("已保存网页内容到51job.html，请用浏览器打开分析")

# 确保响应正常再解析
if response.status_code == 200 and len(response.content) > 1000:
    tree = html.fromstring(response.content)

    # 使用更灵活的XPath选择器
    job_items = tree.xpath('//div[contains(@class, "job-item") or contains(@class, "list")]')

    if not job_items:
        print("警告：未匹配到职位列表项，请检查XPath")
        # 提供备选选择器
        job_items = tree.xpath('//div[contains(@class, "result")]//div[contains(@class, "item")]')
        if not job_items:
            print("所有备选选择器均失败，请手动分析51job.html")
        else:
            print("使用备选选择器成功匹配到职位项")
    else:
        print(f"成功匹配到 {len(job_items)} 个职位项")

    for item in job_items:
        try:
            # 根据实际HTML结构调整XPath
            job_title = item.xpath('.//h3[contains(@class, "job-name")]/text()')
            job_title = job_title[0].strip() if job_title else "未找到职位名称"

            company_name = item.xpath('.//div[contains(@class, "company")]//a/text()')
            company_name = company_name[0].strip() if company_name else "未找到公司名称"

            location = item.xpath('.//span[contains(@class, "location")]/text()')
            location = location[0].strip() if location else "未找到工作地点"

            salary = item.xpath('.//span[contains(@class, "salary")]/text()')
            salary = salary[0].strip() if salary else "未找到薪资"

            print(f"职位名称：{job_title}, 公司名称：{company_name}, 工作地点：{location}, 薪资：{salary}")
        except Exception as e:
            print(f"解析职位时出错: {e}")
else:
    print("错误：未获取到有效响应，请检查网络或反爬机制")