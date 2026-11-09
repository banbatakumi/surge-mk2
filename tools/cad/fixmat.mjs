// OpenCASCADE の glTF 書き出しは全マテリアルを metallic=1・roughness=1 にするので、
// 樹脂の部品まで「暗い金属」に見える。樹脂らしい値に直し、真っ黒は少しだけ持ち上げる。
// 使い方: node fixmat.mjs in.glb out.glb
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
const [,, inp, out] = process.argv;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(inp);
const MIN_LINEAR = 0.03;    // 真っ黒（線形 0.01）→ sRGB で #303030 程度
for (const m of doc.getRoot().listMaterials()) {
  const [r, g, b, a] = m.getBaseColorFactor();
  const mx = Math.max(r, g, b);
  const k = mx < MIN_LINEAR ? MIN_LINEAR / Math.max(mx, 1e-4) : 1;
  m.setBaseColorFactor([Math.min(r * k, 1), Math.min(g * k, 1), Math.min(b * k, 1), a]);
  m.setMetallicFactor(0);
  m.setRoughnessFactor(0.5);
}
await io.write(out, doc);
