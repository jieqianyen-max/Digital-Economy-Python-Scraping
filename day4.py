import requests
import pandas as pd
import time

# 1. 监控名单（使用字典：代码作为 Key，中文名作为 Value）
stock_pool = {
    'SH601318': '中国平安',
    'SZ000001': '平安银行',
    'SH600519': '贵州茅台',
    'SZ000858': '五粮液',
    'SH600009': '上海机场'
}
all_results = []

# 2. 身份门票与深度伪装
# 请确保从浏览器复制的最新的 Cookie 填入此处
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; remember=1; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwNTYzNjk4MjIsImlzcyI6InVjIiwiZXhwIjoxNzc3NDMxODU5LCJjdG0iOjE3NzQ4Mzk4NTk5NTIsImNpZCI6ImQ5ZDBuNEFadXAifQ.q0cg_5BGqUzYHvfdFwaf_MfbEAtE2_pnSsw9fzMz9CEUfPw0YNoS3MdsXSlJVmcYVw61x4h5nxqA2D64KbiPRH7SGVIvSNjDODomRyuNsbs4ncR52jaZ_yozh5scr9FekZdeaolNW9gSUlR2EM3QhjPtcrIgtlP1Byl-k8dYTICES1_1mWh5KnaB3bwuF8jeojNyX5SSelUUKScsVw1-uxZtpak1fpKyyE-B9djGStMCG6toYnmWN7hU_lOQhoVOPZ7G_y90EvR6RvYG-LAVM3TRu4yqBaV6oprxv5McbAG-AYTIaGc5LaDOc6yKMhvhCbvDzwtsmM8UCxH9RZ1hyw; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; xq_is_login=1; u=1056369822; Hm_lvt_1db88642e346389874251b5a1eded6e3=1774839765,1774877787,1775003285,1775092203; HMACCOUNT=E43A5117E149967B; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1775092892; ssxmod_itna=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDGhxIhXxDjhvtPSD0v4qwDA5DnCx7YDt=RP_YKaQmDNqQajeKxKYaDkkb40B2/Fbqob//1SY07MIl8XS6TvrDB3DbqDyKDIr_7eD4f3Dt4DIDAYDDxDWDYEqxGUNDG=D7gRtx=nQxi3Db2WDmL0WFcaD0SwdwlcoDDtA3QwWnm5D0wvwZ2re70aDYf0HVYqN5AOPWBbDjdPD/RDUggbzM/kz36gfXIcm_eGy85Gu4PytuiK=NaWF5r2mWCewAIr7GpQDN0De0q_GD/=D59phBPU0qejDqexKnYm0PDt4DDa5=_rF0iKhM_ylQchj5w0R7jT1fqV8TrQ0i_GOentQGND_4Brr70D10iiikQ0_4AiPD; ssxmod_itna2=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDGhxIhXxDjhvtPwDDcYwQ5Zn7W1SYnM5qPl3R0EnA4D',
    'Referer': 'https://xueqiu.com/',
    'Host': 'stock.xueqiu.com',
    'Accept': 'application/json, text/plain, */*'
}

print("🕵️ 工业级监控中心启动，身份验证已加载...")

# 3. 循环扫描全场数据
# 💡 关键点：使用 .items() 同时获取代码(code)和名称(name)
for code, name in stock_pool.items():
    try:
        # 修正后的标准行情接口 URL
        url = f"https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol={code}"
        
        # 发送请求，设置 10 秒超时防止程序卡死
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            res_json = response.json()
            
            # 检查接口是否真的返回了数据
            if 'data' in res_json and res_json['data']:
                stock_data = res_json['data'][0]
                
                # 构造结构化字典
                info = {
                    '代码': code,
                    '名称': name,  # 💡 核心修复：直接使用字典里的中文名
                    '当前价': stock_data.get('current', 0),
                    '涨跌幅': stock_data.get('percent', 0),
                    '更新时间': time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                all_results.append(info)
                print(f"✅ 成功捕获: {name} ({code}) | 价格: {info['当前价']} | 涨幅: {info['涨跌幅']}%")
            else:
                print(f"⚠️ {name} ({code}) 接口返回数据为空，请检查 Cookie。")
        else:
            print(f"❌ {name} 访问失败，状态码: {response.status_code}")

        # 频率控制：每抓一个歇 1.5 秒，模拟真人行为
        time.sleep(1.5)

    except Exception as e:
        print(f"❌ 抓取 {code} 时发生异常: {e}")
        continue

# 4. 结果固化与导出
if all_results:
    df = pd.DataFrame(all_results)
    # 按照抓取顺序保存到 Excel
    df.to_excel('Day4_全平台监控资产_完美版.xlsx', index=False)
    print(f"\n📊 任务圆满完成！共采集 {len(all_results)} 条数据。")
    print("📂 文件已生成: Day4_全平台监控资产_完美版.xlsx")
else:
    print("\n😱 警告：未能采集到任何有效数据，请检查网络或 Cookie！")