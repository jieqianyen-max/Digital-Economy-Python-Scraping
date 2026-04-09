import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def industrial_data_fetch():
    # 1. 启动实战引擎
    driver = webdriver.Chrome()
    try:
        # 2. 实战路径：直接访问数据密度最高的行情中心
        driver.get("https://xueqiu.com/hq")
        time.sleep(5) 

        # 3. 自动化提取：抓取当前页面的所有行情行
        print("📊 正在同步实时行情数据...")
        rows = driver.find_elements(By.XPATH, "//table//tr")[1:16] # 抓取前15只股票
        
        final_data = []
        for row in rows:
            cols = row.text.split()
            if len(cols) >= 3:
                final_data.append({
                    "股票代码": cols[0],
                    "最新价": cols[1],
                    "涨跌幅": cols[2]
                })

        # 4. 实战落地：生成你的第一份金融资产负债表原始数据
        df = pd.DataFrame(final_data)
        file_name = f"Market_Snapshot_{time.strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        
        print(f"✅ 实战任务达成！数据已存入: {file_name}")
        print(df.head()) # 打印前几行看看你的战果

    finally:
        driver.quit()

if __name__ == "__main__":
    industrial_data_fetch()