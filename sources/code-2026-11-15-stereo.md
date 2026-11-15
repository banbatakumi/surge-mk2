# コードの記録から取ったハードの事実（2026-11-15）前方ステレオカメラ

2026-11-13 のカメラの付け替え（前後 1 台ずつ → 前方の左右 2 台）は聞き取りに無い。
開発者の了承（2026-11-15）を得て、上位リポジトリの記録から次の事実だけを取った。製作方法・部品の形など、記録に無いことは書かない。

確認した版: `AutonomousCar_RasPi` `7c7054e`（2026-11-15）

| 事実 | 根拠 |
|---|---|
| 後ろに付けていた 1 台を前へ移し、前向きに左右 2 台を並べたステレオにした。台数は 2 台のまま。後方カメラは無い | `surge_mk2/CLAUDE.md`（「前後配置は 2026-11-13 にやめ、コードからも消した」）、`docs/stereo_plan.md` §1 |
| カメラは IMX219・160° 広角（魚眼）、CSI で Pi 5 につなぐ | `config/vehicle.toml` `[sensors.cam_front]` のコメント（`wide160sr`）、`CLAUDE.md` |
| 右が主カメラ（libcamera 0 番、`image/front`）、左は 1 番（`image/left`）。2026-11-12 にケーブルを左右で入れ替えた | `vehicle.toml`、`stereo_plan.md` §1・§2 |
| 基線は公称 75 mm（剛体の 1 枚の部品に固定）、校正値 76.2 mm | `stereo_plan.md` §1、`vehicle.toml` `[sensors.stereo] baseline_mm` |
| 取付位置 x=0.09 m、y=±0.0375 m、z=0.08 m（2026-11-12 の実測） | `vehicle.toml` `[sensors.cam_front.lenses.wide160sr]`・`[sensors.cam_left.lenses.wide160sl]` |
| 校正: 魚眼は各 13 枚（再投影誤差 0.131 / 0.125 px）、ステレオは 13 組（0.369 px、平行化後の縦ずれ 中央値 0.29 px） | `vehicle.toml` |
| 同期はソフトウェア同期。差が 0.5 ms 以内の組を `synced` とする | `stereo_plan.md` §2 |
| 左カメラの電流 +57 mA、照合込み +156 mA | `stereo_plan.md` §3、`PROGRESS.md` |
| LiDAR の取付の高さは 0.095 m（以前は 0.110 m と書いていた） | `vehicle.toml` `[sensors.lidar] z` |
| 床が見えるのは中央で約 1.1 m より先。画像の約 255 行より下には車体が写る | `stereo_plan.md`、`stereo_node.py` |
