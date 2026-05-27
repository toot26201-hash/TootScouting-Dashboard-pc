import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide")

# تحميل البيانات (مع تأكيد وجود الملف)
@st.cache_data
def load_data():
    return pd.read_csv('EPS-honka-actions.csv')

try:
    df = load_data()
except:
    st.error("لم يتم العثور على ملف 'EPS-honka-actions.csv'. تأكد من وجوده في نفس المجلد.")
    st.stop()

# القائمة الجانبية
players = sorted(df['Player'].dropna().unique())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)

# تعريف المتغير الموحد player_df
player_df = df[df['Player'] == selected_player]

# --- تصميم الكارت ---
st.title(f"تقرير الضغط: {selected_player}")

# تقسيم الشاشة
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("إحصائيات الأداء")
    pressing_count = len(player_df[player_df['Action'] == 'pressing'])
    st.metric("عدد عمليات الضغط", pressing_count)
    
    # أشرطة بسيطة للتقييم
    st.write("معدل الضغط (Percentile)")
    st.progress(0.75) 
    st.write("الضغط العالي")

with col2:
    st.subheader("خريطة كثافة الضغط")
    # إعداد الملعب
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(6, 4))
    
    # الرسم باستخدام المتغير الموحد player_df
    press_df = player_df[player_df['Action'] == 'pressing']
    if not press_df.empty:
        sns.kdeplot(x=press_df['X Start'] * 105, y=press_df['Y Start'] * 68, 
                    fill=True, cmap='viridis', levels=15, ax=ax)
    
    st.pyplot(fig)
