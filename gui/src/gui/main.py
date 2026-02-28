import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ページ設定
st.set_page_config(page_title="Streamlit サンプル", page_icon="🚀", layout="wide")

# タイトル
st.title("🚀 Streamlit サンプルアプリ")
st.write("Streamlit の主要な機能をまとめたデモです。")

# サイドバー
st.sidebar.header("設定")
chart_type = st.sidebar.selectbox(
    "グラフの種類", ["折れ線グラフ", "棒グラフ", "散布図"]
)
num_points = st.sidebar.slider("データ点数", min_value=10, max_value=200, value=50)
show_table = st.sidebar.checkbox("データテーブルを表示", value=True)

# データ生成
np.random.seed(42)
x = np.arange(num_points)
y1 = np.cumsum(np.random.randn(num_points))
y2 = np.cumsum(np.random.randn(num_points))

df = pd.DataFrame({"x": x, "系列A": y1, "系列B": y2})

# 2カラムレイアウト
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 グラフ")
    fig, ax = plt.subplots(figsize=(6, 4))

    if chart_type == "折れ線グラフ":
        ax.plot(x, y1, label="系列A")
        ax.plot(x, y2, label="系列B")
    elif chart_type == "棒グラフ":
        width = 0.4
        ax.bar(x, y1, width=width, label="系列A", alpha=0.7)
        ax.bar(x + width, y2, width=width, label="系列B", alpha=0.7)
    else:
        ax.scatter(x, y1, label="系列A", alpha=0.7)
        ax.scatter(x, y2, label="系列B", alpha=0.7)

    ax.legend()
    ax.set_title(chart_type)
    st.pyplot(fig)

with col2:
    st.subheader("📈 メトリクス")
    m1, m2 = st.columns(2)
    m1.metric("系列A 最終値", f"{y1[-1]:.2f}", f"{y1[-1] - y1[-2]:.2f}")
    m2.metric("系列B 最終値", f"{y2[-1]:.2f}", f"{y2[-1] - y2[-2]:.2f}")

    st.subheader("📝 テキスト入力")
    user_input = st.text_input("メモを入力してください", placeholder="ここに入力...")
    if user_input:
        st.success(f"入力内容: {user_input}")

    st.subheader("🎛️ インタラクション")
    if st.button("データを再生成"):
        st.toast("データを再生成しました！", icon="✅")

# データテーブル
if show_table:
    st.subheader("📋 データテーブル")
    st.dataframe(df.head(10), use_container_width=True)

# フッター
st.divider()
st.caption("Streamlit サンプルアプリ | Python + Streamlit で作成")
