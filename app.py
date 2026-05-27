import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# إعداد الصفحة
st.set_page_config(layout="wide")
st.title("TootScouting: تحليل تكتيكي")

# تحميل البيانات
df = pd.read_csv('EPS-honka-actions.csv')
player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == player]

# --- رسم الملعب بأبعاد طبيعية وخلفية بيضاء ---
# استخدمنا 'statsbomb' لأنها تضبط أبعاد الملعب الطبيعية (105x68)
# pitch_color='white' للخلفية البيضاء
# line_color='black' لظهور الخطوط بوضوح على الأبيض
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black', figsize=(10, 6))
fig, ax = pitch.draw()

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
