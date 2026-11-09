#!/usr/bin/env python3
"""ビルド結果（build/）の中のリンク切れ・アンカー切れを調べる。

Zensical のビルドはページ内アンカーの存在までは確かめないので、出力した HTML を直接見る。
外部リンク（http/https）は見ない。切れが 1 つでもあれば終了コード 1。

    python3 tools/check_links.py [build ディレクトリ]
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASE = "/surge-mk2/"  # mkdocs.yml の site_url のパス部分


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a and a["id"]:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        # 3D のラベル（クリックで移動する先）と、3D モデル・画像の読み込み先も調べる
        for key in ("data-href", "data-src-exploded"):
            if a.get(key):
                self.links.append(a[key])
        if tag in ("model-viewer", "img") and a.get("src"):
            self.links.append(a["src"])


def _parse(path: Path) -> _Collector:
    c = _Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "build").resolve()
    pages = {p: _parse(p) for p in root.rglob("*.html")}
    bad: list[str] = []
    for page, info in pages.items():
        for href in info.links:
            u = urlsplit(href)
            if u.scheme or href.startswith("//") or href.startswith("mailto:"):
                continue
            if not u.path:  # 同じページ内のアンカー
                target = page
            elif u.path.startswith("/"):  # 404.html などの絶対パス（公開 URL の /surge-mk2/ 始まり）
                rel = unquote(u.path)[len(BASE):] if unquote(u.path).startswith(BASE) else None
                if rel is None:
                    bad.append(f"{page.relative_to(root)}: サイトの外を指す絶対パス {href}")
                    continue
                target = (root / rel).resolve()
                if target.is_dir():
                    target = target / "index.html"
            else:
                target = (page.parent / unquote(u.path)).resolve()
                if target.is_dir():
                    target = target / "index.html"
            if not target.exists():
                bad.append(f"{page.relative_to(root)}: リンク先が無い {href}")
                continue
            frag = unquote(u.fragment)
            if frag and target.suffix == ".html":
                ids = pages[target].ids if target in pages else _parse(target).ids
                if frag not in ids:
                    bad.append(f"{page.relative_to(root)}: アンカーが無い {href}")
    for b in sorted(set(bad)):
        print(b)
    print(f"{len(pages)} ページを確認、切れ {len(set(bad))} 件")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
