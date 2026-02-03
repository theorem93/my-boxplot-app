import streamlit as st
import matplotlib.pyplot as plt

# 1. 網頁基本設定
st.set_page_config(page_title="專業盒狀圖產生器", layout="centered")
st.title("📊 盒狀圖生成工具")
st.write("請在左側選單輸入統計數值，圖表將會自動即時更新。")

# 2. 側邊欄輸入：讓使用者輸入數據
st.sidebar.header("數據輸入")
label = st.sidebar.text_input("數據名稱", "我的樣本數據")
min_v = st.sidebar.number_input("最小值 (Min)", value=10.0)
q1 = st.sidebar.number_input("第一四分位數 (Q1)", value=25.0)
med = st.sidebar.number_input("中位數 (Median)", value=35.0)
q3 = st.sidebar.number_input("第三四分位數 (Q3)", value=50.0)
max_v = st.sidebar.number_input("最大值 (Max)", value=80.0)

# 3. 邏輯檢查：確保數值順序正確
if not (min_v <= q1 <= med <= q3 <= max_v):
    st.error("⚠️ 數值順序有誤！請確保：最小值 ≤ Q1 ≤ 中位數 ≤ Q3 ≤ 最大值")
else:
    # 4. 準備繪圖數據
    fig, ax = plt.subplots(figsize=(8, 6))
    stats = [{
        'label': label,
        'whislo': min_v,
        'q1': q1,
        'med': med,
        'q3': q3,
        'whishi': max_v,
        'fliers': []  # 無離群值
    }]
    
    # 5. 繪製盒狀圖 (這是之前出錯的地方，現在已修正)
    # patch_artist=True 才能填充顏色
    result_dict = ax.bxp(stats, patch_artist=True, showfliers=False)
    
    # 6. 美化圖表元件
    # 設定盒子顏色
    for box in result_dict['boxes']:
        box.set_facecolor('#A6CEE3')  # 淺藍色
        box.set_edgecolor('#1F78B4')  # 深藍邊框
        box.set_linewidth(2)

    # 設定中位數線條顏色
    for median in result_dict['medians']:
        median.set_color('#E31A1C')   # 紅色
        median.set_linewidth(3)

    # 設定鬍鬚與橫槓顏色
    plt.setp(result_dict['whiskers'], color='#1F78B4', linewidth=2)
    plt.setp(result_dict['caps'], color='#1F78B4', linewidth=2)

    # 7. 圖表輔助設定
    ax.set_ylabel("數值", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 8. 在 Streamlit 網頁上顯示圖表
    st.pyplot(fig)
    
    # 9. 提供下載功能
    fn = 'boxplot.png'
    plt.savefig(fn, bbox_inches='tight')
    with open(fn, "rb") as img:
        st.download_button(label="📥 下載圖表圖片", data=img, file_name=fn, mime="image/png")
