#!/usr/bin/env python3
"""図「向きをずらす拡張」の SVG を作る（模倣学習のページ）。

入力は AutonomousCar_RasPi の `ml_cam_e2e/yaw_aug.py` で作った絵（学習と同じ関数・同じ切り落とし）:
  p-4.jpg / p+0.jpg / p+4.jpg  … 向きを ψ = −4°, 0°, +4° ずらした窓
  mask.jpg                     … 推定した車体マスク（紫）を重ねた絵
  meta.json                    … fx・ずらした画素数・補正後の舵 δ' = δ − k·ψ

    python3 tools/fig_yaw_aug.py <その 5 ファイルのフォルダ> > docs/assets/fig/yaw_aug.svg
"""
import base64
import json
import math
import sys
from pathlib import Path

d = Path(sys.argv[1])
meta = json.loads((d / "meta.json").read_text())
IW, IH = 560, round(560 * meta["h"] / meta["w"])
GAP, M = 24, 24
W = M * 2 + IW * 3 + GAP * 2
ROW1 = 70
H1 = ROW1 + IH + 96
MASK_W = 380
MASK_H = round(MASK_W * meta["h"] / meta["w"])
H = H1 + MASK_H + 70
ORANGE, INK, SUB = "#d4520a", "#222", "#555"


def img(name, x, y, w, h):
    b = base64.b64encode((d / name).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/jpeg;base64,{b}"/>'


def deg_txt(rad):
    v = math.degrees(rad)
    return f'{"右" if v < 0 else "左"} {abs(v):.1f}°'


lab = {int(k): v for k, v in meta["labels"].items()}
base = lab[0]
panels = [
    (-4, "車が右へ 4° 向いた絵", f"戻す舵 δ′ = {deg_txt(lab[-4])}", f"（手本より {abs(math.degrees(lab[-4]-base)):.1f}° 左へ）"),
    (0, "記録した絵（手本）", f"手本の舵 δ = {deg_txt(base)}", "人や slam2d_route の操作"),
    (4, "車が左へ 4° 向いた絵", f"戻す舵 δ′ = {deg_txt(lab[4])}", f"（手本より {abs(math.degrees(lab[4]-base)):.1f}° 右へ）"),
]
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">',
       f'<rect width="{W}" height="{H}" fill="#fff" rx="14"/>',
       f'<text x="{M}" y="40" font-size="26" font-weight="700" fill="{INK}">1 枚の記録から「ずれた絵」と「戻す舵」の組を作る</text>']
for i, (deg, title, l1, l2) in enumerate(panels):
    x = M + i * (IW + GAP)
    stroke = ORANGE if deg == 0 else "#bbb"
    out.append(img(f"p{deg:+d}.jpg", x, ROW1, IW, IH))
    out.append(f'<rect x="{x}" y="{ROW1}" width="{IW}" height="{IH}" fill="none" stroke="{stroke}" stroke-width="{4 if deg == 0 else 2}" rx="4"/>')
    out.append(f'<text x="{x + IW/2}" y="{ROW1 + IH + 32}" text-anchor="middle" font-size="22" font-weight="700" fill="{INK}">{title}</text>')
    out.append(f'<text x="{x + IW/2}" y="{ROW1 + IH + 60}" text-anchor="middle" font-size="20" fill="{ORANGE if deg else INK}">{l1}</text>')
    out.append(f'<text x="{x + IW/2}" y="{ROW1 + IH + 84}" text-anchor="middle" font-size="16" fill="{SUB}">{l2}</text>')
# 下の段: 車体マスクと式
y2 = H1 + 10
out.append(img("mask.jpg", M, y2, MASK_W, MASK_H))
out.append(f'<rect x="{M}" y="{y2}" width="{MASK_W}" height="{MASK_H}" fill="none" stroke="#bbb" stroke-width="2" rx="4"/>')
tx = M + MASK_W + 30
lines = [
    ("紫は記録から推定した車体（走行中も画素がほとんど変わらない所）。", INK, 19),
    ("車体はカメラと一緒に回るので、ずらさずに元の絵を貼り戻す。", INK, 19),
    (f"向きのずれ ψ は窓の横ずらし（fx·ψ、4° で約 {meta['shift_px_4deg']:.0f} px）で近似する。", INK, 19),
    ("左右を切り落とした窓の中だけを動かし、端に作り物の画素を出さない。", INK, 19),
    ("δ′ = δ − k·ψ　（k = 0.8。ψ > 0 は車が左を向いた向き、舵も左が正）", ORANGE, 21),
    ("学習では ψ を ±6° の範囲から一様に選ぶ。この図は ±4° の例。", SUB, 17),
]
for j, (t, c, s) in enumerate(lines):
    out.append(f'<text x="{tx}" y="{y2 + 30 + j * 36}" font-size="{s}" fill="{c}">{t}</text>')
out.append('</svg>')
print("\n".join(out))
