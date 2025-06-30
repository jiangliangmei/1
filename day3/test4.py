import requests
from bs4 import BeautifulSoup
import time
import random
import re
import os
import logging
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import DownloadManager
from webdriver_manager.core.os_manager import ChromeType
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CNKISpider:
    def __init__(self):
        # 初始化随机User-Agent
        self.ua = UserAgent()

        # 配置WebDriverManager使用国内镜像（关键修改）
        os.environ["WDM_SERVER_URL"] = "https://npm.taobao.org/mirrors/chromedriver"

        # 配置Chrome浏览器
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

        # 初始化浏览器驱动（添加chrome_type参数）
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()),
            options=self.chrome_options
        )
        self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": self.ua.random
        })

        # 基础URL
        self.base_url = "https://www.cnki.net"

        # 存储已访问的URL
        self.visited_urls = set()




    def random_sleep(self, min_sec=3, max_sec=8):
        """随机延迟，模拟人类浏览行为"""
        sleep_time = random.uniform(min_sec, max_sec)
        logger.info(f"休眠 {sleep_time:.2f} 秒")
        time.sleep(sleep_time)

    def human_like_scroll(self):
        """模拟人类滚动页面行为"""
        scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        scroll_steps = random.randint(3, 6)

        for _ in range(scroll_steps):
            step = random.randint(300, 800)
            current_position += step
            if current_position > scroll_height:
                current_position = scroll_height

            self.driver.execute_script(f"window.scrollTo(0, {current_position})")
            self.random_sleep(0.5, 1.5)

        # 滚动回顶部
        self.random_sleep(1, 3)
        self.driver.execute_script("window.scrollTo(0, 0)")

    def search(self, keyword, page=1):
        """搜索文献"""
        encoded_keyword = requests.utils.quote(keyword)
        search_url = f"{self.base_url}/kns8/defaultresult/index?dbcode=CJFD&sfield=title&skey={encoded_keyword}&page={page}"

        try:
            logger.info(f"搜索关键词: {keyword}, 第 {page} 页")
            self.driver.get(search_url)
            self.random_sleep(5, 10)  # 首次加载延迟

            # 检查是否有验证码
            if "验证码" in self.driver.page_source:
                logger.warning("触发了验证码，请手动处理")
                input("请在浏览器中完成验证码，然后按Enter继续...")
                self.random_sleep(3, 5)

            # 等待搜索结果加载
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".list-item"))
            )

            # 模拟人类浏览行为
            self.human_like_scroll()

            return self._parse_search_results()
        except TimeoutException:
            logger.error("搜索结果加载超时")
            return []
        except WebDriverException as e:
            logger.error(f"搜索过程中发生错误: {e}")
            return []

    def _parse_search_results(self):
        """解析搜索结果页面"""
        results = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:
            items = soup.select(".list-item")
            for item in items:
                # 提取标题和链接
                title_elem = item.select_one(".title a")
                if not title_elem:
                    continue

                title = title_elem.text.strip()
                href = title_elem.get("href", "")

                # 处理相对URL
                if href.startswith("/"):
                    url = self.base_url + href
                else:
                    url = href

                # 提取作者
                author_elem = item.select_one(".author")
                authors = author_elem.text.strip() if author_elem else ""

                # 提取来源和发表时间
                source_elem = item.select_one(".source")
                source_info = source_elem.text.strip() if source_elem else ""

                # 提取被引次数
                cite_elem = item.select_one(".data-cita")
                cite_count = re.search(r"被引\s*(\d+)", cite_elem.text) if cite_elem else None
                cite_count = int(cite_count.group(1)) if cite_count else 0

                results.append({
                    'title': title,
                    'url': url,
                    'authors': authors,
                    'source_info': source_info,
                    'cite_count': cite_count
                })

            logger.info(f"解析出 {len(results)} 篇文献")
            return results
        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")
            return []

    def get_document_details(self, doc_url, doc_title):
        """获取文献详情"""
        if not doc_url or doc_url in self.visited_urls:
            return None

        self.visited_urls.add(doc_url)

        try:
            logger.info(f"访问文献详情: {doc_title}")
            self.driver.get(doc_url)
            self.random_sleep(6, 12)  # 模拟阅读时间

            # 检查是否有验证码
            if "验证码" in self.driver.page_source:
                logger.warning("触发了验证码，请手动处理")
                input("请在浏览器中完成验证码，然后按Enter继续...")
                self.random_sleep(3, 5)

            # 等待页面加载
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".doc-top"))
            )

            # 模拟人类浏览行为
            self.human_like_scroll()

            return self._parse_document_details()
        except TimeoutException:
            logger.error("文献详情加载超时")
            return None
        except WebDriverException as e:
            logger.error(f"访问文献详情时发生错误: {e}")
            return None

    def _parse_document_details(self):
        """解析文献详情页面"""
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:
            # 提取摘要
            abstract_elem = soup.select_one(".abstract-text")
            abstract = abstract_elem.text.strip() if abstract_elem else "摘要未找到"

            # 提取关键词
            keywords = []
            keyword_elems = soup.select(".keywords a")
            for keyword in keyword_elems:
                keywords.append(keyword.text.strip())

            # 提取作者信息
            authors = []
            author_elems = soup.select(".author-text a")
            for author in author_elems:
                authors.append({
                    'name': author.text.strip(),
                    'affiliation': author.get("title", "")
                })

            # 提取基金信息
            fund_elems = soup.select(".funds a")
            funds = [fund.text.strip() for fund in fund_elems]

            # 提取参考文献
            references = []
            ref_elems = soup.select(".reference-item")
            for ref in ref_elems:
                ref_text = ref.text.strip()
                if ref_text:
                    references.append(ref_text)

            # 提取DOI
            doi_elem = soup.select_one(".doi .value")
            doi = doi_elem.text.strip() if doi_elem else ""

            return {
                'abstract': abstract,
                'keywords': keywords,
                'authors': authors,
                'funds': funds,
                'references': references,
                'doi': doi
            }
        except Exception as e:
            logger.error(f"解析文献详情失败: {e}")
            return None

    def format_to_text(self, search_result, details=None):
        """将文献信息格式化为易读文本"""
        if not search_result:
            return ""

        text = f"标题: {search_result['title']}\n"
        text += f"作者: {search_result['authors']}\n"
        text += f"来源: {search_result['source_info']}\n"
        text += f"被引次数: {search_result['cite_count']}\n\n"

        if details:
            text += f"摘要: {details['abstract']}\n\n"
            text += f"关键词: {', '.join(details['keywords'])}\n\n"

            if details['authors']:
                text += "作者详情:\n"
                for author in details['authors']:
                    text += f"- {author['name']} ({author['affiliation']})\n"
                text += "\n"

            if details['funds']:
                text += f"基金支持: {', '.join(details['funds'])}\n\n"

            if details['doi']:
                text += f"DOI: {details['doi']}\n\n"

            if details['references']:
                text += "参考文献:\n"
                for i, ref in enumerate(details['references'], 1):
                    text += f"[{i}] {ref}\n"
                text += "\n"

        text += "=" * 80 + "\n\n"
        return text

    def save_text(self, text, filename='cnki_results.txt'):
        """保存文本内容到文件"""
        if not text:
            return

        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(text)
            logger.info(f"已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存文件失败: {e}")

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")

    def run(self, keyword, max_pages=3):
        """运行爬虫"""
        output_file = f"{keyword.replace(' ', '_')}_cnki_results.txt"
        if os.path.exists(output_file):
            os.remove(output_file)

        try:
            for page in range(1, max_pages + 1):
                # 搜索文献
                results = self.search(keyword, page)

                if not results:
                    logger.warning(f"第 {page} 页没有搜索结果")
                    continue

                # 随机打乱处理顺序
                random.shuffle(results)

                for result in results:
                    # 获取文献详情
                    details = self.get_document_details(result['url'], result['title'])

                    # 格式化并保存
                    text = self.format_to_text(result, details)
                    self.save_text(text, output_file)

                    # 随机延迟，模拟阅读行为
                    self.random_sleep(8, 15)

                # 页面间延迟
                self.random_sleep(15, 25)

        finally:
            self.close()


if __name__ == "__main__":
    spider = CNKISpider()
    spider.run("人工智能", max_pages=2)