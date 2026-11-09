# STEP → 表示用 GLB

依存: `pip install cadquery-ocp`（OpenCASCADE）、`npm i @gltf-transform/cli`。

```bash
# 1. STEP → GLB（面を三角形に分割。0.2 mm の弦の誤差。ピークメモリ約 4 GB）
python step2glb.py surge_mk2.step raw.glb 0.2
# 1b. マテリアルを樹脂らしく直す（OpenCASCADE は全部 metallic=1・roughness=1 で書くので黒い部品が真っ黒に見える）
node fixmat.mjs raw.glb raw.glb
# 2. 間引き＋Draco 圧縮（約 32 MB → 1.7 MB）
npx gltf-transform optimize raw.glb ../../docs/assets/3d/car.glb --compress draco --simplify-ratio 0.3 --simplify-error 0.0003 --texture-compress false
# 3. 後輪ユニットだけを切り出す（最後の引数を付けると車軸方向に分解して並べる [m]）
node extract.mjs raw.glb wheel_raw.glb WheelUnit:1
node extract.mjs raw.glb wheel_exp_raw.glb WheelUnit:1 0.022
npx gltf-transform optimize wheel_raw.glb ../../docs/assets/3d/wheel.glb --compress draco --simplify-ratio 0.5 --simplify-error 0.0002 --texture-compress false
npx gltf-transform optimize wheel_exp_raw.glb ../../docs/assets/3d/wheel_exp.glb --compress draco --simplify-ratio 0.5 --simplify-error 0.0002 --texture-compress false
```

`extract.mjs` はノード名（Fusion のコンポーネント名）で探す。分解の並び順は `RANK` に書いてある。
3D ページのラベルの座標（`data-position`）は GLB の座標（m、Y が上、Z が前、X が左）。

## 図を作る

```bash
# センサの配置図（F-05）: car.glb を真上から正射影で描く（ortho.html を http で配信して ortho.mjs で PNG に）
python3 -m http.server 8773 &   # ortho.html と car.glb を置いたディレクトリで
node ortho.mjs top.png
python3 ../fig_sensor_layout.py top.png > ../../docs/assets/fig/sensor_layout.svg
# 前輪の断面図（F-04）: 左前輪ユニットを車軸を通る面（Z=0.1153 m）で切る
node section.mjs raw.glb LeftUnit:1 0.1153 sec.json
python3 ../fig_front_section.py sec.json > ../../docs/assets/fig/front_section.svg
# ステアリングの換算のグラフ（F-02）
python3 ../fig_steer_link.py > ../../docs/assets/fig/steer_link.svg
```
