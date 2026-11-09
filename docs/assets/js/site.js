// サイト共通の小さなスクリプト。
// - <model-viewer> があるページだけ、model-viewer 本体を読み込む（ホームはテンプレートが読む）
// - 3D の「組み立て / 分解」切り替えと、ホットスポットのクリックで該当の節へ飛ぶ
// - Fusion の埋め込みはクリックされるまで読み込まない（ページを重くしない）
(function () {
  var MV_SRC = "https://cdn.jsdelivr.net/npm/@google/model-viewer@4.4.0/dist/model-viewer.min.js";

  function init() {
    if (document.querySelector("model-viewer") && !customElements.get("model-viewer")
        && !document.querySelector('script[src="' + MV_SRC + '"]')) {
      var s = document.createElement("script");
      s.type = "module"; s.src = MV_SRC;
      document.head.appendChild(s);
    }

    document.querySelectorAll(".sg-3d").forEach(function (box) {
      var mv = box.querySelector("model-viewer");
      if (!mv) return;
      var srcs = { assembled: mv.getAttribute("src"), exploded: mv.dataset.srcExploded };
      box.querySelectorAll("button[data-view]").forEach(function (b) {
        b.addEventListener("click", function () {
          var v = b.dataset.view;
          if (!srcs[v]) return;
          mv.setAttribute("src", srcs[v]);
          box.querySelectorAll("button[data-view]").forEach(function (o) {
            o.setAttribute("aria-pressed", String(o === b));
          });
        });
      });
      box.querySelectorAll(".sg-hotspot[data-href]").forEach(function (h) {
        h.addEventListener("click", function () { location.href = h.dataset.href; });
      });
    });

    document.querySelectorAll(".sg-fusion[data-embed]").forEach(function (box) {
      var btn = box.querySelector(".sg-fusion__load");
      if (!btn) return;
      btn.addEventListener("click", function () {
        var f = document.createElement("iframe");
        f.src = box.dataset.embed;
        f.title = box.dataset.title || "Fusion の 3D ビューア";
        f.allowFullscreen = true;
        f.setAttribute("allow", "fullscreen");
        box.replaceChildren(f);
      });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
