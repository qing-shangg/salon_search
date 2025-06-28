import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("merged.csv")

df = load_data()

st.title("美容院データ検索＆可視化アプリ")

# 滑动条筛选评分和价格
min_star, max_star = st.sidebar.slider(
    "評価点の範囲", float(df['star'].min()), float(df['star'].max()),
    (float(df['star'].min()), float(df['star'].max()))
)

min_price, max_price = st.sidebar.slider(
    "価格の範囲", float(df['price'].min()), float(df['price'].max()),
    (float(df['price'].min()), float(df['price'].max()))
)

filtered_df = df[
    (df['star'] >= min_star) & (df['star'] <= max_star) &
    (df['price'] >= min_price) & (df['price'] <= max_price)
]

st.write(f"### 絞り込み結果： {len(filtered_df)} 件")

st.write("価格と評価点の散布図")
st.scatter_chart(filtered_df[['price', 'star']].rename(columns={'price':'価格', 'star':'評価'}))

st.write("### 店舗一覧（クリックでGoogleマップへ）")
for idx, row in filtered_df.iterrows():
    map_url = f"https://www.google.com/maps/search/?api=1&query={row['address']}"
    st.markdown(f"[{row['name_salon']}]({map_url}) - 評価: {row['star']}, 価格: {row['price']}")

st.write("### 評価トップ5")
top5 = df.sort_values(by='star', ascending=False).head(5)
for i, row in enumerate(top5.itertuples(), 1):
    url = f"https://www.google.com/maps/search/?api=1&query={row.address}"
    st.markdown(f"{i}. [{row.name_salon}]({url}) - 評価: {row.star}, 価格: {row.price}")
