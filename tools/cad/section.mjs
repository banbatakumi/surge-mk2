// 3D モデル（GLB）の一部を、Z（前後）が一定の平面で切った断面を SVG 用の多角形として書き出す。
// 使い方: node section.mjs raw.glb NodeName z_plane_m out.json
// 出力: [{ name, part, loops: [[[x,y],...], ...] }]（x=左右・y=上下、単位 m、ワールド座標）
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import fs from 'fs';
const [,, inp, nodeName, zArg, out] = process.argv;
const Z = +zArg;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(inp);
const root = doc.getRoot().listNodes().find(n => n.getName() === nodeName);
if (!root) throw new Error('not found ' + nodeName);
const mul = (m, p) => [m[0]*p[0]+m[4]*p[1]+m[8]*p[2]+m[12], m[1]*p[0]+m[5]*p[1]+m[9]*p[2]+m[13], m[2]*p[0]+m[6]*p[1]+m[10]*p[2]+m[14]];
const results = [];
function walk(n, path) {
  const mesh = n.getMesh();
  if (mesh) {
    const wm = n.getWorldMatrix();
    const segs = [];
    for (const prim of mesh.listPrimitives()) {
      const pos = prim.getAttribute('POSITION'); const idx = prim.getIndices();
      const cnt = idx ? idx.getCount() : pos.getCount();
      const v = i => mul(wm, pos.getElement(idx ? idx.getScalar(i) : i, []));
      for (let t = 0; t < cnt; t += 3) {
        const P = [v(t), v(t+1), v(t+2)];
        const pts = [];
        for (let e = 0; e < 3; e++) {
          const a = P[e], b = P[(e+1)%3];
          const da = a[2]-Z, db = b[2]-Z;
          if ((da < 0) !== (db < 0)) { const s = da/(da-db); pts.push([a[0]+s*(b[0]-a[0]), a[1]+s*(b[1]-a[1])]); }
        }
        if (pts.length === 2) segs.push(pts);
      }
    }
    if (segs.length) {
      // 端点をつないで閉じた輪にする（1 µm 単位で丸めて同一視）
      const key = p => Math.round(p[0]*1e6) + ',' + Math.round(p[1]*1e6);
      const adj = new Map();
      segs.forEach((s, i) => s.forEach((p, j) => { const k = key(p); if (!adj.has(k)) adj.set(k, []); adj.get(k).push([i, j]); }));
      const used = new Uint8Array(segs.length); const loops = [];
      for (let i = 0; i < segs.length; i++) {
        if (used[i]) continue;
        used[i] = 1; const loop = [segs[i][0], segs[i][1]]; let cur = segs[i][1];
        for (let guard = 0; guard < segs.length; guard++) {
          const cand = (adj.get(key(cur)) || []).find(([k]) => !used[k]);
          if (!cand) break;
          const [k, j] = cand; used[k] = 1; cur = segs[k][1-j]; loop.push(cur);
        }
        if (loop.length > 3) loops.push(loop);
      }
      results.push({ name: n.getName(), part: path.join('/'), loops });
    }
  }
  n.listChildren().forEach(c => walk(c, [...path, c.getName()]));
}
walk(root, [root.getName()]);
fs.writeFileSync(out, JSON.stringify(results));
console.log(results.map(r => `${r.part}  loops=${r.loops.length}`).join('\n'));
