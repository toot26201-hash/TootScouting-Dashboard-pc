import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide")
st.title("TootScouting: تقرير تحليل الضغط")

# تحميل البيانات
df = pd.read_csv('EPS-honka-actions.csv')
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == selected_player]

# تصميم الكارت (تقسيم الشاشة لعمودين)
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("كثافة الضغط")
    # رسم خريطة الكثافة (Heatmap)
    pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, 
                  pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(8, 6))
    
    # استخدام KDEPlot لرسم الكثافة (شكل الضغط)
    sns.kdeplot(x=player_df[player_df['Action']=='pressing']['X Start'] * 100, 
                y=player_df[player_df['Action']=='pressing']['Y Start'] * 100, 
                fill=True, cmap='viridis', levels=10, thresh=0.1, ax=ax)
    st.pyplot(fig)

with col_right:
    st.subheader("أبرز إحصائيات الضغط")
    # أشرطة الـ Percentiles
    stats = {
        "الضغط العالي (High Press)": 85,
        "الضغط المضاد (Counter-Press)": 72,
        "نجاح الضغط (%)": 60,
        "الضغط في الوسط": 45
    }
    
    for label, val in stats.items():
        st.write(f"**{label}**")
        st.progress(val / 100)
