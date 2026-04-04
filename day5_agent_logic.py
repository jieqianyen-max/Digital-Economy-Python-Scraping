import requests
import time

# 你的身份门票（用你昨天成功的那个）
headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Cookie': 'cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; remember=1; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwNTYzNjk4MjIsImlzcyI6InVjIiwiZXhwIjoxNzc3NDMxODU5LCJjdG0iOjE3NzQ4Mzk4NTk5NTIsImNpZCI6ImQ5ZDBuNEFadXAifQ.q0cg_5BGqUzYHvfdFwaf_MfbEAtE2_pnSsw9fzMz9CEUfPw0YNoS3MdsXSlJVmcYVw61x4h5nxqA2D64KbiPRH7SGVIvSNjDODomRyuNsbs4ncR52jaZ_yozh5scr9FekZdeaolNW9gSUlR2EM3QhjPtcrIgtlP1Byl-k8dYTICES1_1mWh5KnaB3bwuF8jeojNyX5SSelUUKScsVw1-uxZtpak1fpKyyE-B9djGStMCG6toYnmWN7hU_lOQhoVOPZ7G_y90EvR6RvYG-LAVM3TRu4yqBaV6oprxv5McbAG-AYTIaGc5LaDOc6yKMhvhCbvDzwtsmM8UCxH9RZ1hyw; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; xq_is_login=1; u=1056369822; Hm_lvt_1db88642e346389874251b5a1eded6e3=1774839765,1774877787,1775003285,1775092203; HMACCOUNT=E43A5117E149967B; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1775092892; ssxmod_itna=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDGhxIhXxDjhvtPSD0v4qwDA5DnCx7YDt=RP_YKaQmDNqQajeKxKYaDkkb40B2/Fbqob//1SY07MIl8XS6TvrDB3DbqDyKDIr_7eD4f3Dt4DIDAYDDxDWDYEqxGUNDG=D7gRtx=nQxi3Db2WDmL0WFcaD0SwdwlcoDDtA3QwWnm5D0wvwZ2re70aDYf0HVYqN5AOPWBbDjdPD/RDUggbzM/kz36gfXIcm_eGy85Gu4PytuiK=NaWF5r2mWCewAIr7GpQDN0De0q_GD/=D59phBPU0qejDqexKnYm0PDt4DDa5=_rF0iKhM_ylQchj5w0R7jT1fqV8TrQ0i_GOentQGND_4Brr70D10iiikQ0_4AiPD; ssxmod_itna2=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDGhxIhXxDjhvtPwDDcYwQ5Zn7W1SYnM5qPl3R0EnA4D',
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