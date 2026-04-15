import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 设置绘图风格
sns.set_theme(style="whitegrid")
# 💡 提示：如果你的电脑没有黑体字，图表中的中文可能显示为方块。建议先用英文标注。

# 2. 读取 Day 13 的分析结果
analysis_df = pd.read_excel("Day13_50_Stocks_Analysis.xlsx")

# --- 任务一：绘制全市场资金流向截面图 ---
# 取 Flow Ratio 最高和最低的各 10 只股票进行对比
top_10 = analysis_df.sort_values('flow_ratio', ascending=False).head(10)
bottom_10 = analysis_df.sort_values('flow_ratio', ascending=True).head(10)
plot_data = pd.concat([top_10, bottom_10])

plt.figure(figsize=(12, 6))
# 💡 逻辑：大于 0 为红色，小于 0 为蓝色
colors = ['#e74c3c' if x > 0 else '#3498db' for x in plot_data['flow_ratio']]
sns.barplot(data=plot_data, x='symbol', y='flow_ratio', palette=colors)

plt.title('Top 10 vs Bottom 10: Money Flow Ratio', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Flow Ratio (Sentiment Index)')
plt.tight_layout()
plt.savefig('Market_Sentiment_Bar.png') # 保存图表
print("✅ 第一张图：全市场情感扫描已生成！")

# --- 任务二：绘制冠军股 SZ301248 的盘中资金趋势 ---
# 读取原始逐笔数据
raw_df = pd.read_excel("Market_50_Stocks_Full.xlsx")
# 筛选出冠军股
champion = raw_df[raw_df['symbol'] == 'SZ301248'].copy()
champion['成交时间'] = pd.to_datetime(champion['成交时间'])
champion = champion.sort_values('成交时间')

# 计算累计净流入
champion['amount'] = champion['current'] * champion['trade_volume']
champion['net_val'] = champion.apply(lambda x: x['amount'] if x['side'] == 1 else (-x['amount'] if x['side'] == -1 else 0), axis=1)
champion['cum_net_flow'] = champion['net_val'].cumsum()

plt.figure(figsize=(12, 6))
plt.plot(champion['成交时间'], champion['cum_net_flow'], color='#27ae60', linewidth=2.5)
plt.fill_between(champion['成交时间'], champion['cum_net_flow'], color='#27ae60', alpha=0.1)

plt.title(f'Intraday Cumulative Money Flow: SZ301248', fontsize=16)
plt.xlabel('Time')
plt.ylabel('Cumulative Net Amount (CNY)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('Champion_Intraday_Trend.png')
print("✅ 第二张图：冠军股资金曲线已生成！")