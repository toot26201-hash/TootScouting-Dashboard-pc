import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# تحميل البيانات مباشرة من ملف موجود في المستودع
df = pd.read_csv('EPS-honka-actions.csv')

st.title("لوحة تحكم TootScouting")

# اختيار اللاعب
player = st.selectbox("اختر اللاعب", df['Player'].dropna().unique())

# عرض إحصائية سريعة
player_data = df[df['Player'] == player]
st.write(f"عدد التحركات المسجلة للاعب: {len(player_data)}")

# رسم الملعب
pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100)
fig, ax = pitch.draw()
pitch.scatter(player_data['X Start'] * 100, player_data['Y Start'] * 100, ax=ax, color='red')
st.pyplot(fig)
