import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# إعداد الصفحة لتكون واسعة
st.set_page_config(layout="wide")

# كود التنسيق (CSS) لتثبيت شكل الكارت
st.markdown("""
<style>
    .main-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .title-text { color: #2c3e50; font-weight: bold; font-size: 28px; }
    .stat-box { background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# البيانات
df = pd.read_csv('EPS-honka-actions.csv')
player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == player]

# --- الكارت ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown(f'<p class="title-text">تقرير تحليل الضغط: {player}</p>', unsafe_allow_html=True)
    
    # تقسيم الصفحة لجزئين: اليمين للخريطة، اليسار للبيانات
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("خريطة كثافة الضغط")
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
        fig, ax = pitch.draw(figsize=(6, 4))
        press = player_df[player_df['Action'] == 'pressing']
        sns.kdeplot(x=press['X Start']*105, y=press['Y Start']*68, fill=True, cmap='viridis', ax=ax)
        st.pyplot(fig)
        
    with col2:
        st.subheader("أبرز الإحصائيات (Percentile)")
        stats = {"الضغط العالي": 85, "الضغط المضاد": 75, "نجاح الضغط": 60, "الضغط الدفاعي": 50}
        for label, val in stats.items():
            st.write(f"**{label}**")
            st.progress(val / 100)
            
    st.markdown('</div>', unsafe_allow_html=True)
