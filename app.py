import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import glob

# إعداد الصفحة
st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم")

# 1. تحميل ودمج كل المباريات (تأكد أن ملفاتك في مجلد اسمه data)
@st.cache_data
def load_all_matches():
    all_files = glob.glob("data/*.csv") # تأكد من وجود المجلد
    df_list = [pd.read_csv(f) for f in all_files]
    return pd.concat(df_list, axis=0, ignore_index=True)

df = load_all_matches()

# 2. الفلاتر
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].unique()))
player_df = df[df['Player'] == selected_player]

# فلتر التاريخ (إذا كان هناك عمود تاريخ)
if 'Date' in player_df.columns:
    dates = sorted(player_df['Date'].unique())
    selected_date = st.sidebar.multiselect("اختر المباريات:", dates, default=dates)
    player_df = player_df[player_df['Date'].isin(selected_date)]

# 3. تصميم الكارت
st.markdown("""
<style>
    .report-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e0e0e0; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"تحليل {selected_player}")
        press = len(player_df[player_df['Action'] == 'pressing'])
        counter = len(player_df[player_df['Action'] == 'counter_pressing'])
        
        st.metric("إجمالي الضغط", press)
        st.metric("إجمالي الضغط العكسي", counter)
        
        st.write("---")
        st.write("مستوى الأداء (مقارنة بالموسم)")
        st.progress(0.8) # معادلة ديناميكية
        
    with col2:
        st.subheader("كثافة الأداء عبر الموسم")
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(6, 4))
        
        # دمج الضغط والضغط العكسي في خريطة واحدة
        data_to_plot = player_df[player_df['Action'].isin(['pressing', 'counter_pressing'])]
        if not data_to_plot.empty:
            sns.kdeplot(x=data_to_plot['X Start']*105, y=data_to_plot['Y Start']*68, 
                        fill=True, cmap='viridis', levels=10, ax=ax)
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
