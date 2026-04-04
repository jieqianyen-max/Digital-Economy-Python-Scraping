import requests
import time

# 你的身份门票（用你昨天成功的那个）
headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Cookie': '你的cookie',
    'Referer': 'https://xueqiu.com/'
}

# 监控名单
target_stock = {'SH601318': '中国平安'}
alert_threshold = 0.5  # 设定报警阈值：涨跌幅超过 0.5% 就报警

print("🚀 智能 Agent 已上线，正在进入实时监控模式...")

while True:
    try:
        for code, name in target_stock.items():
            url = f"https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol={code}"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()['data'][0]
                current_price = data['current']
                percent = data['percent']
                
                # 💡 核心：逻辑判断 (Decision Making)
                if abs(percent) >= alert_threshold:
                    print(f"🚩 【报警】{name} 波动剧烈！当前价: {current_price}, 涨幅: {percent}%")
                else:
                    print(f"🟢 {name} 平稳运行中... 当前价: {current_price}, 涨幅: {percent}%")
            
        print("--------------------------------------")
        # 💡 每隔 30 秒扫描一次，防止被封，同时保持实时
        time.sleep(30) 

    except KeyboardInterrupt:
        print("\n🛑 监控已由用户手动停止。")
        break
    except Exception as e:
        print(f"❌ 运行中出现错误: {e}")
        time.sleep(10) # 报错了也歇会，防止死循环轰炸服务器
