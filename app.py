import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import glob

# 1. تحميل كل الماتشات ودمجها
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = [pd.read_csv(f) for f in all_files]
    return pd.concat(df_list, axis=0, ignore_index=True)

df = load_all_matches()

# 2. الفلاتر
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].unique()))
player_df = df[df['Player'] == selected_player]

# 3. رسم خريطة الضغط التراكمية (لكل الماتشات)
st.title(f"خريطة الضغط التراكمية: {selected_player}")
st.write("هذه الخريطة توضح مناطق تمركز الضغط للاعب في جميع المباريات المسجلة.")

pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
fig, ax = pitch.draw(figsize=(10, 7))

# استخراج بيانات الضغط والضغط العكسي معاً
all_press = player_df[player_df['Action'].isin(['pressing', 'counter_pressing'])]

# رسم الخريطة الحرارية (Heatmap) بدلاً من النقاط، لأنها أفضل لتجميع الماتشات
if not all_press.empty:
    sns.kdeplot(x=all_press['X Start'] * 105, y=all_press['Y Start'] * 68, 
                fill=True, cmap='Reds', thresh=0.1, levels=20, ax=ax, alpha=0.6)

st.pyplot(fig)
