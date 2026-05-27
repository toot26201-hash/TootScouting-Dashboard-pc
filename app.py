import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

# 1. إعداد الصفحة
st.set_page_config(layout="wide", page_title="TootScouting Analytics")
st.title("⚽ TootScouting: لوحة تحليل الموسم الكامل")

# 2. تحميل ودمج البيانات
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    required_cols = ['Player', 'Action', 'X Start', 'Y Start']
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            if all(col in temp_df.columns for col in required_cols):
                temp_df['Match_Name'] = os.path.basename(f)
                temp_df = temp_df.dropna(subset=required_cols)
                df_list.append(temp_df)
        except: continue
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV صالحة في المستودع.")
    st.stop()

# 3. الفلترة
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().astype(str).unique()))
all_matches = sorted(df['Match_Name'].unique())
selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)

player_df = df[(df['Player'] == selected_player) & (df['Match_Name'].isin(selected_matches))]

all_actions = sorted(df['Action'].dropna().unique())
selected_actions = st.sidebar.multiselect("اختر أنواع البيانات:", options=all_actions, default=[a for a in ['pressing', 'counter_pressing'] if a in all_actions])

# 4. واجهة العرض
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"بيانات: {selected_player}")
    for action in selected_actions:
        count = len(player_df[player_df['Action'] == action])
        st.metric(f"إجمالي {action}", count)

with col2:
    st.subheader("خريطة التمركز التكتيكي")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(10, 6))
    
    # تعريف الألوان
    action_colors = {
        'pressing': 'red', 
        'counter_pressing': 'blue', 
        'progressive_pass': 'green', 
        'progressive_run': 'purple'
    }
    
    # رسم كل الأنواع المختارة
    for action in selected_actions:
        data = player_df[player_df['Action'] == action]
        color = action_colors.get(action, 'black')
        
        if not data.empty:
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                          color=color, facecolor='none', edgecolor=color, 
                          s=100, label=action, linewidth=1.5)
    
    plt.legend(loc='upper right')
    st.pyplot(fig)
