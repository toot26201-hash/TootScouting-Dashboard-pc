import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import glob

# 1. إعداد الصفحة
st.set_page_config(layout="wide", page_title="TootScouting Season Analysis")
st.title("⚽ TootScouting: لوحة تحليل الموسم الكامل")

# 2. تحميل ودمج كافة ملفات الـ CSV من المستودع
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    required_cols = ['Player', 'Action', 'X Start', 'Y Start']
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            # التأكد أن الملف يحتوي على الأعمدة المطلوبة
            if all(col in temp_df.columns for col in required_cols):
                temp_df = temp_df.dropna(subset=required_cols)
                df_list.append(temp_df)
        except:
            continue
            
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV صالحة في المستودع. تأكد من رفع ملفات المباريات.")
    st.stop()

# 3. اختيار اللاعب (مع التنظيف)
players = sorted([str(p) for p in df['Player'].dropna().unique()])
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

# 4. الكارت الاحترافي
st.markdown("""
<style>
    .report-card { background-color: white; padding: 30px; border-radius: 20px; border: 2px solid #e0e0e0; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"إحصائيات: {selected_player}")
        press = len(player_df[player_df['Action'] == 'pressing'])
        counter = len(player_df[player_df['Action'] == 'counter_pressing'])
        
        st.metric("إجمالي الضغط (الموسم)", press)
        st.metric("إجمالي الضغط العكسي (الموسم)", counter)
        
    with col2:
        st.subheader("خريطة التمركز (كل المباريات)")
        # ملعب بأبعاد طبيعية وخلفية بيضاء
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(8, 5))
        
        # رسم البيانات (دوائر مفرغة)
        p_data = player_df[player_df['Action'] == 'pressing']
        c_data = player_df[player_df['Action'] == 'counter_pressing']
        
        pitch.scatter(p_data['X Start']*105, p_data['Y Start']*68, ax=ax, color='red', 
                      facecolor='none', edgecolor='red', s=100, label='ضغط')
        pitch.scatter(c_data['X Start']*105, c_data['Y Start']*68, ax=ax, color='blue', 
                      facecolor='none', edgecolor='blue', s=100, label='ضغط عكسي')
        
        plt.legend(loc='upper right')
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
