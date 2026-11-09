# surge-mk2

自律走行ミニカー **SURGE Mark.2** の技術解説サイト（GitHub Pages: https://banbatakumi.github.io/surge-mk2/ ）。

| ディレクトリ | 中身 |
|---|---|
| `docs/` | ページの Markdown と素材（`assets/img` 写真、`assets/fig` 図、`assets/3d` 3D モデル） |
| `overrides/` | ホームのテンプレート |
| `includes/glossary.md` | 用語のツールチップ（全ページに自動で付く） |
| `sources/` | ハードウェアの一次資料（開発者への聞き取りの記録）。**ここに無いハードの事実は書かない** |
| `tools/check_links.py` | ビルド結果のリンク・アンカー・3D モデルの参照切れを調べる |
| `tools/cad/` | STEP から表示用の GLB を作るスクリプト |

## ビルド

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/zensical serve                 # http://127.0.0.1:8000
.venv/bin/zensical build --clean --strict
python3 tools/check_links.py
```

`master` に push すると `.github/workflows/pages.yml` が公開します（初回のみ Settings → Pages → Source を「GitHub Actions」に）。

## 書き方の約束

- 各ページは「要点」（`!!! summary`）→「しくみ」→「設計の詳細」の順に深くする。末尾に出典。
- 写真・図が未着の箇所は `!!! placeholder "写真 P-xx：…"` で置き、届いたら `<figure>` に差し替える。
- 数値の正はソース側（`vehicle.toml`・ファームの定数）。このサイトは写しで、確認した版を書く。
- STEP の ZIP（`cad/`）はリポジトリに入れず、GitHub Release に `surge_mk2_step.zip` として添付する。
