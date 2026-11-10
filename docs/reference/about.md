# このサイトについて

## 目的と範囲

SURGE Mark.2 のハードウェア・制御・システム設計・自動運転の考え方を、作った人以外にも伝わる形で残すためのサイトです。

- **扱う**: ハードウェア（インホイール・ダイレクトドライブ、自作のモータドライバと基板、シャシー、センサ、電源、部品表、3D データ）、STM32 ファームウェア（駆動制御・TC・ABS・トルクベクタリング・安全層）、Pi ⇄ STM32 のプロトコル、Raspberry Pi 側のソフトウェア（走行モード、SLAM、レーシングライン）、開発・検証の道具。
- **扱わない**: V1 の手動遠隔操縦システム（`robotcar/`）。

## どうやって書いたか

既存のドキュメントは古くなっていたり誤りを含んでいることがあるため、**ソースコードを読み直して**書きました。

- 数値は、定数の定義・パラメータ表・`vehicle.toml` から取りました。ドキュメントの数値は、そのまま写していません。
- 設計の理由は、ソースコード中のコメントと開発記録（`PROGRESS.md`）から取り、**出どころを各ページの末尾か本文に示して**います。
- 「実機で確認した」と言えるものと、シミュレータ・机上の値は分けて書きました（[検証状況](../development/status.md)）。
  開発者本人の記録を引いている箇所は、そう書いてあります。**第三者による再現確認ではありません。**
- 実機の走行記録そのもの（mcap）は、このサイトの作成では見ていません。実機の数値は開発記録の引用です。

### 数値を複製しない

リポジトリの方針は「同じ数字を 2 箇所に書くと必ず片方が古くなる」です。このサイトも、仕様の**正を持ちません。**
プロトコルのバイト配置は [`protocol.toml`][protocol-toml]、車両パラメータは [`vehicle.toml`][vehicle-toml]、制御の定数は `drive.h` / `control_params.h` を見てください。
ページ内の数値は、読むときの目安として、確認した版を明記して載せています。

## 数値と記述の信頼度

このサイトは、**ソースコードを正として**書いています。数値や挙動は、各ページの末尾にある
参照先（ファイルと関数名）で確かめられます。それでも、次の区別は必ず見てください。

!!! success "【実機確認】"
    実車の走行記録・計測で確かめられている。

!!! info "【シム／ホスト検証】"
    シミュレータや、ファームをホストでコンパイルした閉ループで確かめている。実車では未確認。

!!! warning "【未検証】"
    計算や設計上の見積もり（机上値）。実車で確かめていない。

!!! note "【設計の説明】"
    動作の優劣は主張せず、「こう作ってある」とその理由だけを述べている。

どの機能がどれに当たるかは [検証状況](../development/status.md) にまとめています。

## 対象の版

| リポジトリ | 内容 | 確認したコミット |
|---|---|---|
| [`AutonomousCar_RasPi`][raspi-repo] | Raspberry Pi 側（`surge_mk2/`） | `2d0a44e`（2026-11-09） |
| [`AutonomousCar`][fw-repo] | STM32 ファーム（`Program/MainF446RE_V3`、ブランチ `FW/MainBoard_V3`）と基板（`Circuit/`） | ファーム `6b5bdb3`（2026-11-09）。基板は `213c0cc`（2026-11-02） |
| [`BLDC`][bldc-repo] | モータドライバのファーム（`ProgramV4`）と基板（`CurcuitV1`〜`V4`）。ブランチ `FW/Program_V4` | `1668666`（2026-11-09） |

開発は続いているため、リンク先のコードはこのサイトより新しくなっていることがあります。
**食い違いを見つけたらコードを信じてください。** 直し方は下の「更新のしかた」にあります。

ハードウェアの節（構造・製作方法・設計の理由）は、**開発者への聞き取り（2026-11-09）**を一次資料にしています。聞き取りにない事実は書いていません。

## 更新のしかた

サイトの元は [`surge-mk2`][site-repo] リポジトリの `docs/` にある Markdown です。ビルドには [Zensical](https://zensical.org/) を使います。

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/zensical serve        # http://127.0.0.1:8000 でプレビュー
.venv/bin/zensical build        # build/ に書き出す
python3 tools/check_links.py    # ページ内リンク・アンカーの切れを調べる
```

`master` に push すると、GitHub Actions がビルドして GitHub Pages に公開します。

**コードを変えたときに見直すページ**

| 変えたもの | 見直すページ |
|---|---|
| MD の `config.h`・`docs/`、`CurcuitV*` | [自作モータドライバ](../hardware/motor-driver.md)、[インホイール駆動](../hardware/in-wheel-drive.md) |
| `Circuit/MainBoard_*` | [電装と電源](../hardware/electronics.md) |
| `vehicle.toml` の寸法・`steer_link_*`・`[sensors.*]` | [シャシー](../hardware/chassis.md)、[ステアリング](../hardware/steering.md)、[センサ](../hardware/sensors.md)、[主要諸元](specs.md) |
| 3D モデル（Fusion） | [3D データ](../hardware/3d-model.md)（`tools/cad/` の手順で GLB を作り直す） |
| `drive.c` / `drive.h` / `control_params.h` / `speed_kf.c` / `encoder_direction.c` | [駆動制御](../control/drive.md)、[スリップ制御](../control/traction.md) |
| `torque_vectoring.c` | [トルクベクタリング](../control/torque-vectoring.md) |
| `vehicle.c` / `heartbeat.c` / `power.h` / `auto_stop_path.c` | [安全層](../control/safety.md) |
| `protocol.toml` / `ras_link.h` | [UART プロトコル](../control/protocol.md) |
| `io_node.py` / `telemetry_node.py` | [上位の安全設計](../autonomy/safety.md)、[ノード構成](../autonomy/index.md) |
| `raspi/setup/install_services.sh` | [システム構成](../about-car/system.md) |
| `ml_cam_e2e/` / `ml_lidar/` / `ml_cam/` | [模倣学習](../autonomy/modes/imitation.md)、[強化学習](../autonomy/modes/reinforcement.md)、[カメラ](../autonomy/modes/camera.md)。拡張の図は `tools/fig_yaw_aug.py` で作り直す |
| `gui/` / `tools/launcher.py` | [操作画面](../development/gui.md)、[補助ツール](../development/tools.md) |
| `raspi/auto/` / `raspi/nav/` / `slam2d/` | [走行モード](../autonomy/modes/index.md)、[地図](../autonomy/mapping.md)、[レーシングライン](../autonomy/raceline.md)、[追従](../autonomy/tracking.md) |
| `raspi/nav/_native.c` / `slam2d/core/_native.c` | [C による高速化](../development/performance.md) |
| `sim/` / `tools/fwsim` / `tools/calib` / `.github/workflows/ci.yml` | [検証の仕組み](../development/workflow.md) |
| 実機で何かを確かめた・`vehicle.toml` の校正値を書き換えた | [検証状況](../development/status.md) |

## この作成中に見つけた食い違い

既存の文書やコードのコメントと、実際のコードが合っていなかった箇所です（`19291eb` / `2a2e9a8` の時点で見つけ、`2d0a44e` / `6b5bdb3` で確かめ直した）。サイトは**コードの側**に合わせて書いています。

| 箇所 | 内容 |
|---|---|
| ファーム `drive.h` の API コメント | **解消済み。** 以前は `Drive_SetTractionControlEnabled` に「既定は有効」、`TorqueVectoring_Init` に「初期状態は有効」とあったが、実装はどちらも無効で初期化する。今のコメントはどちらも「既定は無効」 |
| ファーム `docs/README.md` と `CLAUDE.md` | **解消済み。** 以前は現行版を古い版番号としていた。今の `CLAUDE.md` は `0x001D`（v0.29）でコードと一致し、版ごとの差分の文書は `docs/archive/` へ移された |
| 開発記録とファームのソース | **解消済み。** 以前は `PROGRESS.md`（2026-10-14）の「再 ARM の規則（`rearm_required`）」が、確認したファームのコミットに見当たらなかった。今のファームには `vehicle.c` に実装がある（[安全層](../control/safety.md#再-arm-の扱い)） |
| 開発記録とファームのリポジトリ | `PROGRESS.md`「現在の状態」はファームの HEAD を `99f7c94`（未 push）としているが、確認した時点の HEAD は `6b5bdb3` で、`origin` と一致していた（その後の 2 コミットは文書・コメントの整理） |
| ファームのリポジトリの既定ブランチ | `main` にもファームはあるが最新ではない（最新は `FW/MainBoard_V3`） |
| `vehicle.toml` の `mu` | `[sim]` は 0.42（シムの横グリップ。`[limits]` が無いときの予備）、`[control.plant]` は 1.32（校正 7 のタイヤモデル）。用途が違う値だが、同じ名前で食い違っている |
| Pi への OpenCV の導入 | `slam2d/README.md` は Pi 5 に `opencv-contrib-python-headless` が入っていると書き、`cam_e2e_preproc.py` は「Pi には OpenCV も Pillow も入れていない」と書く。`requirements.txt`（開発）には OpenCV があり、`requirements.lock.txt`（実機）には見当たらない。どちらが正しいかは確定できなかった |

## セキュリティについて

このサイトの本文には、認証情報（パスワード・鍵・トークン）、IP アドレス、実際のホスト名、個人の氏名は載せていません。

- 共有トークンは `config/secret.txt`（`.gitignore` 済み）か環境変数から読む仕組みで、リポジトリには含まれません。
- 制御用の API は既定で `127.0.0.1` にしか開かず、外へ出すときは明示が要ります（[上位の安全設計](../autonomy/safety.md#公開面の守り方)）。

リポジトリ全体の公開前の確認は、サイトの範囲外です。

## 作った人

SURGE Mark.2 の開発者が、ほかの制作物（SURGE Mark.1、ロボット競技の機体など）を [ポートフォリオ](https://banbatakumi.github.io/) にまとめています。

## 連絡・訂正

誤りを見つけたら、リポジトリの issue かプルリクエストでお知らせください。**コードと食い違っていたら、コードが正です。**

[protocol-toml]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/raspi/proto/protocol.toml
[vehicle-toml]: https://github.com/banbatakumi/AutonomousCar_RasPi/blob/master/surge_mk2/config/vehicle.toml
[site-repo]: https://github.com/banbatakumi/surge-mk2
[raspi-repo]: https://github.com/banbatakumi/AutonomousCar_RasPi
[fw-repo]: https://github.com/banbatakumi/AutonomousCar/tree/FW/MainBoard_V3
[bldc-repo]: https://github.com/banbatakumi/BLDC/tree/FW/Program_V4
