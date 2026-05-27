import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# إعداد الصفحة لتكون واسعة
st.set_page_config(layout="wide")

st.title("⚽ TootScouting: خريطة الضغط والضغط العكسي")

# تحميل البيانات (مع تأكيد وجود الملف)
@st.cache_data
def load_data():
    return pd.read_csv('EPS-honka-actions.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("لم يتم العثور على ملف 'EPS-honka-actions.csv'. تأكد من وجوده في نفس المجلد.")
    st.stop()

# القائمة الجانبية لاختيار اللاعب
players = sorted(df['Player'].dropna().unique())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

# --- رسم الملعب (على الطراز الفنلندي الداكن) ---
# سأستخدم pitch_type='custom' وحدد الأبعاد لأنني سأقوم بتحويل الإحداثيات يدوياً
pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100,
              pitch_color='#22312b', line_color='#c7d5cc', line_zorder=2)
fig, ax = pitch.draw(figsize=(10, 7))

# --- رسم نقاط الضغط (باللون الأحمر - دوائر مفرغة) ---
press_df = player_df[player_df['Action'] == 'pressing']
if not press_df.empty:
    pitch.scatter(press_df['X Start'] * 100, press_df['Y Start'] * 100, 
                  ax=ax, color='#ff0000', 
                  edgecolor='#ff0000', facecolor='none', linewidth=1.5,
                  s=100, alpha=0.7, label='الضغط (Pressing)')

# --- رسم نقاط الضغط العكسي (باللون الأزرق - دوائر مفرغة) ---
counter_press_df = player_df[player_df['Action'] == 'counter_pressing']
if not counter_press_df.empty:
    pitch.scatter(counter_press_df['X Start'] * 100, counter_press_df['Y Start'] * 100, 
                  ax=ax, color='#00a2ff', 
                  edgecolor='#00a2ff', facecolor='none', linewidth=1.5,
                  s=100, alpha=0.7, label='الضغط العكسي (Counter-Pressing)')

# إضافة دليل الألوان (Legend)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1), fontsize=10)

st.pyplot(fig)

# عرض البيانات الخام للاعب (اختياري)
if st.checkbox("عرض جدول البيانات الخام للاعب"):
    st.write(player_df[['Player', 'Action', 'X Start', 'Y Start']])
