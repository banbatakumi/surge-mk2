# 3D データ

!!! summary "要点"
    - SURGE Mark.2 の全体の 3D モデルを、このページでそのまま回して見られます。ラベルを押すと、その部品の解説へ移ります。
    - 部品を 1 つずつ選んで見たいときや、寸法を測りたいときは、下の **Fusion のビューア**を使ってください。
    - 設計データ（STEP）はダウンロードできます。

## 車体全体

<div class="sg-3d">
<model-viewer src="../assets/3d/car.glb" alt="SURGE Mark.2 の 3D モデル" camera-controls touch-action="pan-y"
  camera-orbit="35deg 65deg auto" environment-image="neutral" exposure="1.3" shadow-intensity="0.7" style="height:30rem">
<button class="sg-hotspot" slot="hotspot-rear" data-position="0.09 0.02 -0.115" data-normal="1 0 0" data-href="../in-wheel-drive/">インホイール駆動（後輪）</button>
<button class="sg-hotspot" slot="hotspot-steer" data-position="0 0.054 0.07" data-normal="0 1 0" data-href="../steering/">ステアリング</button>
<button class="sg-hotspot" slot="hotspot-front" data-position="-0.09 0.02 0.115" data-normal="-1 0 0" data-href="../chassis/#前輪--回るネジが車軸になる">前輪（車速の計測）</button>
<button class="sg-hotspot" slot="hotspot-lidar" data-position="0 0.089 -0.0475" data-normal="0 1 0" data-href="../sensors/">LiDAR</button>
<button class="sg-hotspot" slot="hotspot-board" data-position="0.01 0.06 0.02" data-normal="0 1 0" data-href="../electronics/">制御基板・Raspberry Pi 5</button>
</model-viewer>
<div class="sg-3d__bar"><span style="opacity:.7">ドラッグで回転・ホイールやピンチで拡大・右ドラッグや 2 本指で移動。表示を軽くするため、形状を間引いています。</span></div>
</div>

## Fusion のビューアで詳しく見る

部品の表示・非表示、断面、寸法の計測ができます。Autodesk のサービスを読み込むので、**押したときだけ**読み込みます。

<div class="sg-fusion" data-embed="https://gmail694332.autodesk360.com/g/shares/SH3a9e9QT2649a137be2ca81bb7bd8ed5011?mode=embed" data-title="SURGE Mark.2（Fusion のビューア）">
<button type="button" class="sg-fusion__load">▶ Fusion のビューアを読み込む<span>autodesk360.com のコンテンツを表示します</span></button>
</div>

表示されないときは、[Fusion の公開ページ](https://a360.co/4eYca8R) を直接開いてください。

## ダウンロード

| ファイル | 形式 | 大きさ |
|---|---|---|
| [surge_mk2_step.zip](https://github.com/banbatakumi/surge-mk2/releases/latest/download/surge_mk2_step.zip) | STEP（AP214）を ZIP で圧縮 | 約 9 MB（展開後 約 61 MB） |

STEP は Fusion から書き出したもので、ネジ・スペーサ・基板の部品まで含みます。
基板の設計データ（KiCad・ガーバー）は [部品表](bom.md#自作部品の設計データ) にまとめています。

## このページのモデルの作り方

ページに埋め込んでいるモデルは、STEP から次の手順で作っています（手順とスクリプトはこのサイトのリポジトリの `tools/cad/`）。

1. OpenCASCADE（`cadquery-ocp`）で STEP を読み、面を三角形に分割して glTF（GLB）に書き出す（約 32 MB）。
2. `gltf-transform` で形状を間引き、Draco で圧縮する（約 1.6 MB）。
3. インホイール部だけを切り出し、分解した状態のモデルも作る（[インホイール・ダイレクトドライブ](in-wheel-drive.md)）。

表示には Google の [`<model-viewer>`](https://modelviewer.dev/) を使っています。
