import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide")

# تحميل البيانات
df = pd.read_csv('EPS-honka-actions.csv')
player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_data = df[df['Player'] == player]

# --- تصميم الكارت "بالحرف" ---
st.markdown("""
<style>
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; }
    .header { font-size: 24px; font-weight: bold; color: #2c3e50; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 1. الترويسة (الاسم والبيانات)
    st.markdown(f'<div class="header">{player} - تقرير الضغط (TootScouting)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.metric("إجمالي الضغط", len(player_data[player_data['Action'] == 'pressing']))
        st.metric("نجاح الاستخلاص", "75%") # يمكنك ربطها بحسابات حقيقية
    
    with col2:
        # هنا سنضع الخريطة الحرارية
        pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, pitch_color='#22312b', line_color='#c7d5cc')
        fig, ax = pitch.draw(figsize=(4, 3))
        pressing = player_data[player_data['Action'] == 'pressing']
        if not pressing.empty:
            sns.kdeplot(x=pressing['X Start']*100, y=pressing['Y Start']*100, fill=True, cmap='viridis', ax=ax)
        st.pyplot(fig)

    # 2. أشرطة الـ Percentiles (تحت الخريطة)
    st.markdown("### كثافة الضغط (Percentile)")
    stats = {"High Press": 90, "Counter-Press": 75, "Defensive Press": 60}
    for label, val in stats.items():
        st.write(label)
        st.progress(val / 100)
        
    st.markdown('</div>', unsafe_allow_html=True)
