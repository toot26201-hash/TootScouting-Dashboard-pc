import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم")

@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            # إضافة اسم الملف كعمود للمباراة
            temp_df['Match_Name'] = os.path.basename(f)
            df_list.append(temp_df)
        except:
            continue
            
    # دمج الملفات حتى لو كانت الأعمدة مختلفة (سيضع قيم فارغة حيث لا يوجد عمود)
    if df_list:
        return pd.concat(df_list, axis=0, ignore_index=True)
    return pd.DataFrame()

df = load_all_matches()

# التأكد من وجود الأعمدة بعد الدمج (بفرض أن أسماء الأعمدة موحدة في أغلب الملفات)
# إذا كانت الأعمدة تختلف، ستحتاج لتوحيدها أولاً في ملفات الـ CSV الخاصة بك
st.sidebar.write("الملفات المدمجة:", df['Match_Name'].unique())

# اختيار اللاعب
if 'Player' in df.columns:
    selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
    player_df = df[df['Player'] == selected_player]
    
    # اختيار المباريات
    all_matches = sorted(player_df['Match_Name'].unique())
    selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)
    player_df = player_df[player_df['Match_Name'].isin(selected_matches)]
    
    # الرسم
    if not player_df.empty:
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(8, 5))
        # ... (بقية كود الرسم)
