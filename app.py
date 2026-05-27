import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide")
st.title("TootScouting: تحليل تكتيكي")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv('EPS-honka-actions.csv')

df = load_data()
player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == player]

# --- رسم الملعب بأبعاد طبيعية وخلفية بيضاء ---
# 1. إعداد الملعب (بدون figsize هنا)
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')

# 2. رسم الملعب (نحدد الـ figsize هنا)
fig, ax = pitch.draw(figsize=(10, 6))

# رسم نقاط الضغط (أحمر مفرغ)
press = player_df[player_df['Action'] == 'pressing']
pitch.scatter(press['X Start'] * 105, press['Y Start'] * 68, 
              ax=ax, color='red', facecolor='none', edgecolor='red', s=100, label='ضغط')

# رسم نقاط الضغط العكسي (أزرق مفرغ)
counter = player_df[player_df['Action'] == 'counter_pressing']
pitch.scatter(counter['X Start'] * 105, counter['Y Start'] * 68, 
              ax=ax, color='blue', facecolor='none', edgecolor='blue', s=100, label='ضغط عكسي')

plt.legend()
st.pyplot(fig)
