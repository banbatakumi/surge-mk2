---
template: home.html
title: SURGE Mark.2
hide:
  - navigation
  - toc
---

# SURGE Mark.2

## 知りたいことから選ぶ

<div class="sg-cards">
<a class="sg-card" href="about-car/"><p class="sg-card__q">どんな車？</p><p class="sg-card__a">何ができて、なぜ作ったのか。写真・動画・3D モデルと、主要な数字で全体をつかむ。</p><p class="sg-card__go">SURGE Mark.2 とは →</p></a>
<a class="sg-card" href="hardware/"><p class="sg-card__q">どう作った？</p><p class="sg-card__a">タイヤの中のモータ、自作のモータドライバ、アルミのシャシー、センサの配置、部品表。</p><p class="sg-card__go">ハードウェア →</p></a>
<a class="sg-card" href="about-car/tour/"><p class="sg-card__q">どう走らせている？</p><p class="sg-card__a">センサが壁を見てからタイヤが回るまでを、1 周の流れに沿って追いかける。</p><p class="sg-card__go">1 周を追いかける →</p></a>
</div>

## 看板はタイヤの中にある

SURGE Mark.2 の後輪は、ドローン用の BLDC モータ（5010 サイズ・360 KV）の**ロータにホイールを直接ネジ留め**しています。
モータはホイールの中にすっぽり収まり、ギアもベルトもありません。

モータの裏側には自作のモータドライバ基板を背負わせ、基板の中央にある角度センサが
モータ軸の磁石を直接読みます。相電流を測ってベクトル制御（FOC）を回すので、
**左右の後輪それぞれに「何 N·m 出すか」を指令できます。**

ギアのガタ（バックラッシ）や粘りがないので、トラクションコントロールやトルクベクタリングの
制御がそのまま路面に届く――これがダイレクトドライブを選んだ理由です。

[インホイール・ダイレクトドライブの詳細 →](hardware/in-wheel-drive.md){ .sg-btn .sg-btn--primary }

<div class="sg-stats" markdown>
<div class="sg-stat"><div class="sg-stat__v">0<small>段</small></div><div class="sg-stat__k">減速機（ダイレクトドライブ）</div></div>
<div class="sg-stat"><div class="sg-stat__v">20<small>kHz</small></div><div class="sg-stat__k">モータドライバの電流制御周期</div></div>
<div class="sg-stat"><div class="sg-stat__v">2<small>kHz</small></div><div class="sg-stat__k">STM32 の駆動制御周期</div></div>
<div class="sg-stat"><div class="sg-stat__v">10<small>種以上</small></div><div class="sg-stat__k">切り替えて走れる自動運転の方式</div></div>
</div>

## この車でできること

| できること | どうやって |
|---|---|
| **地図を作って周回する** | LiDAR で地図を作り、自分の位置を推定しながら、計算した走行ラインで周回します。分岐のあるコースでは経路を選びます。 |
| **地図なしで壁を避けて走る** | LiDAR で空いている方向を探す方式（Follow the Gap など）。 |
| **カメラで道を見る** | 走行可能な領域や白線の認識、カメラ画像から操舵を学ぶ模倣学習。 |
| **学習した方策で走る** | シミュレータで強化学習した方策を実機で動かします。 |
| **安全に止まる** | Raspberry Pi が固まっても、通信が切れても、制御マイコンが単独で車を止めます。 |

方式の一覧は [走らせ方の一覧](about-car/modes.md) にあります。

## このサイトの歩き方

- 各ページの冒頭にある **「要点」** だけを拾い読みすれば、全体の流れがつかめます。
- 本文は **しくみ → 設計の詳細** の順に深くなります。満足したところで次のページへどうぞ。
- 点線の下線が付いた用語（例: FOC、SLAM）は、マウスを乗せると短い説明が出ます。
- 数値や挙動の出どころは、各ページの末尾にソースコードへのリンクで示しています（[このサイトについて](reference/about.md)）。
