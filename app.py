import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob

# 1. إعداد الصفحة
st.set_page_config(layout="wide", page_title="TootScouting Analytics")
st.title("⚽ TootScouting: لوحة تحليل الموسم الكامل")

# 2. تحميل ودمج البيانات (مضاد للأخطاء)
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    required_cols = ['Player', 'Action', 'X Start', 'Y Start']
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            if all(col in temp_df.columns for col in required_cols):
                temp_df = temp_df.dropna(subset=required_cols)
                df_list.append(temp_df)
        except: continue
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV صالحة في المستودع.")
    st.stop()

# 3. الفلترة
players = sorted([str(p) for p in df['Player'].dropna().unique()])
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

all_actions = sorted(df['Action'].dropna().unique())
default_actions = [a for a in ['pressing', 'counter_pressing'] if a in all_actions]

st.sidebar.subheader("تحليل الأداء")
selected_actions = st.sidebar.multiselect("اختر أنواع البيانات:", options=all_actions, default=default_actions)

# 4. واجهة العرض (الكارت)
st.markdown('<div class="report-card" style="background:white; padding:30px; border-radius:20px; border:2px solid #e0e0e0;">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"إحصائيات: {selected_player}")
    for action in selected_actions:
        count = len(player_df[player_df['Action'] == action])
        st.metric(f"إجمالي {action}", count)

with col2:
    st.subheader("خريطة التمركز التكتيكي")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(8, 5))
    
    for action in selected_actions:
        data = player_df[player_df['Action'] == action]
        
        # رسم الضغط والضغط العكسي كدوائر مفرغة
        if action == 'pressing':
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                          color='red', facecolor='none', edgecolor='red', s=100, label='الضغط')
        elif action == 'counter_pressing':
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                          color='blue', facecolor='none', edgecolor='blue', s=100, label='الضغط العكسي')
        else:
            # أي نوع بيانات آخر (تمريرات، إلخ)
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                          color='black', s=80, label=action)

    plt.legend(loc='upper right')
    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)
