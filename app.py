import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob
import os

st.set_page_config(layout="wide")
st.title("TootScouting: لوحة تحليل الموسم")

@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv") + glob.glob("*.xlsx")
    df_list = []
    
    # قائمة للملفات التي فشلت في التحميل للتشخيص
    failed_files = []
    
    for f in all_files:
        try:
            if f.endswith('.csv'):
                temp_df = pd.read_csv(f)
            else:
                temp_df = pd.read_excel(f)
            
            temp_df['Match_Name'] = os.path.basename(f)
            df_list.append(temp_df)
        except Exception as e:
            failed_files.append(f"{os.path.basename(f)}: {str(e)}")
            continue
            
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame(), failed_files

df, errors = load_all_matches()

# عرض أخطاء التحميل في الشريط الجانبي
if errors:
    st.sidebar.error("ملفات بها مشاكل:")
    for err in errors:
        st.sidebar.write(err)

if df.empty:
    st.error("لم يتم العثور على أي بيانات.")
    st.stop()

# تنظيف البيانات
df['Player'] = df['Player'].fillna("Unknown").astype(str).str.strip()

# اختيار اللاعب
players = sorted(df['Player'].unique().tolist())
selected_player = st.sidebar.selectbox("اختر اللاعب:", players)
player_df = df[df['Player'] == selected_player]

# اختيار المباريات
all_matches = sorted(player_df['Match_Name'].unique())
selected_matches = st.sidebar.multiselect("اختر المباريات:", all_matches, default=all_matches)
final_df = player_df[player_df['Match_Name'].isin(selected_matches)]

# عرض الإحصائيات (بقية الكود كما هو...)
# ...
