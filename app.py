import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# 1. إعداد الصفحة
st.set_page_config(layout="wide")
st.title("TootScouting: تقرير الأداء")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv('EPS-honka-actions.csv')

df = load_data()

# 3. اختيار اللاعب (مع التأكد من وجود البيانات)
players = sorted(df['Player'].dropna().unique())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

# 4. بناء الكارت (Card)
st.markdown("""
<style>
    .card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"تحليل: {selected_player}")
        press_count = len(player_df[player_df['Action'] == 'pressing'])
        st.metric("عدد عمليات الضغط", press_count)
        
        # أشرطة التقييم
        st.write("معدلات الضغط (Percentiles)")
        st.progress(0.85) # يمكنك استبدالها بمعادلة حسابية
        st.write("الضغط العالي")
    
    with col2:
        # رسم الملعب
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
        fig, ax = pitch.draw(figsize=(6, 4))
        
        # التأكد من وجود بيانات قبل الرسم
        press_data = player_df[player_df['Action'] == 'pressing']
        if not press_data.empty:
            sns.kdeplot(x=press_data['X Start'] * 105, y=press_data['Y Start'] * 68, fill=True, cmap='viridis', ax=ax)
        
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
