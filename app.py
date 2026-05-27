import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob

# 1. إعداد الصفحة
st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم الكامل")

# 2. تحميل البيانات
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = [pd.read_csv(f) for f in all_files]
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV.")
    st.stop()

# 3. اختيار اللاعب
players = sorted([str(p) for p in df['Player'].dropna().unique()])
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

# 4. اختيار أنواع البيانات (الكود المصحح)
all_actions = sorted(df['Action'].dropna().unique())
default_actions = [a for a in ['pressing', 'counter_pressing'] if a in all_actions]

st.sidebar.subheader("تحليل الأداء")
selected_actions = st.sidebar.multiselect(
    "اختر أنواع البيانات:",
    options=all_actions,
    default=default_actions
)

# 5. عرض الكارت
st.markdown('<div class="report-card" style="background:white; padding:30px; border-radius:20px; border:2px solid #e0e0e0;">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"بيانات: {selected_player}")
    for action in selected_actions:
        st.metric(f"إجمالي {action}", len(player_df[player_df['Action'] == action]))

with col2:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(8, 5))
    
    # رسم البيانات المختار فقط
    for action in selected_actions:
        data = player_df[player_df['Action'] == action]
        if not data.empty:
            if 'X End' in data.columns:
                pitch.arrows(data['X Start']*105, data['Y Start']*68, data['X End']*105, data['Y End']*68, ax=ax, label=action)
            else:
                pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, s=80, label=action)
    plt.legend()
    st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)
