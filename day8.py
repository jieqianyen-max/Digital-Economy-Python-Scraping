from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def start_browser():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # 💡 关键参数：通过设置用户数据目录，可以记住你的登录状态，避免每次弹出登录框
    # options.add_argument("--user-data-dir=C:\\Users\\你的用户名\\AppData\\Local\\Google\\Chrome\\User Data")
    
    # 模拟真实浏览器，减少自动化特征
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print("🚀 正在访问雪球，请在弹窗出现时，如有必要请手动点击关闭或登录一次...")
        driver.get("https://xueqiu.com/")
        
        # 💡 增加一个容错：如果弹出登录框，先等一等手动处理
        time.sleep(5) 
        
        wait = WebDriverWait(driver, 20)
        
        # 💡 使用更稳健的选择器。有时 placeholder 可能会变，改用 class 或 id
        search_xpath = "//input[contains(@placeholder, '搜索')]"
        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, search_xpath)))
        
        print("🔍 发现搜索框，准备搜索中国平安...")
        search_input.click() # 先点一下确保聚焦
        search_input.send_keys("中国平安")
        search_input.send_keys(Keys.ENTER)
        
        # 等待数据刷新
        time.sleep(10)
        print(f"✅ 成功看到结果！当前标题: {driver.title}")
        
    except Exception as e:
        print(f"❌ 运行报错: {type(e).__name__}")
        # 如果报错，我们可以暂停一下，让你看看报错现场，而不是立刻关闭
        time.sleep(10) 
    finally:
        print("🧹 任务结束，正在释放资源...")
        driver.quit()

if __name__ == "__main__":
    start_browser()