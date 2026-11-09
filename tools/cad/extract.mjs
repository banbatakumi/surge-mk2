// 使い方: node extract.mjs in.glb out.glb NodeName [explodeGap_m]
import { NodeIO, getBounds } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { prune } from '@gltf-transform/functions';
const [,, inp, out, name, gapArg] = process.argv;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(inp);
const root = doc.getRoot();
const scene = root.listScenes()[0];
const target = root.listNodes().find(n => n.getName() === name);
if (!target) throw new Error('not found ' + name);
const wm = target.getWorldMatrix();
for (const c of scene.listChildren()) scene.removeChild(c);
target.getParentNode()?.removeChild(target);
target.setMatrix(wm);
scene.addChild(target);
const gap = gapArg ? +gapArg : 0;
if (gap) {
  const motor = target.listChildren().find(c => c.getName().startsWith('BLDC'));
  const mb = getBounds(motor);
  const ext = [0,1,2].map(i => mb.max[i]-mb.min[i]);
  const ax = ext.indexOf(Math.min(...ext));           // モータ（円盤）が最も薄い向き＝車軸
  const ub = getBounds(target); const uc = (ub.min[ax]+ub.max[ax])/2;
  const kids = target.listChildren().map(c => { const b = getBounds(c); return { c, z: (b.min[ax]+b.max[ax])/2 }; });
  // 外側（車輪）→ モータ → マウント → カバー → 基板 → カバー の順に車軸方向へ離す。
  // ボルトと腕はマウントと一緒に動かす（バラバラに飛ぶと構造が読めない）。
  const RANK = { 'Rear:1': -1, 'BLDC5010:1': 0, 'MotorMount_V2:1': 1, 'Fasteners:1': 1, 'Arm:1': 1, 'PCB_Cover:1': 2, 'CurcuitV4:1': 3, 'PCB_Cover_:1': 4 };
  const mi = 0;
  kids.forEach(k => { k.rank = RANK[k.c.getName()] ?? 0; });
  const sign = Math.sign(kids.find(k=>k.rank===1).z - kids.find(k=>k.rank===0).z) || 1;
  // 親の回転を考慮して、ワールドの車軸方向へ動かす: 子のローカル平行移動を、親の逆行列で変換
  const inv = invert(target.getWorldMatrix());
  kids.forEach((k, i) => {
    const d = [0,0,0]; d[ax] = sign * k.rank * gap;
    const l = [inv[0]*d[0]+inv[4]*d[1]+inv[8]*d[2], inv[1]*d[0]+inv[5]*d[1]+inv[9]*d[2], inv[2]*d[0]+inv[6]*d[1]+inv[10]*d[2]];
    const t = k.c.getTranslation(); k.c.setTranslation([t[0]+l[0], t[1]+l[1], t[2]+l[2]]);
    console.log(k.c.getName(), k.rank);
  });
  console.log('axis', ax);
}
await doc.transform(prune());
await io.write(out, doc);
function invert(m){ // 4x4 column-major, affine
  const [a,b,c,,d,e,f,,g,h,i] = m; const det = a*(e*i-f*h)-d*(b*i-c*h)+g*(b*f-c*e);
  return [(e*i-f*h)/det,(c*h-b*i)/det,(b*f-c*e)/det,0,(f*g-d*i)/det,(a*i-c*g)/det,(c*d-a*f)/det,0,(d*h-e*g)/det,(b*g-a*h)/det,(a*e-b*d)/det,0,0,0,0,1];
}
