import pandas as pd

# 1. 读取昨天辛苦抓到的实战数据
file_name = "Result_SZ300750_1775832998.xlsx" # 💡 请改为你文件夹里真实的文件名
df = pd.read_excel(file_name)

print("🔍 原始数据形状:", df.shape)

# 2. 挑选核心列（剔除你看到的“乱码”空列）
# 只保留：成交时间、价格(current)、涨跌(chg)、成交量(trade_volume)、买卖方向(side)
core_cols = ['成交时间', 'current', 'chg', 'percent', 'trade_volume', 'side']
# 💡 容错处理：只选取存在的列
existing_cols = [c for c in core_cols if c in df.columns]
df_clean = df[existing_cols].copy()

# 3. 数据转换：让 side（买卖方向）变直观
# 假设 1 是买入，-1 是卖出，0 是中性
side_map = {1: '买入', -1: '卖出', 0: '中性'}
df_clean['交易性质'] = df_clean['side'].map(side_map)

# 4. 特征工程：计算单笔成交金额
# 成交金额 = 价格 * 成交量
df_clean['成交金额'] = df_clean['current'] * df_clean['trade_volume']

# 5. 排序：按时间从早到晚排序
df_clean = df_clean.sort_values(by='成交时间', ascending=True)

# 6. 保存清洗后的“纯净版”数据
clean_file = "SZ300750_清洗后数据.xlsx"
df_clean.to_excel(clean_file, index=False)

print("\n✨ 清洗完成！")
print(df_clean.head())
print(f"\n📂 清洗后的实战数据已保存至: {clean_file}")