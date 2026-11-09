#!/usr/bin/env python3
"""図 F-04「前輪の断面図」の SVG を作る。

入力は tools/cad/section.mjs の出力（左前輪ユニット LeftUnit:1 を、車軸を通る Z 一定の平面で切った多角形）。
前から見た断面で、右が車の外側。単位は m（ワールド座標）。

    node tools/cad/section.mjs raw.glb LeftUnit:1 0.1153 sec.json
    python3 tools/fig_front_section.py sec.json > docs/assets/fig/front_section.svg
"""
import json
import sys

X0, X1, Y0, Y1 = 0.0425, 0.0915, -0.0205, 0.0455   # 切り出す範囲 [m]
S = 11000                                           # px / m
ML, MR, MT, MB = 40, 330, 30, 40                    # 余白（右にラベル）
W, H = round((X1 - X0) * S) + ML + MR, round((Y1 - Y0) * S) + MT + MB
AXLE_Y = 0.0126                                     # 車軸の高さ（ネジの中心）


def px(x, y):
    return ML + (x - X0) * S, MT + (Y1 - y) * S


STYLE = [  # (部品名に含まれる文字列, 塗り, 線)
    ("Tire", "#3a3d42", "#1d1f22"),
    ("WheelFront", "#9aa0a8", "#5d6168"),
    ("Bearing", "#2f7de1", "#1b4f99"),
    ("CAP_M3_25", "#c8ced6", "#6b727c"),
    ("EncoderMagnet:1/=>", "#8b5cf6", "#5b33c4"),
    ("InsertNut", "#d4a72c", "#8a6a12"),
    ("Upright", "#ffb27a", "#d4520a"),
    ("Uprigh2", "#ffb27a", "#d4520a"),
]


def style(part):
    for key, fill, stroke in STYLE:
        if key in part:
            return fill, stroke
    return "#d9dce0", "#8a8f98"


def main():
    data = json.load(open(sys.argv[1]))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">',
           f'<defs><clipPath id="c"><rect x="{ML}" y="{MT}" width="{(X1-X0)*S:.0f}" height="{(Y1-Y0)*S:.0f}"/></clipPath>'
           f'<pattern id="h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           f'<line x1="0" y1="0" x2="0" y2="8" stroke="#fff" stroke-opacity=".35" stroke-width="2"/></pattern></defs>',
           f'<rect width="{W}" height="{H}" fill="#fff" rx="12"/>', '<g clip-path="url(#c)">']
    # 大きい部品から先に描く（タイヤ → ホイール → ナックル → 小物）
    order = ["Tire", "WheelFront", "Upright", "Uprigh2", "Bearing", "CAP_M3_25", "EncoderMagnet", "InsertNut"]
    rank = lambda r: next((i for i, k in enumerate(order) if k in r["part"]), len(order))
    for r in sorted(data, key=rank):
        if "Spacer" in r["part"]:
            continue
        fill, stroke = style(r["part"])
        d = " ".join("M" + " L".join(f"{px(*p)[0]:.1f},{px(*p)[1]:.1f}" for p in loop) + " Z" for loop in r["loops"])
        out.append(f'<path d="{d}" fill="{fill}" fill-rule="evenodd" stroke="{stroke}" stroke-width="1.2"/>')
        out.append(f'<path d="{d}" fill="url(#h)" fill-rule="evenodd"/>')
    out.append('</g>')
    # 回転軸
    ax0, ay = px(X0, AXLE_Y)
    ax1, _ = px(X1, AXLE_Y)
    out.append(f'<line x1="{ax0:.1f}" y1="{ay:.1f}" x2="{ax1:.1f}" y2="{ay:.1f}" stroke="#d4520a" stroke-width="1.5" stroke-dasharray="14 4 3 4"/>')
    # 角度センサ（3D データに無いので模式）
    mx, my = px(0.0492, AXLE_Y)
    sx = px(0.0445, AXLE_Y)[0]
    out.append(f'<rect x="{sx-6:.1f}" y="{my-46:.1f}" width="10" height="92" fill="none" stroke="#5b33c4" stroke-width="2" stroke-dasharray="5 4"/>')
    lx = W - MR + 24

    def lab(x, y, ty, title, sub, color="#222"):
        cx, cy = px(x, y) if x < 1 else (x, y)
        return (f'<polyline points="{cx:.1f},{cy:.1f} {W-MR+8:.1f},{ty:.1f} {lx-6:.1f},{ty:.1f}" fill="none" stroke="#666" stroke-width="1.3"/>'
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="#222"/>'
                f'<text x="{lx}" y="{ty-4:.1f}" font-size="19" font-weight="700" fill="{color}">{title}</text>'
                f'<text x="{lx}" y="{ty+19:.1f}" font-size="15" fill="#555">{sub}</text>')
    out.append(lab(0.0870, 0.0400, 60, "タイヤ", "TPE の 3D プリント（自作）"))
    out.append(lab(0.0830, 0.0340, 125, "ホイール", "3D プリント"))
    out.append(lab(0.0820, AXLE_Y + 0.0024, 195, "回るネジ（車軸）", "M3×25。車輪と一緒に回る"))
    out.append(lab(0.0684, AXLE_Y + 0.0028, 265, "ベアリング ×2", "ナックルに入れる"))
    out.append(lab(0.0560, 0.0260, 335, "ナックル", "サスペンションのアームが付く"))
    out.append(lab(0.0555, 0.0147, 405, "磁石付きの自作ナット", "ネジの先端を留め、磁石が回る"))
    out.append(lab(sx - 1, my + 40, 475, "角度センサ（AS5600）", "灯火・エンコーダ基板上（位置は模式）", "#5b33c4"))
    out.append(f'<text x="{ML}" y="{H-14}" font-size="15" fill="#777">前から見た断面（右が車の外側）。一点鎖線が回転軸。</text>')
    out.append('</svg>')
    print("\n".join(out))


if __name__ == "__main__":
    main()
