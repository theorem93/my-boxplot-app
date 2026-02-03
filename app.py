import streamlit as st
import matplotlib.pyplot as plt

# 設定網頁標題
st.set_page_config(page_title="專業盒狀圖產生器", layout="centered")
st.title("📊 盒狀圖生成工具")
st.write("輸入統計數值，立即生成視覺化圖表。")

# 側邊欄輸入
st.sidebar.header("數據輸入")
label = st.sidebar.text_input("數據名稱", "範例數據")
min_v = st.sidebar.number_input("最小值 (Min)", value=10.0)
q1 = st.sidebar.number_input("第一四分位數 (Q1)", value=25.0)
med = st.sidebar.number_input("中位數 (Median)", value=35.0)
q3 = st.sidebar.number_input("第三四分位數 (Q3)", value=50.0)
max_v = st.sidebar.number_input("最大值 (Max)", value=80.0)

# 邏輯檢查
if not (min_v <= q1 <= med <= q3 <= max_v):
    st.error("錯誤：請確保數值大小順序正確 (Min ≤ Q1 ≤ Median ≤ Q3 ≤ Max)")
else:
    # 繪圖邏輯
    fig, ax = plt.subplots(figsize=(10, 6))
    stats = [{
        'label': label,
        'whislo': min_v,
        'q1': q1,
        'med': med,
        'q3': q3,
        'whishi': max_v,
        'fliers': []
    }]
    
    box = ax.bxp(stats, patch_artist=True, showfliers=False)
    
    # 美化
    plt.setp(box[0]['boxes'], facecolor='#A6CEE3', linewidth=2)
    plt.setp(box[0]['medians'], color='#E31A1C', linewidth=3)
    
    ax.set_ylabel("數值", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 顯示圖表
    st.pyplot(fig)
    
    # 下載按鈕
    fn = 'boxplot.png'
    plt.savefig(fn)
    with open(fn, "rb") as img:
        st.download_button(label="📥 下載圖表圖片", data=img, file_name=fn, mime="image/png")