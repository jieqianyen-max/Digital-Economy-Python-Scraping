import requests
from bs4 import BeautifulSoup
import pandas as pd  # 导入数据处理神器

# 1. 准备容器（就像准备一个空的 Excel 表格）
data_list = []

# 2. 访问目标
url = "https://quotes.toscrape.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 3. 精准抓取（注意这里的逻辑：先找大盒子，再找小盒子）
# 在这个网页里，每一条名言都装在 class 为 "quote" 的 div 盒子里
quotes_boxes = soup.find_all('div', class_='quote')

for box in quotes_boxes:
    # 在每一个“大盒子”里，分别提取名言和作者
    text = box.find('span', class_='text').get_text()
    author = box.find('small', class_='author').get_text()
    
    # 把这一行数据存进字典
    data_list.append({
        '名言内容': text,
        '作者': author
    })

# 4. 魔法时刻：用 Pandas 导出 Excel
df = pd.DataFrame(data_list)  # 把列表变成表格对象
df.to_excel('我的第一个数据资产.xlsx', index=False) # 导出到文件

print("🎉 恭喜！数据已成功导出到 Excel 文件，请查看你的文件夹！")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time # 导入时间库，做一个“绅士”的爬虫

all_data = []

# 自动爬取 1 到 3 页
for page in range(1, 4):
    print(f"正在开采第 {page} 页的数据...")
    url = f"https://quotes.toscrape.com/page/{page}/"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_boxes = soup.find_all('div', class_='quote')

    for box in quotes_boxes:
        text = box.find('span', class_='text').get_text()
        author = box.find('small', class_='author').get_text()
        all_data.append({'内容': text, '作者': author, '页码': page})
    
    # 港大标准：每爬一页歇 1 秒。防止动作太快被服务器封 IP，这叫“爬虫的自我修养”
    time.sleep(1)

# 导出最终大表
df = pd.DataFrame(all_data)
df.to_excel('三页名言汇总.xlsx', index=False)
print("✅ 三页数据已全部打包完毕！")