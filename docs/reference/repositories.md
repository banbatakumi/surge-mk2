# リポジトリの案内

SURGE Mark.2 のソースは 3 つのリポジトリに分かれています。このサイト自体も別のリポジトリです。

| リポジトリ | 中身 | 最新のブランチ |
|---|---|---|
| [`AutonomousCar_RasPi`](https://github.com/banbatakumi/AutonomousCar_RasPi) | Raspberry Pi 5 側のソフト（`surge_mk2/`）。自動運転、SLAM、GUI、シミュレータ、校正のツール | `master` |
| [`AutonomousCar`](https://github.com/banbatakumi/AutonomousCar/tree/FW/MainBoard_V3) | STM32F446RE のファーム（`Program/MainF446RE_V3`）と、制御基板などの回路（`Circuit/`） | `FW/MainBoard_V3` |
| [`BLDC`](https://github.com/banbatakumi/BLDC/tree/FW/Program_V4) | モータドライバのファーム（`ProgramV4`）と基板（`CurcuitV1`〜`V4`） | `FW/Program_V4` |
| [`surge-mk2`](https://github.com/banbatakumi/surge-mk2) | このサイト | `master` |

!!! note "既定のブランチは最新ではない"
    `AutonomousCar` と `BLDC` は、既定のブランチ（`main`）が古い状態のままです。最新は上の表のブランチを見てください。

## どこから読むか

| 知りたいこと | 入口 |
|---|---|
| 車速制御・TC・ABS・トルクベクタリング | `AutonomousCar` の `Program/MainF446RE_V3/src/control/` |
| モータドライバの FOC と校正 | `BLDC` の `ProgramV4/docs/FOC.md` |
| 自動運転の方式 | `AutonomousCar_RasPi` の `surge_mk2/raspi/auto/` |
| 2D LiDAR SLAM | `AutonomousCar_RasPi` の `surge_mk2/slam2d/` |
| Pi ⇄ STM32 のプロトコル | `AutonomousCar_RasPi` の `surge_mk2/raspi/proto/protocol.toml` |
| 車両のパラメータ | `AutonomousCar_RasPi` の `surge_mk2/config/vehicle.toml` |
