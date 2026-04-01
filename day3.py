import requests
import pandas as pd

# 1. 目标 URL (昨天找出来的金矿)
url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH601318,sz000001,"

# 2. 伪装请求头 (这是你的“特工装备”)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # ⚠️ 把下面引号里的内容换成你刚才在浏览器里复制的那一长串 Cookie
    'Cookie': 'YOUR_COOKIE_HERE'
}

print("🚀 正在伪装身份请求数据...")

# 3. 发送带“门票”的请求
response = requests.get(url, headers=headers)

# 4. 处理 JSON 数据 (不再需要 BeautifulSoup，直接解析字典)
data_json = response.json() 

# 5. 提取核心数字 (像剥洋葱一样)
# 观察昨天 Preview 里的层级：data -> [0] -> current
stock_info = data_json['data'][0]

print(f"📈 股票名称: {stock_info['symbol']}")
print(f"💰 当前价格: {stock_info['current']}")
print(f"📊 成交量: {stock_info['volume']}")

# 6. 存入 Excel (资产化)
df = pd.DataFrame([stock_info])
df.to_excel('Day3_带权访问资产.xlsx', index=False)
print("\n✅ 身份验证通过，数据已安全落地！")
