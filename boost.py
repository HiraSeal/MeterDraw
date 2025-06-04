import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ---- パラメータ設定 ----
# メーターの値範囲と刻み
tick_values = np.arange(-1.0, 2.01, 0.1)       # 0.1刻み
major_values = np.arange(-1.0, 2.01, 0.5)      # 0.5刻み（太線＋ラベル）

# 線の長さ・太さ
major_r_start = 0.82 # 太線の開始半径
major_r_end   = 1.0  # 太線の終了半径
minor_r_start = 0.88 # 細線の開始半径
minor_r_end   = 1.0  # 細線の終了半径
label_radius  = 0.7  # ラベルの半径
major_width   = 3.0  # 太線の太さ
minor_width   = 1.0  # 細線の太さ

# 帯用の設定
inner_radius = major_r_start # 帯の内側半径
outer_radius = major_r_end   # 帯の外側半径
angle_offset = 0  # このメーターはvalue_to_angleで既に正しい角度変換済み

# 色設定
color1 = 'black' # 太線の色
color2 = 'dimgray' # 細線の色
color3 = 'red' # 赤帯範囲の線の色(tachometer.pyでは使用)
color4 = 'lightgray' # 外周円の色
color_band1 = 'gold' # 黄色帯（0.0〜1.0）
color_band2 = 'red'  # 赤帯（1.0〜2.0）

# 角度に応じたラベルの記載関数
def draw_label(ax, angle_rad, label, radius=0.7, fontsize=12):
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)

    if np.isclose(label, 0.0):
        label_text = "0.0" # 0.0は特別に表示(-0.0となるのを回避)
    else:
        label_text = f"{label:.1f}"
    ax.text(x, y, label_text, ha='center', va='center', fontsize=fontsize)

# Boost計: 値 → 角度への変換（−1.0 → 270°, 0.0 → 180°, 1.0 → 90°, 2.0 → 0°）
def value_to_angle(v):
    return 270 - ((v + 1.0) / 3.0) * 270  # 範囲3.0を270度にマッピング

# 帯を描画する関数
def add_colored_band(ax, start_val, end_val, color):
    theta1 = value_to_angle(start_val) + angle_offset
    theta2 = value_to_angle(end_val) + angle_offset
    if theta1 > theta2:
        theta1, theta2 = theta2, theta1  # Wedgeは反時計回り描画なので順序調整

    wedge = patches.Wedge(center=(0, 0),
                          r=outer_radius * 1.01,  # 少し外側に出すと見映えが良い
                          theta1=theta1,
                          theta2=theta2,
                          width=outer_radius - inner_radius,
                          facecolor=color,
                          edgecolor='none',
                          alpha=0.5)
    ax.add_patch(wedge)

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

# 線＆ラベルを描画
for v in tick_values:
    angle = value_to_angle(v)
    if round(v * 10) % 5 == 0:  # 太線
        draw_tick(angle, major_r_start, major_r_end, color1, major_width)
        draw_label(ax, np.radians(angle), v, radius=label_radius)
    else:  # 細線
        draw_tick(angle, minor_r_start, minor_r_end, color2, minor_width)

# 中心点
ax.plot(0, 0, 'ko', markersize=4)

# 外周円
circle = patches.Circle((0, 0), radius=1.04, fill=False, edgecolor=color4, linewidth=1.0)
ax.add_patch(circle)

# 黄色帯（0.0〜1.0）
add_colored_band(ax, 0.0, 1.0, color_band1)

# 赤帯（1.0〜2.0）
add_colored_band(ax, 2.0, 1.0, color_band2)

# 中央ラベル
ax.text(0, -0.2, "bar", ha='center', va='center', fontsize=14)
ax.text(0, 0.25, "BOOST", ha='center', va='center', fontsize=20, fontweight='bold',fontname='Times New Roman', fontstyle='italic' )

# 表示
plt.savefig("boostmeter.png", dpi=300)
plt.show()
