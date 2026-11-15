# リポジトリの案内

SURGE Mark.2 のソースは 3 つのリポジトリに分かれています。このサイト自体も別のリポジトリです。

| リポジトリ | 中身 | 最新のブランチ |
|---|---|---|
| [`AutonomousCar_RasPi`](https://github.com/banbatakumi/AutonomousCar_RasPi) | Raspberry Pi 5 側のソフト（`surge_mk2/`）。自動運転、SLAM、GUI、シミュレータ、校正のツール | `master` |
| [`AutonomousCar`](https://github.com/banbatakumi/AutonomousCar/tree/main) | STM32F446RE のファーム（`Program/MainF446RE_V3`）と、制御基板などの回路（`Circuit/`） | `main` |
| [`BLDC`](https://github.com/banbatakumi/BLDC/tree/main) | モータドライバのファーム（`ProgramV4`）と基板（`CurcuitV1`〜`V4`） | `main` |
| [`surge-mk2`](https://github.com/banbatakumi/surge-mk2) | このサイト | `master` |

!!! note "開発用のブランチは main へまとめた"
    `AutonomousCar` と `BLDC` は、以前は開発用のブランチ（`FW/MainBoard_V3`・`FW/Program_V4`）が最新でした。2026-11-10 に `main` へマージしたので、今はどちらも `main` が最新です。

## どこから読むか

| 知りたいこと | 入口 |
|---|---|
| 車速制御・TC・ABS・トルクベクタリング | `AutonomousCar` の `Program/MainF446RE_V3/src/control/` |
| モータドライバの FOC と校正 | `BLDC` の `ProgramV4/docs/FOC.md` |
| 自動運転の方式 | `AutonomousCar_RasPi` の `surge_mk2/raspi/auto/` |
| 前方ステレオ（照合・同期・校正） | `AutonomousCar_RasPi` の `surge_mk2/docs/stereo_plan.md`、`surge_mk2/raspi/nodes/stereo_node.py` |
| 2D LiDAR SLAM | `AutonomousCar_RasPi` の `surge_mk2/slam2d/` |
| Pi ⇄ STM32 のプロトコル | `AutonomousCar_RasPi` の `surge_mk2/raspi/proto/protocol.toml` |
| 車両のパラメータ | `AutonomousCar_RasPi` の `surge_mk2/config/vehicle.toml` |
