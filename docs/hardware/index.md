# ハードウェア

!!! summary "要点"
    - SURGE Mark.2 は、Raspberry Pi やカメラなどの既製品を除き、**モータドライバを含めて自作**しています。
    - 看板は、後輪のホイールの中にモータを収めた**インホイール・ダイレクトドライブ**です。左右の後輪に、1 輪ずつ N·m 単位でトルクを指令できます。
    - ステアリングにも、後輪と**同じモータと同じモータドライバ**を使っています。

<div class="sg-3d">
<model-viewer src="../assets/3d/car.glb" alt="SURGE Mark.2 の 3D モデル" camera-controls touch-action="pan-y"
  camera-orbit="35deg 65deg auto" environment-image="neutral" exposure="1.3" shadow-intensity="0.7">
<button class="sg-hotspot" slot="hotspot-rear" data-position="0.09 0.02 -0.115" data-normal="1 0 0" data-href="in-wheel-drive/">インホイール駆動</button>
<button class="sg-hotspot" slot="hotspot-steer" data-position="0 0.054 0.07" data-normal="0 1 0" data-href="steering/">ステアリング</button>
<button class="sg-hotspot" slot="hotspot-lidar" data-position="0 0.089 -0.0475" data-normal="0 1 0" data-href="sensors/">LiDAR</button>
<button class="sg-hotspot" slot="hotspot-board" data-position="0.01 0.06 0.02" data-normal="0 1 0" data-href="electronics/">制御基板</button>
</model-viewer>
<div class="sg-3d__bar"><span style="opacity:.7">ラベルを押すと、その部品の解説へ移ります。全体を詳しく見るなら <a href="3d-model/">3D データ</a> へ。</span></div>
</div>

## 全体の構成

| 区分 | 中身 | 自作か |
|---|---|---|
| 駆動 | 後輪 2 輪のインホイール・ダイレクトドライブ（5010 360 KV の BLDC） | モータは市販品。ホイール・タイヤ・MD は自作 |
| 操舵 | 後輪と同じモータと MD を位置モードで使う | 同上 |
| 車体 | 厚さ 3 mm のアルミのシャシー、前後ダブルウィッシュボーン、ラジコン用のオイルダンパー | |
| 計算機 | Raspberry Pi 5（判断）＋ STM32F446RE（リアルタイム制御） | STM32 の基板は自作 |
| センサ | LiDAR、前後カメラ、前後超音波、IMU、前輪の角度センサ | |
| 電源 | 駆動用・信号用の 2 系統（Ni-MH 9.6 V ×2）、両系統の電圧・電流を測定 | |

!!! placeholder "写真 P-14：車体全体（カウルを外した状態）"
    斜め前上方から、内部の配置が分かる写真。ハードウェアの入口ページの扉に使う。

## 各ページ

<div class="sg-cards">
<a class="sg-card" href="in-wheel-drive/"><p class="sg-card__q">インホイール・ダイレクトドライブ</p><p class="sg-card__a">ホイールの中にモータを収めた後輪。構造、ダイレクトドライブを選んだ理由、4 代の MD 基板。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="motor-driver/"><p class="sg-card__q">自作モータドライバと FOC</p><p class="sg-card__a">1 秒に 2 万回電流を測ってトルクを出す基板と、その守りの仕組み。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="steering/"><p class="sg-card__q">ステアリング</p><p class="sg-card__a">サーボの代わりに BLDC を位置制御。比例しないリンクを、走って測った式で換算する。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="chassis/"><p class="sg-card__q">シャシーと足まわり</p><p class="sg-card__a">アルミのシャシー、ダブルウィッシュボーン、ネジごと回る前輪の車軸。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="sensors/"><p class="sg-card__q">センサ</p><p class="sg-card__a">LiDAR・カメラ・超音波・IMU の配置と、それぞれの癖への対処。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="electronics/"><p class="sg-card__q">電装と電源</p><p class="sg-card__a">2 系統の電源、制御基板、Raspberry Pi からの「生きている」合図。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="bom/"><p class="sg-card__q">部品表（BOM）</p><p class="sg-card__a">役割ごとの部品の一覧と、自作部品の設計データの置き場所。</p><p class="sg-card__go">読む →</p></a>
<a class="sg-card" href="3d-model/"><p class="sg-card__q">3D データ</p><p class="sg-card__a">車体全体を回して見る。Fusion のビューアと STEP のダウンロード。</p><p class="sg-card__go">読む →</p></a>
</div>
