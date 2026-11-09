# 部品表（BOM）

!!! summary "要点"
    - SURGE Mark.2 を構成する部品を、**役割ごと**にまとめた表です。
    - 価格は**購入時の単価（概算）**、入手先は**購入したショップ名**です。部品の合計はおよそ **3 万 5,700 円**です。
    - 自作の部品（基板・3D プリント部品）は、設計データの置き場所と解説ページへのリンクを付けています。

価格は**購入時の単価（概算、円）**です。合計はおよそ **35,700 円**（下の表の合計 35,680 円）です。
シャシー・ホイール・タイヤは大学の設備で製作したため、表では 0 円としています。

<div class="sg-stats">
<div class="sg-stat"><div class="sg-stat__v">35,680<small>円</small></div><div class="sg-stat__k">部品の合計（購入時の概算）</div></div>
<div class="sg-stat"><div class="sg-stat__v">13,000<small>円</small></div><div class="sg-stat__k">うち Raspberry Pi 5（最も高い部品）</div></div>
<div class="sg-stat"><div class="sg-stat__v">5,400<small>円</small></div><div class="sg-stat__k">BLDC モータ 3 個</div></div>
</div>

## 計算機・制御

| 部品 | 型番 | 数量 | 用途 | 入手先 | 単価 | 小計 | 備考 |
|---|---|---|---|---|---|---|---|
| Raspberry Pi 5（4 GB） | — | 1 | 自動運転の判断、地図、ログ | スイッチサイエンス | 13,000 | 13,000 | |
| メイン基板（自作） | — | 1 | STM32F446RE を搭載。リアルタイム制御・安全停止 | JLCPCB・マルツオンライン・秋月電子 | 2,500 | 2,500 | 部品込み。DC-DC と IMU は別計上。[電装と電源](electronics.md) |
| IMU | MPU6050 | 1 | 角速度・加速度 | Amazon | 300 | 300 | メイン基板に載せる |
| DC-DC コンバータ | OKL-T/6-W12N-C | 1 | 電池 → Raspberry Pi 用 5 V | 秋月電子 | 880 | 880 | メイン基板に載せる |

## 駆動・操舵

| 部品 | 型番 | 数量 | 用途 | 入手先 | 単価 | 小計 | 備考 |
|---|---|---|---|---|---|---|---|
| BLDC モータ（5010 サイズ・360 KV、アウターロータ型） | — | 3 | 後輪 ×2・ステアリング ×1 | AliExpress | 1,800 | 5,400 | ドローン用を改造せずに使用。[インホイール駆動](in-wheel-drive.md) |
| BLDC 制御基板（自作 MD、CurcuitV4） | — | 3 | FOC によるトルク・位置制御 | JLCPCB・マルツオンライン・秋月電子 | 1,500 | 4,500 | 部品込み（モータ角度用の AS5600 を含む）。[自作モータドライバ](motor-driver.md) |

## センサ

| 部品 | 型番 | 数量 | 用途 | 入手先 | 単価 | 小計 | 備考 |
|---|---|---|---|---|---|---|---|
| LiDAR | LD06 | 1 | 地図・自己位置・障害物 | AliExpress | 2,000 | 2,000 | |
| カメラ | IMX219 | 2 | 前後の映像 | AliExpress | 600 | 1,200 | 160° の広角レンズ |
| 超音波センサ | RCW-0001 | 2 | 前後の近距離の障害物 | AliExpress | 200 | 400 | |
| 磁気式角度センサ | AS5600 | 2 | 前輪の車速 | AliExpress | 150 | 300 | 灯火・エンコーダ基板（OtherBoard_V1）で使用 |

## 電源

| 部品 | 型番 | 数量 | 用途 | 入手先 | 単価 | 小計 | 備考 |
|---|---|---|---|---|---|---|---|
| バッテリー（Melasta 9.6 V 1600 mAh） | — | 2 | 駆動用・信号用 | Amazon | 1,500 | 3,000 | Ni-MH 8 セル |

## 機構

| 部品 | 型番 | 数量 | 用途 | 入手先 | 単価 | 小計 | 備考 |
|---|---|---|---|---|---|---|---|
| オイルダンパー（50 mm） | — | 4 | サスペンション | AliExpress | 400 | 1,600 | ラジコン用 |
| ベアリング | — | 4 | 前輪のナックル（左右 2 個ずつ） | Amazon | 150 | 600 | |
| シャシー | — | 1 | 主となる板（アルミ t3） | 大学の設備で製作 | 0 | 0 | [シャシーと足まわり](chassis.md) |
| ホイール | — | 4 | 3D プリント | 大学の設備で製作 | 0 | 0 | |
| タイヤ | — | 4 | TPE の 3D プリント | 大学の設備で製作 | 0 | 0 | |

**合計: 35,680 円**

ネジ・スペーサ・配線・コネクタなどの細かい部品は、この表に含めていません。

## 自作部品の設計データ

| 対象 | 置き場所 | 形式 |
|---|---|---|
| 車体全体（3D） | [3D データ](3d-model.md) | STEP |
| モータドライバ基板（V1〜V4） | [`BLDC`][bldc-repo] の `CurcuitV1`〜`V4` | KiCad、ガーバー（`CurcuitV4/production/`） |
| メイン基板（`MainBoard_V1`〜`V3_2`）、灯火・エンコーダ基板（`OtherBoard_V1`） | [`AutonomousCar`][fw-repo] の `Circuit/` | KiCad |

<div class="sg-next" markdown>
<div markdown>
隣のしくみへ

- [3D データ](3d-model.md)
- [ハードウェアの全体像](index.md)
</div>
<div markdown>
さらに深く

- [自作モータドライバと FOC](motor-driver.md)
- [電装と電源](electronics.md)
</div>
</div>

---

**出典**: 部品・価格・入手先は開発者の部品表（2026-11-09）。基板の版は各基板の回路図。

[bldc-repo]: https://github.com/banbatakumi/BLDC/tree/FW/Program_V4
[fw-repo]: https://github.com/banbatakumi/AutonomousCar/tree/FW/MainBoard_V3/Circuit
