import requests
import pandas as pd

# 1. 目标 URL (昨天找出来的金矿)
url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH601318,sz000001,"

# 2. 伪装请求头 (这是你的“特工装备”)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # ⚠️ 把下面引号里的内容换成你刚才在浏览器里复制的那一长串 Cookie
    'Cookie': 'cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; remember=1; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwNTYzNjk4MjIsImlzcyI6InVjIiwiZXhwIjoxNzc3NDMxODU5LCJjdG0iOjE3NzQ4Mzk4NTk5NTIsImNpZCI6ImQ5ZDBuNEFadXAifQ.q0cg_5BGqUzYHvfdFwaf_MfbEAtE2_pnSsw9fzMz9CEUfPw0YNoS3MdsXSlJVmcYVw61x4h5nxqA2D64KbiPRH7SGVIvSNjDODomRyuNsbs4ncR52jaZ_yozh5scr9FekZdeaolNW9gSUlR2EM3QhjPtcrIgtlP1Byl-k8dYTICES1_1mWh5KnaB3bwuF8jeojNyX5SSelUUKScsVw1-uxZtpak1fpKyyE-B9djGStMCG6toYnmWN7hU_lOQhoVOPZ7G_y90EvR6RvYG-LAVM3TRu4yqBaV6oprxv5McbAG-AYTIaGc5LaDOc6yKMhvhCbvDzwtsmM8UCxH9RZ1hyw; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; xq_is_login=1; u=1056369822; is_overseas=0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1774839765,1774877787,1775003285; HMACCOUNT=E43A5117E149967B; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1775003291; ssxmod_itna=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDGhs7G47K7er5Q1DBThhrDnqD8UDQeDvKg4rezSD7qxzK7f7oQ4QWCCkb40B2/Fbqob//60Y07MUlSXS6TvrDB3DbqDyKDowDYAfDBYD74G_DDeDixGmteDS/DD9DGp3ynuNXeDEDYPbxiU4ToaFxDLNfl2FvDDBGf0QbxTzDDNslhxKrGxFxGA4kZwQBCGpaih3x0UWDBdqnIv3c1MUgOnpvU8aTSrDzk1DtMTkyQqO0jWia1ePTb2rB4Kw7GpemY0DelwUGDZxmGnP54K10qejDqWiwmKUG2rDDAlv5gR4SRY7yM_5EteZKhrCxOjT1fw/8TH4TH_0OentQGND_4KDqDRYY4qb7kQDb/5qKhDD; ssxmod_itna2=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDGhs7G47K7er5jrDG8eXrQ1/jOTPSYnMH0xQDK6dNxD'
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