import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const sharp=require('/Users/andrewsazonov/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
for(const p of ['/tmp/edi-grammar-review/image13.png','/tmp/edi-grammar-review/image14.png','/var/folders/ym/htbh7q790j50h0txr1w84fzr0000gq/T/TemporaryItems/NSIRD_screencaptureui_tVV88o/Screenshot 2026-11-09 at 08.29.01.png']) {
 const m=await sharp(p).metadata(); console.log(p,m.width,m.height,m.channels);
 if(p.includes('image13')){
  const {data,info}=await sharp(p).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const counts=new Map();
  for(let y=784;y<907;y++)for(let x=910;x<1156;x++) {
   const i=(y*info.width+x)*4;const c=Array.from(data.subarray(i,i+4)).join(',');counts.set(c,(counts.get(c)||0)+1);
  } console.log([...counts.entries()].sort((a,b)=>b[1]-a[1]).slice(0,12));
 }else if(p.includes('image14')){
 await sharp(p).extract({left:1300,top:90,width:650,height:80}).png().toFile('/tmp/edi-grammar-review/browser-original-crop.png');
 }else{
 await sharp(p).extract({left:1300,top:90,width:650,height:80}).png().toFile('/tmp/edi-grammar-review/browser-reference-crop.png');
 }
}
