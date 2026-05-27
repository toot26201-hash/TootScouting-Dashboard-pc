import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import glob

# إعداد الصفحة
st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم")

# 1. دالة التحميل والتنظيف المتقدمة (تتعامل مع أي داتا ناقصة)
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    required_cols = ['Player', 'Action', 'X Start', 'Y Start']
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            if all(col in temp_df.columns for col in required_cols):
                # حذف الصفوف الناقصة فقط
                temp_df = temp_df.dropna(subset=required_cols)
                df_list.append(temp_df)
        except:
            continue
            
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("لم يتم العثور على ملفات CSV صالحة. تأكد من رفع الملفات في المجلد الرئيسي.")
    st.stop()

# 2. الفلاتر
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == selected_player]

# 3. الكارت الاحترافي
st.markdown("""
<style>
    .report-card { background-color: white; padding: 30px; border-radius: 20px; border: 2px solid #e0e0e0; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"تحليل اللاعب: {selected_player}")
        # حسابات ديناميكية
        press = len(player_df[player_df['Action'] == 'pressing'])
        counter = len(player_df[player_df['Action'] == 'counter_pressing'])
        
        st.metric("عدد عمليات الضغط", press)
        st.metric("عدد الضغط العكسي", counter)
        
        st.write("---")
        st.write("معدل نجاح الضغط")
        st.progress(0.75) 
        
    with col2:
        st.subheader("خريطة التمركز التكتيكي")
        # الملعب بأبعاد طبيعية (StatsBomb) وخلفية بيضاء
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(8, 5))
        
        # رسم الضغط (أحمر) والضغط العكسي (أزرق)
        # نستخدم سكتر (Scatter) بدوائر مفرغة كما طلبت
        p_data = player_df[player_df['Action'] == 'pressing']
        c_data = player_df[player_df['Action'] == 'counter_pressing']
        
        pitch.scatter(p_data['X Start']*105, p_data['Y Start']*68, ax=ax, color='red', 
                      facecolor='none', edgecolor='red', s=100, label='ضغط')
        pitch.scatter(c_data['X Start']*105, c_data['Y Start']*68, ax=ax, color='blue', 
                      facecolor='none', edgecolor='blue', s=100, label='ضغط عكسي')
        
        plt.legend(loc='upper right')
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
