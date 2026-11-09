# 走行モード（planner）

!!! summary "要点"
    - 自動運転の方式は、すべて **`Planner` という同じ形**にはめてあり、GUI から切り替えられます。
    - 守る約束は 4 つだけで、新しい方式はファイル 1 つと一覧への 1 行で足せます。
    - 方式ごとの中身は、仕組みの近いものをまとめた 7 つのページで説明します（下の表）。


!!! note "【設計の説明】"
    対象: [`raspi/auto/`][auto-dir]。確認した版: 上位 `2d0a44e`（2026-11-09）。各モードの検証の状態は、それぞれのページの冒頭に書いています。

## planner の約束

自動運転の走らせ方は、すべて `Planner` の形にはめてあり、GUI から選べます（[`base.py`][base-py]）。**守る約束は 4 つだけ**です。

1. **`plan()` は状態を持ってよいが、`reset()` で完全に初期化できる。**
   モードを切り替えたときに前のモードの舵の平滑化が残っていると、engage した瞬間に前回の続きから舵が動き出すため。
2. **戻り値は `AutoState`。指令（`target_speed` / `target_steer` / `brake`）と、その理由（`reason`）を必ず同時に返す。**
   「なぜ止まったか」が後から分からないのが、デバッグを最も消耗させる。
3. **走ってよいか分からないときは `ready=False`。迷ったら止まる。** `ready=False` は `planning_node` が制動指令に読み替える。
4. **パラメータは `params` に宣言する。** GUI のスライダはこの宣言から自動生成されるので、planner を足しても GUI は 1 行も変えなくてよい。

新しい走らせ方を足す手順は 2 つ（`raspi/auto/<名前>.py` を書く、`registry.py` の `PLANNERS` に 1 行足す）だけです。
**id は保存キーでもある**（`config/auto.json` と `localStorage` がこの文字列でパラメータを覚える）ので、後から変えると設定が黙って既定値に戻ります。

単位は SI のまま（距離 [m]、角度 [rad]、車両座標・反時計回りが正）。度に直すのは表示用の `*_deg` だけです。

**計画は入力が来たときだけ**回します。LiDAR は 10 Hz、`auto/cmd` の発行は 50 Hz なので、同じ周で 5 回計算しても答えは変わらないため。

**どの planner も「固定距離のハード停止」は持ちません。** 近づきすぎたら止める役目は、STM32 の `auto_stop`
（速度に応じて伸びる動的停止距離、[自動停止](../../control/safety.md#自動停止)）に任せています。
正面が詰まったときに減速するのは、緊急停止ではなく走行の一部として残してあります。

## 一覧

| id | 名前 | 入力 | 地図 | 概要 |
|---|---|---|---|---|
| [`ftg`](lidar-reactive.md#follow-the-gap) | Follow the Gap | LiDAR | 不要 | 最も広く空いている方向へ |
| [`de`](lidar-reactive.md#disparity-extender) | Disparity Extender | LiDAR | 不要 | 通れない隙間を先に塞いでから、一番遠い帯を狙う |
| [`dp`](lidar-reactive.md#disparity-pursuit) | Disparity Pursuit | LiDAR | 不要 | DE の安全マージン ＋ FTG の Pure Pursuit 舵角 ＋ ヒステリシス |
| [`ftg_cam`](camera.md#follow-the-gapカメラ) | Follow the Gap（カメラ） | カメラ（擬似 LiDAR） | 不要 | `ftg` を擬似 LiDAR（`scan/cam`）で流用 |
| [`cam_centerline`](camera.md#カメラ中心線) | カメラ中心線 | カメラ | 不要 | 走行可能領域の回廊の中心線を追従 |
| [`cam_e2e`](imitation.md) | カメラ E2E | カメラ | 不要 | 画像から操舵を直接回帰（模倣学習） |
| [`line_trace`](camera.md#ライントレース) | ライントレース | カメラ | 不要 | 白線を追う |
| [`e2e_lidar`](reinforcement.md) | LiDAR E2E | LiDAR | 不要 | 強化学習した方策（ONNX） |
| [`slam2d_route`](map-driving.md) | 経路選択走行 | LiDAR ＋ IMU ＋ 車速 | **作る** | 地図→道路グラフ→経路→周回 |
| [`follow_object`](follow.md) | 対象追従 | カメラ ＋ LiDAR | 不要 | 映像上で選んだ対象との車間距離を保つ |
| [`park_to_point`](park.md) | 駐車 | LiDAR | 局所のみ | 指定位置・向きへ自律的に接近して停止 |
| `calib_*` | 車両の校正 | — | — | 校正専用の試験。自動運転タブには出ない（[検証の仕組み](../../development/workflow.md)） |

開発記録（2026-10-14）によれば、GUI の自動運転モードからは `slam2d_raceline`（レーシングライン）が外され、**`slam2d_route` に一本化**されています
（コード上は `PLANNERS` に両方が登録されたままです）。後者は前者の派生で、分岐のあるコースにも対応します（[地図と自己位置推定](../mapping.md)、[レーシングライン](../raceline.md)）。

## 系統ごとのページ

| ページ | モード | 一言で |
|---|---|---|
| [LiDAR で空いている方向へ](lidar-reactive.md) | `ftg`・`de`・`dp` | 地図なし。点群から毎周期「どこへ向かうか」を決める |
| [カメラで道を見る](camera.md) | `ftg_cam`・`cam_centerline`・`line_trace` | 走行可能な領域や白線を認識し、地面の座標に直して追う |
| [模倣学習（カメラ E2E）](imitation.md) | `cam_e2e` | 手本の運転を真似て、画像から舵を直接出す |
| [強化学習（LiDAR E2E）](reinforcement.md) | `e2e_lidar` | シミュレータで試行錯誤した方策で、点群から舵と速度を出す |
| [地図を作って走る](map-driving.md) | `slam2d_route` | 地図・自己位置・走行ライン・経路選択・追い抜き |
| [対象を追う](follow.md) | `follow_object` | 映像で選んだ相手との距離を保って付いていく |
| [駐車する](park.md) | `park_to_point` | クリックした位置と向きへ、障害物を避けて入る |

!!! placeholder "画面 S-01：自動運転タブのモード選択とパラメータ"
    自動運転タブで、モードの一覧を開いた状態と、あるモード（例: Disparity Extender）のパラメータのスライダが見える状態。
    「パラメータを宣言すれば GUI のスライダが自動で出る」ことが伝わる画面。

[auto-dir]: https://github.com/banbatakumi/AutonomousCar_RasPi/tree/master/surge_mk2/raspi/auto
[base-py]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/raspi/auto/base.py
