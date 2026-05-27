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
    st.error("تأكد من وجود ملفات CSV في المستودع")
    st.stop()

# 3. اختيار اللاعب (هنا نحدد player_df)
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
# هذا هو السطر الذي كان مفقوداً في ترتيبك للكود:
player_df = df[df['Player'] == selected_player]

# 4. الحسابات والرسومات
st.markdown('<div class="report-card" style="background:white; padding:20px; border-radius:15px;">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

# الفلترة هنا ستعمل لأننا عرفنا player_df أعلاه
p_data = player_df[player_df['Action'] == 'pressing']
c_data = player_df[player_df['Action'] == 'counter_pressing']

with col1:
    st.subheader(f"تحليل اللاعب: {selected_player}")
    st.metric("إجمالي الضغط (Pressing)", len(p_data))
    st.metric("إجمالي الضغط العكسي (Counter-Pressing)", len(c_data))

with col2:
    st.subheader("خريطة التمركز")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(8, 5))
    
    # الرسم
    pitch.scatter(p_data['X Start']*105, p_data['Y Start']*68, ax=ax, color='red', 
                  facecolor='none', edgecolor='red', s=80, label='ضغط')
    pitch.scatter(c_data['X Start']*105, c_data['Y Start']*68, ax=ax, color='blue', 
                  facecolor='none', edgecolor='blue', s=80, label='ضغط عكسي')
    plt.legend()
    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)
