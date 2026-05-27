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

# تصميم الكارت
st.markdown("""
<style>
    .report-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 2px solid #e0e0e0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    # 1. العنوان
    st.title(f"تقرير الضغط الاحترافي: {player}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # الإحصائيات (الأرقام)
        st.subheader("إحصائيات الأداء")
        pressing = len(player_data[player_data['Action'] == 'pressing'])
        st.metric("عدد عمليات الضغط", pressing)
        
        # أشرطة الـ Percentiles
        st.write("معدلات الضغط (Percentiles)")
        st.progress(0.85)
        st.write("الضغط العالي")
        st.progress(0.70)
        st.write("الضغط المضاد")
        
    with col2:
        # الخريطة الحرارية (الكثافة)
        st.subheader("كثافة الضغط")
        pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, pitch_color='#22312b', line_color='#c7d5cc')
        fig, ax = pitch.draw(figsize=(6, 4))
        press_df = player_data[player_data['Action'] == 'pressing']
        if not press_df.empty:
            sns.kdeplot(x=press_df['X Start']*100, y=press_df['Y Start']*100, fill=True, cmap='viridis', ax=ax)
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
