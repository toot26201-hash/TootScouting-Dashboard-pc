import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob

# 1. إعداد الصفحة
st.set_page_config(layout="wide")
st.title("⚽ TootScouting: لوحة تحليل الموسم الاحترافية")

# 2. تحميل ودمج البيانات
@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    # الأعمدة المطلوبة
    required_cols = ['Player', 'Action', 'X Start', 'Y Start']
    
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            if all(col in temp_df.columns for col in required_cols):
                temp_df = temp_df.dropna(subset=required_cols)
                df_list.append(temp_df)
        except: continue
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

if df.empty:
    st.error("تأكد من وجود ملفات CSV في المستودع.")
    st.stop()

# 3. القائمة الجانبية (الأزرار والفلتر)
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().unique()))
player_df = df[df['Player'] == selected_player]

st.sidebar.subheader("تحليل الأداء")
selected_actions = st.sidebar.multiselect(
    "اختر أنواع البيانات:",
    options=sorted(df['Action'].unique()),
    default=['pressing', 'counter_pressing']
)

# 4. الكارت
st.markdown("""<style>.card { background: white; padding: 30px; border-radius: 20px; border: 2px solid #e0e0e0; }</style>""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(f"بيانات: {selected_player}")
        for action in selected_actions:
            count = len(player_df[player_df['Action'] == action])
            st.metric(f"إجمالي {action}", count)
            
    with col2:
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(10, 6))
        
        # ألوان لكل نوع
        colors = {'pressing': 'red', 'counter_pressing': 'blue', 'progressive_pass': 'green', 'progressive_run': 'purple'}
        
        for action in selected_actions:
            data = player_df[player_df['Action'] == action]
            color = colors.get(action, 'black')
            
            # رسم أسهم إذا توفرت نقاط النهاية، وإلا دوائر
            if 'X End' in data.columns:
                pitch.arrows(data['X Start']*105, data['Y Start']*68, 
                             data['X End']*105, data['Y End']*68, ax=ax, color=color, label=action)
            else:
                pitch.scatter(data['X Start']*105, data['Y Start']*68, ax=ax, color=color, 
                              facecolor='none', edgecolor=color, s=100, label=action)
        
        plt.legend(loc='upper right')
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
