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
    return pd.concat(df_list, axis=0, ignore_index=True)

df = load_all_matches()

# 2. الفلترة التراكمية (الموسم كله أو اختيار مباريات محددة)
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].unique()))
player_df = df[df['Player'] == selected_player]

# اختيار المباريات (لتحليل مباريات معينة من الموسم)
st.sidebar.subheader("فلتر المباريات")
if 'Match_ID' in player_df.columns:
    matches = st.sidebar.multiselect("اختر المباريات للتحليل:", player_df['Match_ID'].unique(), default=player_df['Match_ID'].unique())
    player_df = player_df[player_df['Match_ID'].isin(matches)]

# 3. عرض الإحصائيات التراكمية
st.title(f"تحليل أداء {selected_player} التراكمي")
col1, col2 = st.columns(2)

# حساب الإحصائيات لكل الأكشنز الموجودة
actions = player_df['Action'].unique()
for action in actions:
    count = len(player_df[player_df['Action'] == action])
    col1.metric(f"إجمالي {action}", count)

# 4. خريطة التمركز لجميع المباريات المختارة
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
fig, ax = pitch.draw(figsize=(8, 5))

for action in actions:
    data = player_df[player_df['Action'] == action]
    # رسم الدوائر للضغط (أحمر) والضغط العكسي (أزرق)
    if action == 'pressing':
        pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, color='red', facecolor='none', edgecolor='red', s=80, label='الضغط')
    elif action == 'counter_pressing':
        pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, color='blue', facecolor='none', edgecolor='blue', s=80, label='الضغط العكسي')

plt.legend()
st.pyplot(fig)
