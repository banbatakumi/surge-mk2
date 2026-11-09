# 主要諸元

!!! summary "要点"
    SURGE Mark.2 の数字を 1 ページに集めました。各行の「出どころ」が正で、このページは写しです。

## 車体

| 項目 | 値 | 出どころ |
|---|---|---|
| 外形（長さ × 幅） | 約 0.37 m × 0.18 m | [`vehicle.toml`][vehicle-toml] `footprint` |
| 質量 | 2.0 kg | `vehicle.toml` `mass` |
| ホイールベース | 0.23 m | `vehicle.toml` `wheelbase` |
| 後輪トレッド | 0.155 m | `vehicle.toml` `track` |
| 車輪半径 | 30 mm | `vehicle.toml` `wheel_radius` |
| 最大路面舵角 | 0.472 rad（約 27.0°） | `vehicle.toml` `max_steer` |
| シャシー | アルミ板 t3 | 聞き取り |
| サスペンション | 前後ダブルウィッシュボーン、ラジコン用オイルダンパー | 聞き取り |
| 最高速度 | 15 km/h | `PROTOPEDIA.md` |

## 駆動・操舵

| 項目 | 値 | 出どころ |
|---|---|---|
| 駆動方式 | 後輪左右独立のインホイール・ダイレクトドライブ | 聞き取り |
| モータ | ドローン用 5010 360 KV の BLDC ×3（後輪 2・操舵 1） | 聞き取り |
| モータの極対数 | 7 | MD `config.h` `POLE_PAIRS` |
| モータドライバ | 自作（CurcuitV4）、STM32F303K8、FOC | [`BLDC`][bldc-repo] |
| 電流制御の周期 | 20 kHz | MD `config.h` `PWM_FREQ` |
| 電流の上限 | 10 A | MD `config.h` `MAX_CURRENT` |
| 1 輪のトルク上限 | 0.15 N·m | STM32 `drive.h` `DRIVE_MAX_TORQUE_NM`（[駆動制御](../control/drive.md)） |
| 指令できる最高車速 | 5.0 m/s | STM32 `drive.h` `DRIVE_MAX_SPEED_M_S` |

## 計算機・通信

| 項目 | 値 | 出どころ |
|---|---|---|
| 上位 | Raspberry Pi 5 | |
| 下位 | STM32F446RE、メインループ 2 kHz | [構成と制御周期](../control/index.md) |
| Pi ⇄ STM32 | UART 1 Mbps、指令とテレメトリ 100 Hz、GPIO6 ハートビート 100 Hz | [UART プロトコル](../control/protocol.md) |
| STM32 ⇄ MD | UART 1 Mbps ×3、2 kHz、CRC-8 | MD `docs/SERIAL_PROTOCOL.md` |

## センサ

| 項目 | 値 |
|---|---|
| LiDAR | LD06（10 Hz 回転） |
| カメラ | IMX219（160° 広角）×2、前後 |
| 超音波 | RCW-0001 ×2、前後 |
| IMU | MPU-6050（6 軸、地磁気なし） |
| 車速 | 前輪左右の磁気式角度センサ AS5600 |

## 電源

| 項目 | 値 | 出どころ |
|---|---|---|
| バッテリー | Ni-MH 9.6 V 1600 mAh（8 セル）×2（駆動用・信号用） | `PROTOPEDIA.md`、[システム概要][system-overview] |
| Raspberry Pi の電源 | DC-DC で 5 V | 聞き取り |
| 計測 | 両系統の電圧と電流 | 聞き取り |
| 保護 | ヒューズ | 聞き取り |

「聞き取り」は開発者への聞き取り（2026-11-09）です。

[vehicle-toml]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/config/vehicle.toml
[bldc-repo]: https://github.com/banbatakumi/BLDC/tree/FW/Program_V4
[system-overview]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/docs/system_overview.md#2-ハードウェア
