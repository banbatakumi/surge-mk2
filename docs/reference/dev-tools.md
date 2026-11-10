# 開発に使ったツール

!!! summary "要点"
    - SURGE Mark.2 の設計・製作・ソフトの開発に使った道具を、区分ごとにまとめました。
    - ファームは STM32CubeMX で初期設定を作り、GCC と Makefile でビルドして ST-LINK で書き込んでいます。
    - Raspberry Pi 側は Python が中心で、重い所だけ C です。操作画面は React で書いています。

!!! note "【出典】"
    ソフトの道具は、各リポジトリの依存の定義（`requirements.txt`・`package.json`・`Makefile`・`.ioc`）と CI の設定から書き出しています。
    設計・製作・書き込み器・エディタは、本人への聞き取り（2026-11-10）によるものです。確認した版: 上位 `2d0a44e`、ファーム `6b5bdb3`。

## 設計・製作

| 用途 | ツール |
|---|---|
| 機械の設計（3D CAD） | Autodesk Fusion |
| 回路・基板の設計 | KiCad |
| 基板の製造 | JLCPCB に発注 |
| 樹脂部品（ホイール・タイヤなど） | 3D プリンタ（[シャシー](../hardware/chassis.md)） |

## マイコンのファーム（STM32）

制御基板（STM32F446RE）とモータドライバ（STM32F303K8）で同じ作り方です。

| 用途 | ツール |
|---|---|
| ピン・周辺機能の初期設定とコードの生成 | STM32CubeMX（`.ioc`） |
| コンパイラとビルド | GCC（`arm-none-eabi-gcc`）＋ Makefile |
| 書き込み | STM32CubeProgrammer の CLI（`STM32_Programmer_CLI`）、ST-LINK/V2 で SWD 接続 |
| モータドライバの単体の操作 | 自作の小さな GUI（Python ＋ Tkinter ＋ pySerial） |
| ファームの制御ロジックの検証 | ファームの `src/control` をそのまま Mac でコンパイルして閉ループで回す自作ツール `tools/fwsim`（[検証の仕組み](../development/workflow.md)） |

## Raspberry Pi 側のソフト

| 用途 | ツール |
|---|---|
| 言語 | Python（重い内側だけ C。[C による高速化](../development/performance.md)） |
| 数値計算・画像 | numpy、OpenCV |
| プロセス間の通信 | ZeroMQ（PUB/SUB）、msgspec（メッセージの定義と直列化） |
| STM32 との通信 | pySerial |
| 操作画面との通信 | websockets |
| 学習したモデルの推論 | ONNX Runtime |
| カメラ・GPIO | picamera2、gpiozero（Raspberry Pi 5 のため `RPi.GPIO` は使わない） |
| SLAM のループ閉じの最適化 | g2o（`g2opy`） |
| 走行の記録 | MCAP（Foxglove でも開ける形式） |

## 操作画面（Web GUI）

| 用途 | ツール |
|---|---|
| 言語・フレームワーク | TypeScript、React |
| ビルド | Vite |
| グラフ | uPlot |
| 状態の管理 | zustand |
| 通信のデータ形式 | MessagePack（`@msgpack/msgpack`） |

## 補助ツール・シミュレータ・学習

| 用途 | ツール |
|---|---|
| 補助ツールの窓（ランチャー・校正・解析・学習の操作パネル） | Tkinter |
| シミュレータの俯瞰ビュー | pygame |
| 校正の当てはめ・グラフ | scipy、matplotlib |
| 記録の閲覧 | Foxglove |
| 模倣学習・セグメンテーション | PyTorch、torchvision |
| 半自動のアノテーション | Segment Anything（SAM） |
| 強化学習 | Stable-Baselines3（PPO）、Gymnasium |
| モデルの書き出し | ONNX |

## 開発環境と検証

| 用途 | ツール |
|---|---|
| エディタ | Visual Studio Code |
| ソースの管理 | Git、GitHub |
| 自動テスト | GitHub Actions で pytest・ruff（Python）と、GUI の型検査・ビルドを回す |
| AI によるコーディング支援 | Claude Code、GitHub Copilot |
| このサイト | Zensical、GitHub Pages |

<div class="sg-next" markdown>
<div markdown>
隣のしくみへ

- [リポジトリの案内](repositories.md)
- [補助ツール](../development/tools.md)
</div>
<div markdown>
さらに深く

- [検証の仕組み](../development/workflow.md)
- [C による高速化](../development/performance.md)
</div>
</div>
