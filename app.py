import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="TootScouting Report")

# تحميل البيانات
df = pd.read_csv('EPS-honka-actions.csv')

# القائمة الجانبية
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == selected_player]

# --- العنوان والتصميم العلوي ---
st.title(f"تقرير تحليل الضغط: {selected_player}")
st.write("الموسم: 2026 | TootScouting")

# تصميم صفين رئيسيين (كارتين)
row1 = st.columns([1, 1])

with row1[0]:
    st.subheader("كثافة الضغط (Heatmap)")
    # رسم ملعب داكن احترافي
    pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, 
                  pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(8, 6))
    
    # رسم الكثافة (الـ Heatmap)
    pressing_df = player_df[player_df['Action'] == 'pressing']
    if not pressing_df.empty:
        sns.kdeplot(x=pressing_df['X Start'] * 100, y=pressing_df['Y Start'] * 100, 
                    fill=True, cmap='viridis', levels=15, thresh=0.1, ax=ax)
    st.pyplot(fig)

with row1[1]:
    st.subheader("أبرز إحصائيات الضغط (Percentiles)")
    # إحصائيات وهمية للمثال (يمكنك استبدالها بمعادلات حسابية من ملفك)
    stats = {
        "الضغط العالي (High Press)": 85,
        "الضغط المضاد (Counter-Press)": 70,
        "نجاح الضغط (%)": 65,
        "الضغط في الوسط": 50
    }
    
    for label, val in stats.items():
        st.write(f"**{label}**")
        st.progress(val / 100)
        st.write(f"{val}%")

# تذييل الصفحة
st.markdown("---")
st.caption("تحليل بيانات معتمد من TootScouting")
