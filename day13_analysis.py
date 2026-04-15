import pandas as pd

# 1. 读取 Day 12 的 Master 表
df = pd.read_excel("Day12_Final_Master.xlsx")

# 2. 预处理：计算单笔成交额
# 成交额 = 价格 * 成交量
df['amount'] = df['current'] * df['trade_volume']

# 3. 核心逻辑：区分买入与卖出
# 我们创建一个新列 'net_buy'：买入为正，卖出为负
def calc_net(row):
    if row['side'] == 1:
        return row['amount']
    elif row['side'] == -1:
        return -row['amount']
    else:
        return 0

df['net_amount'] = df.apply(calc_net, axis=1)

# 4. 见证奇迹：使用 Groupby 进行分组统计
# 我们按股票代码(symbol)分组，统计它们的总成交额和净买入额
analysis_res = df.groupby('symbol').agg({
    'amount': 'sum',        # 总成交额
    'net_amount': 'sum',    # 净流入金额
    'current': 'mean'       # 平均成交价
}).reset_index()

# 5. 计算净流入占比（判断资金参与深度）
analysis_res['flow_ratio'] = analysis_res['net_amount'] / analysis_res['amount']

# 6. 结果展示
print("📊 今日多股资金流向扫描：")
print("-" * 50)
print(analysis_res.sort_values(by='flow_ratio', ascending=False))

# 保存为你的第一份量化分析报告
analysis_res.to_excel("Day13_Money_Flow_Report.xlsx", index=False)