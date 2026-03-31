import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 目标设定 (Targeting)
# 我们使用专门的爬虫练习网站，确保 100% 成功率
url = "https://quotes.toscrape.com/"

# 2. 身份伪装 (User-Agent)
# 模拟真实浏览器的“身份证”，防止被识别为机器人
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"正在建立连接: {url} ...")

try:
    # 3. 发送请求 (Request)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8' # 确保中文（如果有）不乱码

    # 4. 解析网页 (Parsing)
    # BeautifulSoup 将混乱的 HTML 源码变成一棵“DOM 树”
    soup = BeautifulSoup(response.text, 'html.parser')

    # 5. 提取数据 (Extraction)
    # 逻辑：先找所有 class 为 'quote' 的大盒子
    quotes = soup.find_all('div', class_='quote')

    results = []
    for item in quotes:
        # 在大盒子里精准定位名言内容和作者
        text = item.find('span', class_='text').get_text()
        author = item.find('small', class_='author').get_text()
        
        results.append({
            '名言': text,
            '作者': author
        })
        print(f"成功捕获 -> 作者: {author}")

    # 6. 数据资产化 (Data Assetization)
    # 使用 Pandas 将结果转化为 DataFrame 矩阵并导出 Excel
    df = pd.DataFrame(results)
    df.to_excel('基础数据资产_名言篇.xlsx', index=False)
    
    print("\n🎉 重跑成功！")
    print(f"✅ 共采集 {len(results)} 条数据")
    print("✅ 已生成文件: 基础数据资产_名言篇.xlsx")

except Exception as e:
    print(f"❌ 运行出错了，错误原因: {e}")