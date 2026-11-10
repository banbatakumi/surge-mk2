# システム構成

!!! summary "要点"
    - 頭脳は 3 段です。**Raspberry Pi 5** が判断し、**STM32** が 2 kHz で車を制御し、**3 枚の自作 MD** が 20 kHz でモータの電流を制御します。
    - 速い制御ほど下の段に置き、**上の段が止まっても下の段だけで車を止められる**ようにしています。
    - Pi の中は役割ごとに別プロセスに分かれ、内部のバスでつながっています。

!!! note "【設計の説明】"
    確認した版: ファーム `6b5bdb3`、上位 `2d0a44e`。

## 役割分担

| | Raspberry Pi 5（上位） | STM32F446RE（下位） | BLDC ドライバ（MD）×3 |
|---|---|---|---|
| 担当 | 知覚、地図、経路計画、経路追従、GUI | 車速制御、TC / ABS / TV、舵角制御、安全層、センサ取得 | FOC による電流（トルク）制御、ステアの位置制御 |
| 周期 | LiDAR 10 Hz、指令 50〜100 Hz | **2 kHz（500 µs 周期のメインループ）** | 電流 20 kHz・外側 1 kHz |
| 失敗したとき | STM32 が最大制動で停車保持 | IWDG でリセット、ハートビート断で緊急停止ラッチ | 通信 100 ms 無応答で STM32 が検出 |
| 言語 | Python 3.13（numpy、ONNX） | C（STM32CubeMX + 自作ライブラリ） | C（STM32F303K8。[自作モータドライバ](../hardware/motor-driver.md)） |

MD は後輪左・後輪右・ステアの 3 台で、STM32 と 1 Mbps の UART で別々につながっています。

### なぜ 2 層に分けたか

- **車速制御・スリップ制御は 2 kHz 級の応答が要る。** Python の 10〜100 Hz では足りません。
  この車の後輪は軽く、実機の ABS の記録では、グリップの限界を超えるトルクを掛けると **約 20 ms で深くロック** しました
  （[`tools/fwsim/plant.py`][plant-py] のコメント）。
- **一方、SLAM やレーシングライン計算は Python の方が速く作れる。** 地図計算は Pi 5 でも 100 ms を超えることがあります
  （[地図と自己位置推定](../autonomy/mapping.md) の実測を参照）。
- **上位が落ちても止まれること。** 安全に関わる処理を下位に置くと、上位の不具合・遅延・Wi-Fi 切断が車の暴走に直結しません。

## データの流れ

```mermaid
flowchart TB
    subgraph SENS["センサ"]
        LIDAR[LD06 LiDAR]
        IMU[MPU6050]
        ENC[前輪エンコーダ ×2]
        US[超音波 ×2]
    end
    subgraph STM["STM32"]
        FW[メインループ 2 kHz]
    end
    MD1[MD 後輪左]
    MD2[MD 後輪右]
    MD3[MD ステア]
    subgraph PI["Raspberry Pi 5（systemd の別プロセス）"]
        IO[io_node<br/>UART・GPIO]
        BUS{{ZeroMQ バス<br/>+ 共有メモリ}}
        PLAN[planning_node]
        TEL[telemetry_node<br/>WebSocket サーバ]
        CAM[camera_node]
        PER[cam_perception_node ほか]
    end
    GUI[ブラウザの GUI]

    LIDAR & IMU & ENC & US --> FW
    FW <--> MD1 & MD2 & MD3
    FW <-- "UART 1 Mbps" --> IO
    IO -- "GPIO6 100 Hz 矩形波" --> FW
    IO <--> BUS
    BUS <--> PLAN
    BUS <--> TEL
    CAM -- "画像は共有メモリ" --> BUS
    BUS --> PER
    TEL <-- "WebSocket" --> GUI
```

### Pi 側のプロセス

`raspi/setup/install_services.sh` が systemd のサービスとして次を立てます
（[`UNITS`][install-services] の定義）。

| サービス | 役割 |
|---|---|
| `surge-io` | STM32 との UART 送受信、GPIO のハートビート、時刻同期。`Nice=-10` で優先度を上げてある |
| `surge-camera` | CSI カメラ 2 台の取り込み。画像を共有メモリへ書く |
| `surge-telemetry` | ブラウザ GUI との WebSocket サーバ。操縦権・デッドマン・自律走行の中継 |
| `surge-planning` | 点群から走行指令を作る（自動運転モードを持つ） |
| `surge-cam-perception` / `surge-cam-e2e` / `surge-line-perception` / `surge-cam-track` | カメラ系の認識（走行可能領域、模倣学習、白線、対象追従） |
| `surge-mdns` | `<ホスト名>.local` の問い合わせに、Wi-Fi 端末向けにユニキャストで答える補助（アクセスポイントがマルチキャストを中継しない環境の対策） |
| `surge-arrow-signal`（任意） | 前方カメラで矢印信号を認識して経路を選ぶ。unit だけ置き、既定では無効 |
| `surge-logger`（任意） | mcap 形式の記録。SD への書き込みを避けるため既定では入れない |
| `surge-logclean.timer` | 古い記録を毎時消す（7 日より古いものと、合計 8 GB を超えたぶん） |

`surge-io` が止まる、または Pi が落ちると、STM32 側のハートビート監視が **緊急停止をラッチ** します
（[安全層](../control/safety.md)）。

## 時刻と遅延

- STM32 の時刻は `micros` のカウンタ（32 bit、約 71.6 分でラップ）で、Pi の `CLOCK_MONOTONIC` とは別物です。
  PING／PONG の 4 つのタイムスタンプからクロックオフセットとドリフトを推定して換算します
  （[プロトコル](../control/protocol.md#時刻同期)）。SLAM と遅延測定がこれに依存します。
- 実測値（[`vehicle.toml`][vehicle-toml] の `[dynamics]`。舵は 2026-10-20 に反映した車両の校正 3、遅延は 2026-11-06 の校正 4）:

    | 量 | 値 |
    |---|---|
    | 操舵のむだ時間（`dead_time_s`） | 約 10 ms |
    | 操舵の 1 次遅れ時定数（`tau_steer_s`） | 0（曲率の 2 次遅れで表す: 固有角振動数 約 69 rad/s、減衰比 0.9） |
    | LiDAR スキャン完了 → 反応した指令を STM32 が受理（`control_latency_s`） | 約 3.9 ms |

    舵そのものはほとんど遅れません。経路追従はこれらを [遅延補償](../autonomy/tracking.md#遅延補償) で見込んでいます。

## このサイトで扱わないもの

- **V1 の `robotcar/`** — Raspberry Pi 3 の手動遠隔操縦システム。SURGE Mark.2 とは別のシステムです。

[install-services]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/raspi/setup/install_services.sh
[plant-py]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/tools/fwsim/plant.py
[vehicle-toml]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/config/vehicle.toml
