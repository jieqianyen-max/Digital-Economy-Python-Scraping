import requests
import pandas as pd
import time

def fetch_real_trade_data(symbol, count=50):
    api_url = f"https://stock.xueqiu.com/v5/stock/history/trade.json?symbol={symbol}&count={count}"
    
    # 💡 这里的 Cookie 我帮你做了一次强力编码修正
    # 请确保把你浏览器里最新的 Cookie 替换到引号内，且不要带任何多余的空格或换行
    raw_cookie = """cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; u=1056369822"""
    
    # 💡 核心修复：强制去除所有非 ASCII 字符，防止 latin-1 报错
    clean_cookie = "".join([c for c in raw_cookie if ord(c) < 128]).strip()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': clean_cookie,
        'Referer': f'https://xueqiu.com/S/{symbol}'
    }

    try:
        print(f"🚀 正在尝试第二次实战同步...")
        # 💡 增加 verify=False 排除证书干扰（有时网络代理会引起问题）
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # 打印状态码，确认是否成功连接
        print(f"📡 服务器响应状态: {response.status_code}")
        
        data = response.json()
        items = data.get('data', {}).get('items', [])
        
        if items:
            df = pd.DataFrame(items)
            
            # 💡 格式化时间
            if 'timestamp' in df.columns:
                df['成交时间'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # 💡 换个名字存，防止 Excel 占用
            output_file = f"Result_{symbol}_{int(time.time())}.xlsx"
            df.to_excel(output_file, index=False)
            
            print(f"✅ 终于抓到了！数据量：{len(items)} 条")
            print(f"📂 请查看新生成的文件: {output_file}")
            print("-" * 30)
            print(df.head())
        else:
            print("⚠️ 抓取成功但数据项为空。")
            print(f"🔍 接口返回信息: {data.get('error_description', '无详细错误')}")

    except Exception as e:
        print(f"❌ 运行依然报错: {e}")

if __name__ == "__main__":
    fetch_real_trade_data("SZ300750", count=50)