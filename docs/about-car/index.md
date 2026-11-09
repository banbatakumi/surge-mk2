# SURGE Mark.2 とは

!!! summary "要点"
    - SURGE Mark.2 は、**10 種類以上の自動運転の方式を 1 台に載せ、同じ車・同じ安全機構で比べられる**自律走行ミニカーです。
    - 後輪は**インホイール・ダイレクトドライブ**で、左右の後輪のトルクを 1 輪ずつ制御します。
    - 頭脳は Raspberry Pi 5（判断）と STM32（リアルタイム制御）の 2 つで、Raspberry Pi が止まっても STM32 が単独で車を止めます。

<div class="sg-video">
<iframe src="https://www.youtube-nocookie.com/embed/Tv3HFxTQJk8" title="SURGE Mark.2 の走行動画" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe>
</div>

<figure markdown>
![SURGE Mark.2 のメイン写真](../assets/img/car_blackback.jpg){ loading=lazy }
<figcaption>SURGE Mark.2。前方のライトは灯火・エンコーダ基板で光らせています。</figcaption>
</figure>

## 主要な数字

<div class="sg-stats">
<div class="sg-stat"><div class="sg-stat__v">2.0<small>kg</small></div><div class="sg-stat__k">質量</div></div>
<div class="sg-stat"><div class="sg-stat__v">0.37 × 0.18<small>m</small></div><div class="sg-stat__k">長さ × 幅</div></div>
<div class="sg-stat"><div class="sg-stat__v">0.23<small>m</small></div><div class="sg-stat__k">ホイールベース</div></div>
<div class="sg-stat"><div class="sg-stat__v">18<small>km/h</small></div><div class="sg-stat__k">最高速度（5.0 m/s）</div></div>
<div class="sg-stat"><div class="sg-stat__v">3<small>個</small></div><div class="sg-stat__k">BLDC モータ（後輪 2・操舵 1）</div></div>
<div class="sg-stat"><div class="sg-stat__v">2<small>系統</small></div><div class="sg-stat__k">電源（駆動用・信号用）</div></div>
</div>

ほかの数字は [主要諸元](../reference/specs.md) にまとめています。

## 3 つの層

```mermaid
flowchart LR
    subgraph PI["Raspberry Pi 5（10〜100 Hz）"]
        P1[知覚・SLAM] --> P2[経路計画<br/>レーシングライン]
        P2 --> P3[経路追従<br/>速度指令]
    end
    subgraph MCU["STM32F446RE（2 kHz）"]
        M1[車速 PI] --> M2[トルク配分<br/>TC / ABS / TV]
        M3[安全層]
    end
    subgraph MD["自作モータドライバ ×3（20 kHz）"]
        D1[FOC<br/>電流ループ]
    end
    P3 -- "UART 1 Mbps<br/>指令 100 Hz" --> M1
    M2 -- "UART 1 Mbps<br/>トルク指令 2 kHz" --> D1
    MCU -- "テレメトリ 100 Hz<br/>LiDAR" --> P1
    PI -. "GPIO 100 Hz 矩形波<br/>（生存信号）" .-> M3
```

- **Raspberry Pi は「どこへ・どれだけの速さで」を決めます。** 自己位置推定、地図、走行ライン、障害物の回避。
- **STM32 は「どうやってタイヤにトルクを伝えるか」を決めます。** 車速の制御、スリップの制御、左右のトルク配分、安全停止。
- **モータドライバは電流だけを見ます。** 狙ったトルクを、相電流を測りながら正確に出します。

「上位が落ちても下位が単独で車を止められること」が設計の出発点です。詳しくは [システム構成](system.md)。

## もっと知る

<div class="sg-cards">
<a class="sg-card" href="story/"><p class="sg-card__q">なぜ作ったのか</p><p class="sg-card__a">「自動運転の手法を、1 台で全部走らせて比べたい」から始まった話と、こだわり。</p><p class="sg-card__go">生まれた理由とこだわり →</p></a>
<a class="sg-card" href="tour/"><p class="sg-card__q">1 周の間に何が起きているか</p><p class="sg-card__a">LiDAR が壁を見てから、タイヤにトルクが出るまでを順に追う。</p><p class="sg-card__go">1 周を追いかける →</p></a>
<a class="sg-card" href="modes/"><p class="sg-card__q">どんな方式で走れるか</p><p class="sg-card__a">地図を作る、壁を避ける、カメラで見る、学習する。走らせ方の一覧。</p><p class="sg-card__go">走らせ方の一覧 →</p></a>
</div>

---

**出典**: 寸法・質量は [`vehicle.toml`][vehicle-toml]、最高速度は STM32 ファームの `DRIVE_MAX_SPEED_M_S`、方式の数は `PROTOPEDIA.md`、周期は STM32 ファームと MD ファーム。

[vehicle-toml]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/config/vehicle.toml
