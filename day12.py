import requests
import pandas as pd
import time
import random

def day12_multistock_final():
    stock_pool = ["SZ300750", "SH600519", "SH600036", "SZ000001", "SZ000858"]
    all_frames = []
    
    # 💡 老师帮你预处理了 Cookie
    raw_cookie = """cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; remember=1; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwNTYzNjk4MjIsImlzcyI6InVjIiwiZXhwIjoxNzc3NDMxODU5LCJjdG0iOjE3NzQ4Mzk4NTk5NTIsImNpZCI6ImQ5ZDBuNEFadXAifQ.q0cg_5BGqUzYHvfdFwaf_MfbEAtE2_pnSsw9fzMz9CEUfPw0YNoS3MdsXSlJVmcYVw61x4h5nxqA2D64KbiPRH7SGVIvSNjDODomRyuNsbs4ncR52jaZ_yozh5scr9FekZdeaolNW9gSUlR2EM3QhjPtcrIgtlP1Byl-k8dYTICES1_1mWh5KnaB3bwuF8jeojNyX5SSelUUKScsVw1-uxZtpak1fpKyyE-B9djGStMCG6toYnmWN7hU_lOQhoVOPZ7G_y90EvR6RvYG-LAVM3TRu4yqBaV6oprxv5McbAG-AYTIaGc5LaDOc6yKMhvhCbvDzwtsmM8UCxH9RZ1hyw; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; xq_is_login=1; u=1056369822; Hm_lvt_1db88642e346389874251b5a1eded6e3=1775003285,1775092203,1775288740,1775832020; HMACCOUNT=E43A5117E149967B; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1775832069; is_overseas=0; ssxmod_itna=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXN_KiQ_egKDknxT5D/W77eDZDGIdDqx0ErUiexDQSKbiLhp3W4wDqPKy_mDQ6LXhni4mU1LDFe7LkTF6HZcEuYDCPDExGkqCWewDiiWx0rD0eDPxDYDG4Do1YDnZxDjxDdFRgvG_oDbxi3p4GCPI_f64DFs7omUtxD0ZWhOmbI8xDz8OjFQnY4Qn3DeaALsmrvqnj437oD9p4DsODy8OgU1V6Fm9CcHX3bi40k6q0OGzdvOYTIIKSfwAYb3t4H0uYQGbKG57D4nRDK44ByDzA4K_eV_tn44FDi7DwiqHBBYDDWDWmCOxP212kzpSi9keQRPwEtnhtlw=qxQqo4IriMDY/YwOhdK0xQm=KBYxmxwiDD; ssxmod_itna2=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXN_KiQ_egKDknxkeDAKxDIrQ1/jOTPSY0u5iKY_Y=8WxD
"""
    clean_cookie = "".join([c for c in raw_cookie if ord(c) < 128]).replace('\n', '').strip()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': clean_cookie,
        'Referer': 'https://xueqiu.com/',
        'Connection': 'close' # 💡 关键：告诉服务器每次请求完就关闭连接，避免占用过多连接数
    }

    print("🛡️ 稳健采集引擎启动...")

    for symbol in stock_pool:
        # 💡 增加重试逻辑 (Retry Mechanism)
        retry_count = 3
        success = False
        
        while retry_count > 0 and not success:
            try:
                print(f"📡 正在尝试连接 {symbol} (剩余重试次数: {retry_count})...")
                url = f"https://stock.xueqiu.com/v5/stock/history/trade.json?symbol={symbol}&count=50"
                
                # 增加 timeout 防止死等
                resp = requests.get(url, headers=headers, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('data', {}).get('items', [])
                    if items:
                        temp_df = pd.DataFrame(items)
                        temp_df['symbol'] = symbol
                        all_frames.append(temp_df)
                        print(f"✅ {symbol} 捕获成功！")
                        success = True
                else:
                    print(f"⚠️ 服务器返回状态码: {resp.status_code}，正在等待重试...")
            
            except Exception as e:
                print(f"❌ 连接异常: {e}")
            
            if not success:
                retry_count -= 1
                wait = random.uniform(5, 10) # 💡 连接失败时多等会儿
                print(f"💤 休息 {wait:.1f} 秒后重试...")
                time.sleep(wait)

        # 每只股票抓完后，固定休息一下，防止被封 IP
        time.sleep(random.uniform(3, 5))

    # 合并逻辑
    if all_frames:
        master_df = pd.concat(all_frames, ignore_index=True)
        if 'timestamp' in master_df.columns:
            master_df['成交时间'] = pd.to_datetime(master_df['timestamp'], unit='ms')
        
        output_file = "Day12_Final_Master.xlsx"
        master_df.to_excel(output_file, index=False)
        print(f"\n🏆 任务达成！最终面板已生成: {output_file}")
    else:
        print("❌ 最终尝试失败，请检查网络连接或更换 IP 环境。")

if __name__ == "__main__":
    day12_multistock_final()