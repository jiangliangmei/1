import requests
from lxml import html
import os
from urllib.parse import urljoin
import time

# 目标URL（广州Java岗位）
TARGET_URL = "https://we.51job.com/pc/search?jobArea=090200&keyword=java&searchType=2&sortType=0&metro="

# 请求头（模拟浏览器访问）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://www.51job.com/"
}

# 创建存储目录
OUTPUT_DIR = "job_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_page(url):
    """获取网页内容"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"请求失败：{str(e)}")
        return None


def parse_images(html_content):
    """解析页面中的图片"""
    tree = html.fromstring(html_content)
    img_urls = []

    # 根据实际页面结构调整XPath（示例为通用选择器）
    # 常见图片位置：
    # 1. 公司LOGO：//img[contains(@class, 'com_logo')]
    # 2. 广告图片：//img[contains(@class, 'ad_img')]
    # 3. 职位卡片图片：//div[@class="job_card"]//img

    # 示例选择器（需根据实际页面调整）：
    for img in tree.xpath('//img'):
        src = img.get('src') or img.get('data-src')  # 处理懒加载图片
        if src and not src.startswith('data:image'):  # 过滤base64编码图片
            img_urls.append(src)

    return list(set(img_urls))  # 去重


def download_image(url, save_path):
    """下载单张图片"""
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"下载失败 {url}: {str(e)}")
        return False


def main():
    # 获取页面内容
    print("正在获取页面内容...")
    html_content = fetch_page(TARGET_URL)
    if not html_content:
        return

    # 解析图片URL
    print("正在解析图片地址...")
    img_urls = parse_images(html_content)
    print(f"发现{len(img_urls)}张图片")

    # 下载图片
    for idx, img_url in enumerate(img_urls):
        # 生成绝对URL
        abs_url = urljoin(TARGET_URL, img_url)

        # 生成唯一文件名
        filename = f"{OUTPUT_DIR}/{idx + 1}_{abs_url.split('/')[-1]}"

        print(f"正在下载 {idx + 1}/{len(img_urls)}: {abs_url}")
        if download_image(abs_url, filename):
            print(f"保存成功：{filename}")
        else:
            print(f"保存失败：{filename}")

        # 添加延迟避免被封禁
        time.sleep(1)


if __name__ == "__main__":
    main()