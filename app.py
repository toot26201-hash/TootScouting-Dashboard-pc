import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

# 1. تحميل ودمج البيانات (مع ميزة طباعة الملفات المكتشفة للتأكد)
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    
    # للتأكد من أن الكود يرى كل الملفات
    st.sidebar.write("الملفات المكتشفة:", all_files) 
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            # إضافة اسم الملف كعمود للتمييز
            temp_df['Match_Name'] = os.path.basename(f)
            df_list.append(temp_df)
        except Exception as e:
            st.sidebar.error(f"خطأ في قراءة {f}: {e}")
            continue
            
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV.")
    st.stop()

# 2. الفلاتر
# ملاحظة: إذا ظهرت داتا مباراة واحدة فقط، تأكد أن باقي الملفات تحتوي على أعمدة بنفس الأسماء بالضبط
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
all_matches = sorted(df['Match_Name'].unique())
selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)

# 3. تصفية البيانات
player_df = df[(df['Player'] == selected_player) & (df['Match_Name'].isin(selected_matches))]

# 4. اختيار الأكشن
all_actions = sorted(df['Action'].dropna().unique())
selected_actions = st.sidebar.multiselect("اختر أنواع البيانات:", options=all_actions, default=[a for a in ['pressing', 'counter_pressing'] if a in all_actions])

# 5. العرض
st.title(f"تحليل الموسم: {selected_player}")
# للتأكد من حجم الداتا
st.write(f"عدد السجلات المتاحة لهذا اللاعب: {len(player_df)}")

# (بقية كود الرسم كما هو...)
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
fig, ax = pitch.draw(figsize=(8, 5))
# ... [أكمل رسم الدوائر هنا] ...
st.pyplot(fig)
