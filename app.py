import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم")

# 1. دالة التحميل الموحدة
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            temp_df['Match_Name'] = os.path.basename(f)
            df_list.append(temp_df)
        except: continue
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV.")
    st.stop()

# 2. الفلترة مع حماية من الأخطاء (التنظيف الذكي)
# نحول القيم لنص ونحذف الفارغ قبل الترتيب
players = sorted([str(p) for p in df['Player'].dropna().unique()])
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)

# فلتر المباريات
all_matches = sorted(df['Match_Name'].unique())
selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)

player_df = df[(df['Player'] == selected_player) & (df['Match_Name'].isin(selected_matches))]

# اختيار الأحداث
actions = st.multiselect("اختر الأحداث للعرض:", options=df['Action'].dropna().unique(), default=['pressing', 'counter_pressing'] if 'pressing' in df['Action'].unique() else [])

# 3. العرض
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"تحليل: {selected_player}")
    for action in actions:
        count = len(player_df[player_df['Action'] == action])
        st.metric(f"إجمالي {action}", count)
            
with col2:
    st.subheader("خريطة التمركز")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(8, 5))
    
    for action in actions:
        data = player_df[player_df['Action'] == action]
        if not data.empty:
            color = 'red' if 'press' in action else 'blue'
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                          color=color, facecolor='none', edgecolor=color, s=100, label=action)
    
    plt.legend(loc='upper right')
    st.pyplot(fig)
