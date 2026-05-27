import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

# 1. تحميل ودمج البيانات مع تخزين اسم الملف (كمباراة)
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    for f in all_files:
        temp_df = pd.read_csv(f)
        temp_df['Match_Name'] = os.path.basename(f) # إضافة اسم الملف كاسم للمباراة
        df_list.append(temp_df)
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

# 2. الفلترة
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))

# فلتر المباريات (يظهر أسماء الملفات)
all_matches = sorted(df['Match_Name'].unique())
selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)

# تصفية البيانات
player_df = df[(df['Player'] == selected_player) & (df['Match_Name'].isin(selected_matches))]

# 3. اختيار الأكشن
all_actions = sorted(df['Action'].dropna().unique())
selected_actions = st.sidebar.multiselect("اختر أنواع البيانات:", options=all_actions, default=[a for a in ['pressing', 'counter_pressing'] if a in all_actions])

# 4. العرض
st.title(f"تحليل {selected_player}")
col1, col2 = st.columns([1, 2])

with col1:
    for action in selected_actions:
        st.metric(f"إجمالي {action}", len(player_df[player_df['Action'] == action]))

with col2:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(8, 5))
    
    for action in selected_actions:
        data = player_df[player_df['Action'] == action]
        # ألوان ثابتة
        color = 'red' if action == 'pressing' else 'blue' if action == 'counter_pressing' else 'black'
        pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, 
                      color=color, facecolor='none', edgecolor=color, s=100, label=action)
    
    plt.legend()
    st.pyplot(fig)
