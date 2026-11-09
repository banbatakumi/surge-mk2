#!/usr/bin/env python3
"""図 F-05「センサの配置図」の SVG を作る。

背景は 3D モデル（docs/assets/3d/car.glb）を真上から正射影で描いた PNG（tools/cad/ortho.html で作る）。
画素と座標の対応: px = (X1 - X) * PXM、py = (Z1 - Z) * PXM（モデル座標 X=左, Z=前、単位 m）。
センサの位置は 3D モデルの部品の中心。vehicle.toml の取付位置（後車軸の中心が原点）とも一致を確認済み。
画角はカメラが vehicle.toml の undistort_hfov（補正後 1.92 rad ≈ 110°）。超音波は指向角の資料が無いので向きだけ描く。

    python3 tools/fig_sensor_layout.py top.png > docs/assets/fig/sensor_layout.svg
"""
import base64
import math
import sys

X0, X1, Z0, Z1, PXM = -0.13, 0.13, -0.235, 0.225, 3000
IMG_W, IMG_H = round((X1 - X0) * PXM), round((Z1 - Z0) * PXM)
MARGIN = 330                       # 左右のラベル用の余白 [px]
W, H = IMG_W + 2 * MARGIN, IMG_H + 40
ORANGE, BLUE, GREEN, PURPLE, INK = "#ff6a13", "#2f7de1", "#1f9d55", "#8b5cf6", "#222"


def px(x, z):
    return MARGIN + (X1 - x) * PXM, 20 + (Z1 - z) * PXM


def fan(x, z, heading_deg, fov_deg, r_m, color):
    cx, cy = px(x, z)
    r = r_m * PXM
    a0, a1 = math.radians(heading_deg - fov_deg / 2), math.radians(heading_deg + fov_deg / 2)
    # heading 0° = 前（画像の上）、時計回りを正
    p0 = (cx + r * math.sin(a0), cy - r * math.cos(a0))
    p1 = (cx + r * math.sin(a1), cy - r * math.cos(a1))
    large = 1 if fov_deg > 180 else 0
    return (f'<path d="M{cx:.1f},{cy:.1f} L{p0[0]:.1f},{p0[1]:.1f} A{r:.1f},{r:.1f} 0 {large} 1 {p1[0]:.1f},{p1[1]:.1f} Z" '
            f'fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-width="2"/>')


def dot(x, z, color, r=7):
    cx, cy = px(x, z)
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}" stroke="#fff" stroke-width="2.5"/>'


def label(x, z, side, y_px, title, sub, color):
    """部品 (x, z) から、左右の余白の y_px へ引き出し線を引いてラベルを置く。"""
    cx, cy = px(x, z)
    tx = 24 if side == "left" else W - 24
    ex = MARGIN - 20 if side == "left" else MARGIN + IMG_W + 20
    anchor = "start" if side == "left" else "end"
    return (f'<polyline points="{cx:.1f},{cy:.1f} {ex:.1f},{y_px:.1f} {tx + (0 if side == "left" else 0):.1f},{y_px:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="2"/>'
            f'<text x="{tx}" y="{y_px - 10:.1f}" text-anchor="{anchor}" font-size="26" font-weight="700" fill="{INK}">{title}</text>'
            f'<text x="{tx}" y="{y_px + 26:.1f}" text-anchor="{anchor}" font-size="21" fill="#555">{sub}</text>')


def main():
    png = base64.b64encode(open(sys.argv[1], "rb").read()).decode()
    lidar = (0.0, -0.0475)
    cam_f, cam_r = (0.0, -0.0148), (0.0, -0.0802)
    us_f, us_r = (0.0, 0.1372), (0.0, -0.1472)
    enc_l, enc_r = (0.0536, 0.1150), (-0.0536, 0.1150)
    board = (0.010, 0.0205)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">',
           f'<rect width="{W}" height="{H}" fill="#fff" rx="16"/>',
           f'<image x="{MARGIN}" y="20" width="{IMG_W}" height="{IMG_H}" href="data:image/png;base64,{png}"/>']
    # 視野
    out.append(fan(*cam_f, 0, 110, 0.085, BLUE))
    out.append(fan(*cam_r, 180, 110, 0.085, BLUE))
    cx, cy = px(*lidar)
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{0.105 * PXM:.1f}" fill="{ORANGE}" fill-opacity="0.08" '
               f'stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="10 8"/>')
    for (x, z), d in ((us_f, 1), (us_r, -1)):  # 超音波は向きだけ
        sx, sy = px(x, z)
        out.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{sx:.1f}" y2="{sy - d * 70:.1f}" stroke="{GREEN}" stroke-width="5" '
                   f'marker-end="url(#arr)"/>')
    out.insert(1, f'<defs><marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
                  f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker></defs>')
    # 点
    for p, c in ((lidar, ORANGE), (cam_f, BLUE), (cam_r, BLUE), (us_f, GREEN), (us_r, GREEN), (enc_l, PURPLE), (enc_r, PURPLE), (board, INK)):
        out.append(dot(*p, c))
    # ラベル（左右の余白）
    out.append(label(*us_f, "right", 120, "超音波（前）", "RCW-0001", GREEN))
    out.append(label(*enc_l, "left", 340, "前輪の角度センサ", "AS5600（左右）", PURPLE))
    out.append(label(*enc_r, "right", 340, "前輪の角度センサ", "AS5600（左右）", PURPLE))
    out.append(label(*cam_f, "right", 620, "前方カメラ", "IMX219・補正後 約110°", BLUE))
    out.append(label(*board, "left", 640, "メイン基板", "IMU（MPU6050）を搭載", INK))
    out.append(label(*lidar, "left", 900, "LiDAR", "LD06・360°・10 Hz", ORANGE))
    out.append(label(*cam_r, "right", 900, "後方カメラ", "IMX219・補正後 約110°", BLUE))
    out.append(label(*us_r, "right", 1240, "超音波（後）", "RCW-0001", GREEN))
    # 方位
    ax, ay = MARGIN + IMG_W / 2, 6
    out.append(f'<text x="{W - 24}" y="{H - 20}" text-anchor="end" font-size="20" fill="#777">上が車の前</text>')
    out.append('</svg>')
    print("\n".join(out))


if __name__ == "__main__":
    main()
