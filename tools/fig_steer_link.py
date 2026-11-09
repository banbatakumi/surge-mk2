#!/usr/bin/env python3
"""図 F-02「モータ角と路面舵角の関係」の SVG を作る（依存なし）。

値は AutonomousCar_RasPi の config/vehicle.toml（[control] steer_link_gain / steer_link_cubic、
2026-10-20 の校正 2）。式: δ = g·x + c·x³、x = 0.5 × モータ角 [rad]。モータの可動域は ±60°。

    python3 tools/fig_steer_link.py > docs/assets/fig/steer_link.svg
"""
import math

G = 1.101158   # steer_link_gain
C = -0.730735  # steer_link_cubic
MOTOR_MAX_DEG = 60.0

W, H = 720, 440
L, R, T, B = 70, 30, 30, 60          # 余白
XMAX, YMAX = 60.0, 32.0              # 軸の範囲 [deg]


def sx(deg):  # モータ角 → x 座標
    return L + (deg + XMAX) / (2 * XMAX) * (W - L - R)


def sy(deg):  # 路面舵角 → y 座標
    return T + (YMAX - deg) / (2 * YMAX) * (H - T - B)


def road_deg(motor_deg):
    x = 0.5 * math.radians(motor_deg)
    return math.degrees(G * x + C * x ** 3)


def path(fn):
    pts = [(m / 10.0, fn(m / 10.0)) for m in range(int(-MOTOR_MAX_DEG * 10), int(MOTOR_MAX_DEG * 10) + 1, 5)]
    return "M" + " L".join(f"{sx(a):.1f},{sy(b):.1f}" for a, b in pts)


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="13">',
       f'<rect width="{W}" height="{H}" fill="#fff" rx="8"/>']
for d in range(-60, 61, 15):  # 縦の目盛り線
    out.append(f'<line x1="{sx(d):.1f}" y1="{T}" x2="{sx(d):.1f}" y2="{H-B}" stroke="#e3e5e8"/>')
    out.append(f'<text x="{sx(d):.1f}" y="{H-B+18}" text-anchor="middle" fill="#555">{d}°</text>')
for d in range(-30, 31, 10):  # 横の目盛り線
    out.append(f'<line x1="{L}" y1="{sy(d):.1f}" x2="{W-R}" y2="{sy(d):.1f}" stroke="#e3e5e8"/>')
    out.append(f'<text x="{L-8}" y="{sy(d)+4:.1f}" text-anchor="end" fill="#555">{d}°</text>')
out.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{W-R}" y2="{sy(0):.1f}" stroke="#999"/>')
out.append(f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{H-B}" stroke="#999"/>')
# 比例（リンク比 0.5）の直線と、校正した換算の曲線
out.append(f'<path d="{path(lambda m: 0.5 * m)}" fill="none" stroke="#8a8f98" stroke-width="2" stroke-dasharray="6 5"/>')
out.append(f'<path d="{path(road_deg)}" fill="none" stroke="#ff6a13" stroke-width="3"/>')
# 最大舵角の点
mx = road_deg(MOTOR_MAX_DEG)
for s in (1, -1):
    out.append(f'<circle cx="{sx(s*MOTOR_MAX_DEG):.1f}" cy="{sy(s*mx):.1f}" r="5" fill="#ff6a13"/>')
out.append(f'<text x="{sx(MOTOR_MAX_DEG)-8:.1f}" y="{sy(mx)+34:.1f}" text-anchor="end" fill="#d4520a">最大 {mx:.1f}°</text>')
# 凡例と軸ラベル
out.append(f'<line x1="{L+16}" y1="{T+16}" x2="{L+46}" y2="{T+16}" stroke="#ff6a13" stroke-width="3"/>'
           f'<text x="{L+52}" y="{T+20}" fill="#222">校正した換算（δ = g·x + c·x³）</text>')
out.append(f'<line x1="{L+16}" y1="{T+38}" x2="{L+46}" y2="{T+38}" stroke="#8a8f98" stroke-width="2" stroke-dasharray="6 5"/>'
           f'<text x="{L+52}" y="{T+42}" fill="#222">比例とした場合（モータ角 × 0.5）</text>')
out.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-14}" text-anchor="middle" fill="#222">ステアリングモータの角度</text>')
out.append(f'<text transform="translate(18,{(T+H-B)/2:.0f}) rotate(-90)" text-anchor="middle" fill="#222">路面舵角（タイヤの向き）</text>')
out.append('</svg>')
print("\n".join(out))
