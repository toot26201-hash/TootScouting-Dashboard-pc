from mplsoccer import Pitch

# استخدام pitch_type='statsbomb' هو المعيار الأفضل للبيانات التي إحداثياتها من 0 إلى 1
# إذا كانت بياناتك لا تتبع Statsbomb، استخدم custom وحدد الأبعاد بدقة
pitch = Pitch(
    pitch_type='statsbomb', 
    pitch_color='#22312b', # لون العشب الداكن الاحترافي
    line_color='#c7d5cc',  # لون الخطوط الفاتح
    stripe=True            # لإضافة شكل العشب المخطط (الاحترافي)
)

fig, ax = pitch.draw(figsize=(10, 7))

# الآن، بما أن بياناتك بين 0 و 1، سنقوم بضربها في 100 
# (لأن mplsoccer يحولها تلقائياً لمساحة الملعب عند استخدام statsbomb)
pitch.scatter(player_df['X Start'] * 100, player_df['Y Start'] * 100, 
              ax=ax, color='#ff0000', s=100, alpha=0.7)
