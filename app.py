import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(layout="wide")
st.title("⚽ TootScouting: تشخيص داتا الموسم")

@st.cache_data
def load_all_matches():
    all_files = glob.glob("*.csv")
    df_list = []
    for f in all_files:
        try:
            temp_df = pd.read_csv(f)
            temp_df['Match_Name'] = os.path.basename(f)
            df_list.append(temp_df)
        except: continue
    return pd.concat(df_list, axis=0, ignore_index=True) if df_list else pd.DataFrame()

df = load_all_matches()

# عرض قائمة بكل اللاعبين المكتشفين في كل الملفات
st.sidebar.subheader("فحص البيانات المكتشفة:")
st.sidebar.write("قائمة اللاعبين في كل الملفات:", df['Player'].unique().tolist())

# الفلترة
selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(df['Player'].dropna().astype(str).unique()))
player_df = df[df['Player'] == selected_player]

# عرض المباريات المتاحة لهذا اللاعب فقط
st.sidebar.subheader("المباريات المتاحة لهذا اللاعب:")
available_matches = player_df['Match_Name'].unique()
st.sidebar.write(available_matches)

selected_matches = st.sidebar.multiselect("اختر المباريات:", available_matches, default=available_matches)
final_df = player_df[player_df['Match_Name'].isin(selected_matches)]

# عرض الإحصائيات
st.write(f"تحليل اللاعب: {selected_player}")
st.write(f"عدد المباريات المدمجة: {len(selected_matches)}")
st.dataframe(final_df)
