import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="TootScouting Dashboard")

# 1. دالة تحميل البيانات
@st.cache_data
def load_data():
    # تأكد من أن ملفك موجود في نفس المجلد أو قم بتعديل المسار
    df = pd.read_csv('EPS-honka-actions.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("لم يتم العثور على ملف البيانات. تأكد من وجود 'EPS-honka-actions.csv' في مجلد المشروع.")
    st.stop()

# 2. القائمة الجانبية (Sidebar)
st.sidebar.header("إعدادات التقرير")
players = sorted(df['Player'].dropna().unique())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)

# تصفية البيانات للاعب المختار
player_df = df[df['Player'] == selected_player]

# 3. العنوان والإحصائيات السريعة
st.title(f"تقرير تحليل الأداء: {selected_player}")
col1, col2, col3 = st.columns(3)
col1.metric("إجمالي التحركات", len(player_df))
col2.metric("عدد عمليات الضغط", len(player_df[player_df['Action'] == 'pressing']))
col3.metric("عدد الكرات الهوائية", len(player_df[player_df['Action'] == 'Aerial']))

# 4. الخريطة الحرارية (Heatmap)
st.subheader("خريطة التمركز والتحركات")
# استخدام Pitch من mplsoccer
pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, 
              pitch_color='#f0f0f0', line_color='#666666', line_zorder=2)
fig, ax = pitch.draw(figsize=(10, 7))

# إضافة نقاط الـ Pressing بلون مختلف للتمييز
pressing_only = player_df[player_df['Action'] == 'pressing']
pitch.scatter(player_df['X Start'] * 100, player_df['Y Start'] * 100, 
              ax=ax, color='blue', s=80, alpha=0.5, label='Actions')
pitch.scatter(pressing_only['X Start'] * 100, pressing_only['Y Start'] * 100, 
              ax=ax, color='red', s=100, alpha=0.7, label='Pressing')

plt.legend(loc='upper left')
st.pyplot(fig)

# 5. عرض البيانات الخام (اختياري للتحقق)
if st.checkbox("عرض البيانات الخام للاعب"):
    st.write(player_df)