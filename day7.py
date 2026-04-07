import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random

# --- 第一步：先定义函数（不要放在 if __name__ 下面） ---

def get_robust_session():
    """创建一个具备自动重试功能的工业级 Session"""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_with_politeness(url, headers):
    """工业级稳健抓取逻辑"""
    session = get_robust_session()
    try:
        # 礼貌性延迟，模拟真人呼吸
        time.sleep(random.uniform(1, 3)) 
        
        # 使用 .strip() 彻底清理 URL 首尾的换行符和空格
        response = session.get(url.strip(), headers=headers, timeout=10)
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        print(f"⚠️ 抓取过程中出现异常: {e}")
    return None

# --- 第二步：最后才是执行区 ---

if __name__ == "__main__":
    # 💡 1. 这里的三引号没问题，但结尾加了 .strip() 来防错
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': '''cookiesu=381774839755266; device_id=95927fb46cd3d61b6560e87d0d1a9e4b; s=ad11ui3ggv; remember=1; xq_a_token=a136967185c8266409c0cbfd856452175d719db4; xqat=a136967185c8266409c0cbfd856452175d719db4; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwNTYzNjk4MjIsImlzcyI6InVjIiwiZXhwIjoxNzc3NDMxODU5LCJjdG0iOjE3NzQ4Mzk4NTk5NTIsImNpZCI6ImQ5ZDBuNEFadXAifQ.q0cg_5BGqUzYHvfdFwaf_MfbEAtE2_pnSsw9fzMz9CEUfPw0YNoS3MdsXSlJVmcYVw61x4h5nxqA2D64KbiPRH7SGVIvSNjDODomRyuNsbs4ncR52jaZ_yozh5scr9FekZdeaolNW9gSUlR2EM3QhjPtcrIgtlP1Byl-k8dYTICES1_1mWh5KnaB3bwuF8jeojNyX5SSelUUKScsVw1-uxZtpak1fpKyyE-B9djGStMCG6toYnmWN7hU_lOQhoVOPZ7G_y90EvR6RvYG-LAVM3TRu4yqBaV6oprxv5McbAG-AYTIaGc5LaDOc6yKMhvhCbvDzwtsmM8UCxH9RZ1hyw; xq_r_token=14532987bc22f749a4ca9205f8001d43a6a1b6bb; xq_is_login=1; u=1056369822; Hm_lvt_1db88642e346389874251b5a1eded6e3=1774877787,1775003285,1775092203,1775288740; HMACCOUNT=E43A5117E149967B; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1775531519; ssxmod_itna=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNQKWQWD0IGQG=RvtDlZkeDZDGIdDqx0ErUiexDQS4bidiGdhrGh4109ImDQ6LXpni_mU1LY=jc65L9k/SSQ4DHxi8DB9DKP2YDeeaDCeDQxirDD4DADibK4D1sDDkD0bpkSgvH4GWDm4EDY5hEm3LDGc5a/7LTDDCNr7KEGEFDGvFPLPqQ_Dqj4Dre9S5O0gDQLG4a4G1ED0HKj6FafdyzLcAQT6cfInwDlKMDC9v9UOKRGOEGfSrgpBYCp9YQ0blre7D4nRD444tRD8AiKRHnhFi04QixHnOBbK5xDGRssmddYYwA10TzmRicked4K4eNooNe7DoOmPDKxxQxo4pOeKO5R25KDK5Qxxnx3m=4Zw0GxwiDD; ssxmod_itna2=1-QqUxcDnD2Dg0KxGqYjKGjx7QG7fYAQpoDXDUMkq7tdGcD8xiKDHKmaYjKXNQKWQWD0IGQG=RyYDi=4DQw8/efTvKyOAyN7Y7IifHI4D
'''.strip()
    }
    
    # 💡 2. URL 建议直接用单引号写成一行，或者末尾也加 .strip()
    target_url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH688146".strip()
    
    print("🚀 启动工业级稳健抓取任务...")
    result = fetch_with_politeness(target_url, my_headers)
    
    if result:
        print("✅ 成功获取数据结构！")
        print(result)
    else:
        print("💡 抓取失败，请检查 Cookie 字符串是否有特殊不可见字符。")