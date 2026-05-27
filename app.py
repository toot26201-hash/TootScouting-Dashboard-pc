import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

# 1. إعداد الصفحة
st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم")

# 2. تحميل البيانات ودمج كل ملفات الـ CSV من المجلد
@st.cache_data
def load_all_matches():
    # البحث عن كل ملفات CSV في نفس مجلد الكود
    all_files = glob.glob("*.csv")
    df_list = []
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            # إضافة اسم الملف كعمود للتمييز بين المباريات
            temp_df['Match_Name'] = os.path.basename(f)
            df_list.append(temp_df)
        except: continue
    
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV صالحة.")
    st.stop()

# 3. الفلترة
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].unique()))

# فلتر المباريات (لضمان دمج واختيار كل الماتشات)
all_matches = sorted(df[df['Player'] == selected_player]['Match_Name'].unique())
selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)

player_df = df[(df['Player'] == selected_player) & (df['Match_Name'].isin(selected_matches))]

# اختيار الأكشن (ضغط، ضغط عكسي، إلخ)
actions = st.multiselect("اختر الأحداث للعرض:", options=df['Action'].unique(), default=['pressing', 'counter_pressing'])

# 4. الكارت الاحترافي
st.markdown("""
<style>
    .report-card { background-color: white; padding: 25px; border-radius: 15px; border: 2px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"تحليل الموسم: {selected_player}")
        # عرض الإحصائيات
        for action in actions:
            count = len(player_df[player_df['Action'] == action])
            st.metric(f"إجمالي {action}", count)
            
    with col2:
        st.subheader("خريطة التمركز")
        # الملعب بأبعاد طبيعية وخلفية بيضاء
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(8, 5))
        
        # رسم البيانات (ضغط وأي أكشن آخر)
        for action in actions:
            data = player_df[player_df['Action'] == action]
            if not data.empty:
                color = 'red' if 'press' in action else 'blue' # تحديد الألوان تلقائياً
                pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                              color=color, facecolor='none', edgecolor=color, s=100, label=action)
        
        plt.legend(loc='upper right')
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
