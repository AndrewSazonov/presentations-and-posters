import {createRequire} from 'node:module';
import fs from 'node:fs/promises';
const require=createRequire(import.meta.url);
const sharp=require('/Users/andrewsazonov/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const out=new URL('./',import.meta.url).pathname;
const original=await sharp('/tmp/edi-grammar-review/image13.png').ensureAlpha().raw().toBuffer({resolveWithObject:true});
const edited=Buffer.from(original.data);
const old=[185,121,34], target=[204,73,55];
const backgrounds=[[255,255,255],[174,196,151],[185,167,207]];
const box={left:910,top:783,right:1157,bottom:908};
let changed=0;const bounds=[Infinity,Infinity,-1,-1];
for(let y=box.top;y<box.bottom;y++)for(let x=box.left;x<box.right;x++) {
 const off=(y*original.info.width+x)*4;
 const p=Array.from(original.data.subarray(off,off+3));
 // Decompose existing antialiasing into original box fill + existing foreground/background.
 // Only recolour pixels which contain this box's fill; keep white text and stripe colours intact.
 let best=null;
 for(const bg of backgrounds){
  const v=old.map((c,k)=>c-bg[k]);
  const denom=v.reduce((s,c)=>s+c*c,0);
  const a=Math.max(0,Math.min(1,p.reduce((s,c,k)=>s+(c-bg[k])*v[k],0)/denom));
  const err=Math.max(...p.map((c,k)=>Math.abs(c-(bg[k]+a*v[k]))));
  if(!best||err<best.err)best={bg,a,err};
 }
 if(best.err<=2.2 && best.a>0.003){
  let different=false;
  for(let k=0;k<3;k++){
   const c=Math.max(0,Math.min(255,Math.round(p[k]+best.a*(target[k]-old[k]))));
   edited[off+k]=c;different ||= c!==p[k];
  }
  if(different){changed++;bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);}
 }
}
await sharp(edited,{raw:original.info}).removeAlpha().png().toFile(out+'diagram-coral.png');
let outside=0;
for(let y=0;y<original.info.height;y++)for(let x=0;x<original.info.width;x++) {
 if(x>=box.left&&x<box.right&&y>=box.top&&y<box.bottom)continue;
 const off=(y*original.info.width+x)*4;
 for(let k=0;k<4;k++)if(original.data[off+k]!==edited[off+k]){outside++;break;}
}
const browser=await sharp('/tmp/edi-grammar-review/image14.png').ensureAlpha().raw().toBuffer({resolveWithObject:true});
const ref=await sharp('/var/folders/ym/htbh7q790j50h0txr1w84fzr0000gq/T/TemporaryItems/NSIRD_screencaptureui_tVV88o/Screenshot 2026-11-09 at 08.29.01.png').ensureAlpha().raw().toBuffer({resolveWithObject:true});
const address={left:1440,top:108,width:400,height:46};
const corrected=Buffer.from(browser.data);
let urlPixels=0;
for(let y=address.top;y<address.top+address.height;y++)for(let x=address.left;x<address.left+address.width;x++){
 const i=(y*browser.info.width+x)*4, j=(y*ref.info.width+x)*4;
 for(let k=0;k<4;k++) {if(corrected[i+k]!==ref.data[j+k])urlPixels++;corrected[i+k]=ref.data[j+k];}
}
await sharp(corrected,{raw:browser.info}).png().toFile(out+'browser-address-corrected.png');
await sharp(edited,{raw:original.info}).extract({left:875,top:760,width:320,height:180}).png().toFile(out+'box-detail.png');
await sharp(corrected,{raw:browser.info}).extract({left:1300,top:90,width:650,height:80}).png().toFile(out+'address-detail.png');
const receipt={diagram:{size:[original.info.width,original.info.height],changedPixels:changed,changedBounds:bounds,pixelsChangedOutsideBox:outside,newFill:'#CC4937'},browser:{size:[browser.info.width,browser.info.height],patch:address,changedChannels:urlPixels,pixelsChangedOutsideAddress:0}};
await fs.writeFile(out+'pixel-check.json',JSON.stringify(receipt,null,2));
console.log(receipt);
