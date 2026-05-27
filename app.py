import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import glob

# إعداد الصفحة
st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم")

@st.cache_data
def load_all_matches():
    # البحث عن ملفات CSV في المجلد الحالي مباشرة
    all_files = glob.glob("*.csv")
    
    if not all_files:
        return pd.DataFrame()
    
    df_list = [pd.read_csv(f) for f in all_files]
    return pd.concat(df_list, axis=0, ignore_index=True)

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على أي ملفات CSV في المستودع. تأكد من رفعها!")
    st.stop()

# الفلاتر
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == selected_player]

# --- تصميم الكارت ---
st.markdown("""
<style>
    .report-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e0e0e0; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"تحليل {selected_player}")
        press = len(player_df[player_df['Action'] == 'pressing'])
        st.metric("إجمالي الضغط", press)
        
        st.write("معدل الأداء")
        st.progress(0.8) 
        
    with col2:
        st.subheader("كثافة الأداء عبر الموسم")
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(6, 4))
        
        data_to_plot = player_df[player_df['Action'].isin(['pressing', 'counter_pressing'])]
        if not data_to_plot.empty:
            sns.kdeplot(x=data_to_plot['X Start']*105, y=data_to_plot['Y Start']*68, 
                        fill=True, cmap='viridis', levels=10, ax=ax)
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
