import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 色定数
color1 = 'black' # 太線の色
color2 = 'dimgray' # 細線の色
color3 = 'red' # 赤帯範囲の線の色(tachometer.pyでは使用)
color4 = 'lightgray' # 外周円の色
color_band1 = 'gold' # 黄色帯（boost.pyでは使用）
color_band2 = 'red' # 赤帯（7〜9）

# ---- パラメータ設定 ----
major_values = list(range(0, 10))        # 0〜9 (黒太線+数字)
minor_values = [v + 0.5 for v in range(9)]  # 0.5〜8.5 (細線)
red_values   = [7, 8, 9]                 # レッドゾーン (赤線)

angle_start_deg = 210 # 開始角度（210度）
angle_end_deg = -30 # 終了角度（-30度）
angle_range = angle_start_deg - angle_end_deg  # 240度
unit_angle = angle_range / (len(major_values) - 1) # 1目盛りの角度

# 線の長さ
major_r_start = 0.8 # 太線の開始半径
major_r_end = 1.0 # 太線の終了半径
minor_r_start = 0.88 # 細線の開始半径
minor_r_end = 1.0 # 細線の終了半径
label_radius = 0.7 # ラベルの半径  

# 太さ
major_width = 3.0 # 太線の太さ 
minor_width = 1.0 # 細線の太さ
red_width   = major_width # 赤線の太さ

# レッドゾーン、イエローゾーン帯の設定
red_zone_start_val = 7 # レッドゾーン開始値 
red_zone_end_val = 9 # レッドゾーン終了値
yellow_zone_start_val = 5 # イエローゾーン開始値
yellow_zone_end_val = 7 # イエローゾーン終了値
inner_radius = major_r_start # 帯の内側半径
outer_radius = major_r_end # 帯の外側半径


# 角度に応じたラベルの記載関数
def draw_label(ax, angle_rad, label, radius=0.7, fontsize=14):
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    ax.text(x, y, str(label), ha='center', va='center', fontsize=fontsize)

# タコメーター：値 → 角度への変換
def value_to_angle(v):
    return angle_start_deg - v * unit_angle

# 目盛り線描画関数
def draw_tick(angle_deg, r0, r1, color, width):
    angle_rad = np.radians(angle_deg)
    x0 = r0 * np.cos(angle_rad)
    y0 = r0 * np.sin(angle_rad)
    x1 = r1 * np.cos(angle_rad)
    y1 = r1 * np.sin(angle_rad)
    ax.plot([x0, x1], [y0, y1], color=color, linewidth=width)

# ---- 描画開始 ----
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal') # アスペクト比を1:1に設定
ax.axis('off') # 軸を非表示にする

# major（黒線＋数字）
for i, v in enumerate(major_values):
    angle = angle_start_deg - i * unit_angle
    draw_tick(angle, major_r_start, major_r_end, color1, major_width)
    draw_label(ax, np.radians(angle), v, radius=label_radius)

# minor（細グレー線）
for v in minor_values:
    i = v
    angle = angle_start_deg - (i * unit_angle)
    draw_tick(angle, minor_r_start, minor_r_end, color2, minor_width)

# red zone（太赤線）
for v in red_values:
    i = v
    angle = angle_start_deg - (i * unit_angle)
    draw_tick(angle, major_r_start, major_r_end, color3, red_width)

# 中心点
ax.plot(0, 0, 'ko', markersize=4)

# 外周円
circle = patches.Circle((0, 0), radius=1.04, fill=False, edgecolor=color4, linewidth=1.0)
ax.add_patch(circle)

# 扇形（Wedge）でレッドゾーン、イエローゾーンを描く
red_wedge = patches.Wedge(center=(0, 0),
                          r=outer_radius*1.01,
                          theta1=value_to_angle(red_zone_end_val),
                          theta2=value_to_angle(red_zone_start_val) ,
                          width=outer_radius - inner_radius,
                          facecolor=color_band2,
                          edgecolor='none',
                          alpha=0.5)
ax.add_patch(red_wedge)

yellow_wedge = patches.Wedge(center=(0, 0),
                          r=outer_radius*1.01,
                          theta1=value_to_angle(yellow_zone_end_val),
                          theta2=value_to_angle(yellow_zone_start_val) ,
                          width=outer_radius - inner_radius,
                          facecolor=color_band1,
                          edgecolor='none',
                          alpha=0.5)
ax.add_patch(yellow_wedge)

# 中央ラベル
ax.text(0, -0.2, "×1000 r/min", ha='center', va='center', fontsize=14)
ax.text(0, 0.25, "Engine", ha='center', va='center', fontsize=20, fontweight='bold',fontname='Times New Roman', fontstyle='italic' )

plt.savefig("tachometer.png", dpi=300)
plt.show()
