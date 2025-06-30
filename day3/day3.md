
# 学习日志：2025年6月30日  


## 一、学习内容概述  
今日主要学习了 Python 在数据处理、网络爬虫及数据分析可视化中的实际应用，涉及文件操作、数据清洗、网页爬取及可视化图表绘制等核心技能。通过实战代码练习，掌握了处理不同场景下数据问题的方法，并解决了多个技术报错。  


## 二、核心学习模块与代码实践  


### 1. 数据处理与文件操作  
#### CSV 文件合并与分析  
练习了多文件合并、缺省值处理、分组聚合及统计计算，例如合并三年城市数据并计算 GDP 年均增长率：  
```python
# 合并多份城市数据并计算GDP增长率
file_paths = [r"E:\2015年国内主要城市年度数据.csv", ...]
dfs = []
for path in file_paths:
    df = pd.read_csv(path)
    df["年份"] = int(path.split("年")[0])
    dfs.append(df)
merged_df = pd.concat(dfs)

# 计算GDP年均增长率
pivot_df = merged_df.pivot_table(index="城市", columns="年份", values="GDP")
pivot_df["年均增长率(%)"] = ((pivot_df[2017] / pivot_df[2015]) ** 0.5 - 1) * 100
```  
**关键点**：使用 `pivot_table` 重构数据结构，通过数学公式计算复合增长率，处理了缺失值和异常数据。  

#### 文件编码与路径问题解决  
针对 Linux/Windows 路径差异及编码错误，学习了动态适配路径分隔符、编码检测及异常处理：  
```python
# 自动检测文件编码
def get_file_encoding(path):
    with open(path, 'rb') as f:
        return chardet.detect(f.read(100000))['encoding']

# 适配不同系统路径（自动适配 \ 或 /）
file_path = os.path.join('data', 'file.csv')
```  


### 2. 网络爬虫实践  
#### 豆瓣电影 Top 250 数据抓取  
练习了基础爬虫开发，包括请求头设置、HTML 解析及数据提取：  
```python
url = 'https://movie.douban.com/top250'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
movies = soup.find_all('div', class_='item')

# 注意：添加随机延迟避免被封IP
time.sleep(random.uniform(1, 3))
```  

#### 51job 职位信息爬取与图片下载  
结合 `requests` 和 `lxml` 解析网页，下载职位相关图片：  
```python
def parse_images(html_content):
    tree = html.fromstring(html_content)
    img_urls = tree.xpath('//img/@src | //img/@data-src')
    return [url for url in img_urls if url and not url.startswith('data:image')]
```  

#### CNKI 文献爬虫（Selenium 版本）  
使用 Selenium 模拟浏览器行为，处理动态加载页面和验证码：  
```python
# 配置ChromeDriver并模拟人类操作
driver = webdriver.Chrome(...)
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua.random})

# 模拟滚动页面
def human_like_scroll():
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(random.randint(3, 6)):
        driver.execute_script(f"window.scrollTo(0, {random.randint(300, 800)})")
        time.sleep(random.uniform(0.5, 1.5))
```  


### 3. 数据可视化  
#### 销量趋势图绘制  
使用 Matplotlib 绘制时间序列图表，处理 x 轴标签显示问题：  
```python
# 生成日期与销量数据
date = np.array(['2000/1/1', '2000/2/15', ...])
sales = np.random.randint(500, 2000, 20)

# 绘制图表
plt.xticks(range(0, len(date), 2), date[::2], rotation=45, color='red')
plt.plot(date, sales)
```  


## 三、遇到的问题与解决方案  
1. **文件路径与编码错误**  
   - **问题**：Windows 路径 `E:\file.csv` 在 Linux 环境报错 `FileNotFoundError`。  
   - **解决**：使用 `os.path.join` 动态适配路径分隔符，或手动修改为 Linux 路径 `/home/user/data/file.csv`。  

2. **编码异常 `Cannot convert numpy.ndarray to numpy.ndarray`**  
   - **问题**：CSV 文件编码不匹配导致数据类型转换失败。  
   - **解决**：使用 `chardet` 自动检测编码，优先尝试 `utf-8-sig`、`gb18030` 等编码，添加 `on_bad_lines='skip'` 跳过异常行。  

3. **语法错误 `SyntaxError: invalid syntax`**  
   - **问题**：代码中出现嵌套列表定义（如 `file_paths = [file_paths = [...]]`）。  
   - **解决**：检查并修正语法，确保列表定义无嵌套赋值。  


## 四、学习收获与总结  
1. **数据处理能力提升**：熟练掌握 Pandas 数据合并、分组聚合及透视表操作，能处理跨年度数据的统计分析。  
2. **爬虫实战经验**：了解不同网站的反爬机制，掌握 `requests` 与 Selenium 结合的爬虫策略，学会处理动态页面和验证码。  
3. **问题调试思路**：  
   - 打印错误堆栈定位问题位置；  
   - 分段测试代码（如先读取文件再处理数据）；  
   - 使用工具（如 `chardet`）检测文件编码，手动验证路径有效性。  
4. **跨平台开发意识**：编写代码时需考虑操作系统差异，使用 `os` 模块适配路径和环境变量。  


## 五、明日学习计划  
1. 深入学习 Pandas 高级数据处理（如时间序列、数据透视表高级功能）。  
2. 练习 Scrapy 框架开发复杂爬虫，实现增量爬取和数据持久化。  
3. 学习 Seaborn 数据可视化，绘制更专业的统计图表。  


可直接将上述内容复制到.md文件中，Markdown格式会自动渲染标题层级、代码块高亮及列表结构，适合文档存储和分享。