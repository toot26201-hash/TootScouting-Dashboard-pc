import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob

# 1. تحميل ودمج البيانات
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = [pd.read_csv(f) for f in all_files]
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("تأكد من وجود ملفات CSV في المستودع.")
    st.stop()

# 2. اختيار اللاعب (مع التنظيف الذكي لمنع الخطأ)
players = sorted(df['Player'].dropna().astype(str).unique())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

# 3. اختيار أنواع الأداء (اختياري)
all_actions = sorted(df['Action'].dropna().unique())
selected_actions = st.sidebar.multiselect("اختر أنواع البيانات:", options=all_actions, default=[a for a in ['pressing', 'counter_pressing'] if a in all_actions])

# 4. العرض
st.title(f"تحليل الموسم: {selected_player}")
col1, col2 = st.columns([1, 2])

with col1:
    for action in selected_actions:
        st.metric(f"إجمالي {action}", len(player_df[player_df['Action'] == action]))

with col2:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(8, 5))
    
    for action in selected_actions:
        data = player_df[player_df['Action'] == action]
        if action == 'pressing':
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, color='red', facecolor='none', edgecolor='red', s=100, label='ضغط')
        elif action == 'counter_pressing':
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, color='blue', facecolor='none', edgecolor='blue', s=100, label='ضغط عكسي')
        else:
            pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, color='black', label=action, s=80)
            
    plt.legend()
    st.pyplot(fig)
