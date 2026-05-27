import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import glob

# ... (نفس دالة load_all_matches السابقة) ...

# 4. الكارت المحدث (لضمان وضوح الضغط والضغط العكسي)
with st.container():
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("تحليل الأداء التراكمي")
        # حساب كل الضغط والضغط العكسي لكل الماتشات
        p_data = player_df[player_df['Action'] == 'pressing']
        c_data = player_df[player_df['Action'] == 'counter_pressing']
        
        st.metric("إجمالي الضغط (Pressing)", len(p_data))
        st.metric("إجمالي الضغط العكسي (Counter-Pressing)", len(c_data))
        
    with col2:
        st.subheader("توزيع الضغط (أحمر) والضغط العكسي (أزرق)")
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        fig, ax = pitch.draw(figsize=(8, 5))
        
        # رسم الضغط (أحمر مفرغ)
        pitch.scatter(p_data['X Start']*105, p_data['Y Start']*68, ax=ax, color='red', 
                      facecolor='none', edgecolor='red', s=80, label='ضغط', alpha=0.6)
        
        # رسم الضغط العكسي (أزرق مفرغ)
        pitch.scatter(c_data['X Start']*105, c_data['Y Start']*68, ax=ax, color='blue', 
                      facecolor='none', edgecolor='blue', s=80, label='ضغط عكسي', alpha=0.6)
        
        plt.legend(loc='upper right')
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)
