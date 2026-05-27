import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="TootScouting Dashboard")
st.title("⚽ TootScouting: لوحة تحليل الأداء")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv('EPS-honka-actions.csv')

try:
    df = load_data()
except:
    st.error("خطأ: تأكد من رفع ملف 'EPS-honka-actions.csv' في نفس مجلد الكود.")
    st.stop()

# 3. القائمة الجانبية
st.sidebar.header("إعدادات التقرير")
players = sorted(df['Player'].dropna().unique())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)

# تصفية البيانات
player_df = df[df['Player'] == selected_player]

# 4. عرض الإحصائيات (Metrics)
col1, col2, col3 = st.columns(3)
total_actions = len(player_df)
pressing_count = len(player_df[player_df['Action'] == 'pressing'])
aerial_count = len(player_df[player_df['Action'] == 'Aerial'])

col1.metric("إجمالي التحركات", total_actions)
col2.metric("عمليات الضغط", pressing_count)
col3.metric("الكرات الهوائية", aerial_count)

# 5. تحليل المقارنة (الذكاء التحليلي)
st.subheader("تحليل الأداء مقارنة بالفريق")
team_avg = df[df['Action'] == 'pressing'].groupby('Player').size().mean()

if pressing_count > team_avg:
    st.success(f"اللاعب يتفوق على متوسط الفريق في الضغط (اللاعب: {pressing_count} | المتوسط: {team_avg:.1f})")
else:
    st.warning(f"أداء اللاعب في الضغط أقل من متوسط الفريق (اللاعب: {pressing_count} | المتوسط: {team_avg:.1f})")

# 6. الخريطة الحرارية (Heatmap)
st.subheader("خريطة التمركز والتحركات")
pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, 
              pitch_color='#f0f0f0', line_color='#666666')
fig, ax = pitch.draw(figsize=(10, 7))

# رسم التحركات
pitch.scatter(player_df['X Start'] * 100, player_df['Y Start'] * 100, 
              ax=ax, color='blue', s=80, alpha=0.5, label='تحركات')
# تمييز الضغط باللون الأحمر
pitch.scatter(player_df[player_df['Action'] == 'pressing']['X Start'] * 100, 
              player_df[player_df['Action'] == 'pressing']['Y Start'] * 100, 
              ax=ax, color='red', s=120, alpha=0.8, label='ضغط (Pressing)')

plt.legend(loc='upper left')
st.pyplot(fig)

# 7. عرض البيانات الخام
if st.checkbox("عرض جدول البيانات الخام للاعب"):
    st.write(player_df)
