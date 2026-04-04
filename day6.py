import requests
import time

# 💡 老师为你准备的“终极兼容版”headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # 💡 使用三个单引号，这样无论 Cookie 有多长、有没有换行，都不会报错了
    'Cookie': '''cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; remember=1; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwNTYzNjk4MjIsImlzcyI6InVjIiwiZXhwIjoxNzc3NDMxODU5LCJjdG0iOjE3NzQ4Mzk4NTk5NTIsImNpZCI6ImQ5ZDBuNEFadXAifQ.q0cg_5BGqUzYHvfdFwaf_MfbEAtE2_pnSsw9fzMz9CEUfPw0YNoS3MdsXSlJVmcYVw61x4h5nxqA2D64KbiPRH7SGVIvSNjDODomRyuNsbs4ncR52jaZ_yozh5scr9FekZdeaolNW9gSUlR2EM3QhjPtcrIgtlP1Byl-k8dYTICES1_1mWh5KnaB3bwuF8jeojNyX5SSelUUKScsVw1-uxZtpak1fpKyyE-B9djGStMCG6toYnmWN7hU_lOQhoVOPZ7G_y90EvR6RvYG-LAVM3TRu4yqBaV6oprxv5McbAG-AYTIaGc5LaDOc6yKMhvhCbvDzwtsmM8UCxH9RZ1hyw; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; xq_is_login=1; u=1056369822; Hm_lvt_1db88642e346389874251b5a1eded6e3=1774877787,1775003285,1775092203,1775288740; HMACCOUNT=E43A5117E149967B; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1775288911; ssxmod_itna=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDw_7iDDKeDjhGt7SD0v4qwDA5DnCx7YDt=RP_YxcOQAhI374wDqPYgfmDjGLXEni4pU1LA5jc6oL97/SwG0YDCPDExGkqmWewDiiFx0rD0eDPxDYDG4Do1YDnZxDjxDdFRgvG_oDbxi3p4GCPI_f64DFs7omUtxD0PahOmbIxxDzxOCiQnY4Qn3DeaALsmrvqnj437oD9p4DsODyxOgU1V1im9CcHXfbi40k6q0OGzdvOYTIIKSfwAAb3tbHS2YQDTKG5DbiKDrenD8Axo4eoiHW0iFGx/xwiuexBYDDWCjd1OxeOeUdzuLW5RzwGrU7QchtnhsjhYGhYr0QSi5eG5/DY=YYmnDt7hj2DooGQ7e4D; ssxmod_itna2=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNDw_7iDDKeDjhGt7wDDcAGw8/efTv3nrGvNG=4bWfyG4D''',
    'Referer': 'https://xueqiu.com/',
    'Accept': 'application/json, text/plain, */*'
}

# 目标：中国平安的评论区接口
comment_url = "https://stock.xueqiu.com/v5/stock/quote.json?symbol=SH601988&extend=detail"

def get_market_sentiment():
    print("🚀 正在发起请求...")
    try:
        # 增加 timeout 防止网络卡死
        response = requests.get(comment_url, headers=headers, timeout=10)
        
        # 💡 第一步：先看状态码
        print(f"📡 状态码: {response.status_code}")
        
        if response.status_code == 200:
            res_json = response.json()
            # 💡 第二步：检查返回的 JSON 结构是否符合预期
            if 'statuses' in res_json:
                comments = res_json['statuses']
                print(f"--- 🕵️ 成功获取实时舆情 ({len(comments)}条) ---")
                for c in comments:
                    # 使用 get 防止字段缺失报错
                    text = c.get('description', '无内容')[:50].replace('<br/>', '')
                    print(f"💬 评论: {text}...")
            else:
                print(f"⚠️ 拿到数据但没发现评论，返回内容：{res_json}")
        elif response.status_code == 403:
            print("❌ 403 被封禁！说明你的 Cookie 失效了，或者全角字符导致校验失败。")
        else:
            print(f"❌ 访问失败，错误信息: {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ 运行异常: {e}")

# 执行
get_market_sentiment()