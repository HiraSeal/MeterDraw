import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
color1 = 'black'
color2 = 'dimgray'
color4 = 'lightgray'
# ---- サブルーチン ----
def draw_label(ax, angle_rad, value, radius=1.05*0.7, fontsize=14):
    """指定した角度と値でラベルを描く"""
    x = radius * np.cos(angle_rad) 
    y = radius * np.sin(angle_rad) 
    ax.text(x, y, str(value), ha='center', va='center', fontsize=fontsize)

# ---- パラメータ設定 ----
num_black = 12
num_grey = 11
total = num_black + num_grey
angle_start_deg = 195 - 7.5
angle_end_deg = -15 - 7.5
angles = np.linspace(np.radians(angle_start_deg), np.radians(angle_end_deg), total)

black_width = 3.0
grey_width = 1.5
black_r_start = 0.83
black_r_end = 1.0
grey_r_start = 0.88
grey_r_end = 1.0

# 黒線に付ける数値（例：20刻みで 20~240）
black_labels = list(range(20, 261, 20)) 

# ---- 描画開始 ----
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.axis('off')

label_index = 0  # 黒ラベル用インデックス

for i, angle in enumerate(angles):
    if i % 2 == 0:
        r0, r1 = black_r_start, black_r_end
        color = color1
        width = black_width

        # 黒線を描画
        x0 = r0 * np.cos(angle)
        y0 = r0 * np.sin(angle)
        x1 = r1 * np.cos(angle)
        y1 = r1 * np.sin(angle)
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=width)

        # 数字を描く
        draw_label(ax, angle, black_labels[label_index])
        label_index += 1
    else:
        r0, r1 = grey_r_start, grey_r_end
        color = color2
        width = grey_width
        x0 = r0 * np.cos(angle)
        y0 = r0 * np.sin(angle)
        x1 = r1 * np.cos(angle)
        y1 = r1 * np.sin(angle)
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=width)

# 追加黒線（例：最初の角度 + 15°）
extra_angle_deg = angle_start_deg + 15
extra_angle_rad = np.radians(extra_angle_deg)
x0 = black_r_start * np.cos(extra_angle_rad)
y0 = black_r_start * np.sin(extra_angle_rad)
x1 = black_r_end * np.cos(extra_angle_rad)
y1 = black_r_end * np.sin(extra_angle_rad)
ax.plot([x0, x1], [y0, y1], color='black', linewidth=black_width)
draw_label(ax, extra_angle_rad, 0)

ax.plot(0, 0, 'ko', markersize=6)


# 円の半径と太さの設定
circle_radius = 1.04  # メーター目盛の外側ギリギリに合わせる
circle_width = 1.0    # 線の太さ

# 円を描画（中心0,0）
circle = patches.Circle((0, 0), radius=circle_radius, fill=False, 
                        edgecolor=color4, linewidth=circle_width)

# 軸に追加
ax.add_patch(circle)
ax.text(0, 0.25, "Speed", ha='center', va='center', fontsize=20, fontweight='bold',fontname='Times New Roman', fontstyle='italic' )
ax.text(0, -0.2, "km/h", ha='center', va='center', fontsize=14)

plt.savefig("spdeter.png", dpi=300)
plt.show()
