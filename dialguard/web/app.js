'use strict';
const $ = id => document.getElementById(id);
let image = new Image(), mode = null, lastResult = null;
const canvas = $('image'), ctx = canvas.getContext('2d');
function calibration() {
  return {cx:Number($('cx').value), cy:Number($('cy').value), radius:Number($('radius-value').value),
    minimum:Number($('minimum').value), maximum:Number($('maximum').value),
    start_deg:Number($('start').value), sweep_deg:Number($('sweep').value), unit:$('unit').value,
    review_above:$('threshold').value === '' ? null : Number($('threshold').value)};
}
function draw() {
  canvas.width=image.width; canvas.height=image.height; ctx.drawImage(image,0,0);
  const c=calibration(); ctx.strokeStyle='#2c9061';ctx.lineWidth=Math.max(2,image.width/200);
  ctx.beginPath();ctx.arc(c.cx*image.width,c.cy*image.height,c.radius*Math.min(image.width,image.height),0,Math.PI*2);ctx.stroke();
  ctx.beginPath();ctx.arc(c.cx*image.width,c.cy*image.height,5,0,Math.PI*2);ctx.stroke();
}
function showError(message) { $('status').textContent='CHECK INPUT';$('status').className='status retake';$('message').textContent=message; }
function clearResult() {
  lastResult=null;$('status').textContent='READY TO INSPECT';$('status').className='status idle';$('reading').textContent='—';
  for(const id of ['annotated','metrics','trace-details','download']) $(id).hidden=true;
  $('message').textContent='Calibration changed or a new image loaded. Inspect again to update the evidence.';
}
function loadImage(source,label) {
  return new Promise((resolve,reject)=>{
    const next=new Image(); next.onload=()=>{image=next;draw();clearResult();$('image-label').textContent=label;resolve();};
    next.onerror=()=>reject(new Error('The image could not be opened.'));next.src=source;
  });
}
async function sample(name) {
  try { await loadImage('/sample/'+name,'Generated sample · '+name); }
  catch(e) {showError(e.message);}
}
$('upload').addEventListener('change',async e=>{
  const file=e.target.files[0]; if(!file)return;
  if(!['image/png','image/jpeg'].includes(file.type)||file.size>1572864){showError('Choose a PNG/JPEG photo up to 1.5 MiB.');return;}
  const url=URL.createObjectURL(file);
  try {await loadImage(url,file.name);$('message').textContent='Set the hub and rim, then check the scale. Use a straight-on photograph.';}
  catch(e){showError(e.message);}finally{URL.revokeObjectURL(url);}
});
$('center').onclick=()=>{mode='center';$('click-hint').textContent='Click the needle hub';};
$('radius').onclick=()=>{mode='radius';$('click-hint').textContent='Click a point on the outer rim';};
canvas.addEventListener('click',e=>{
  if(!mode)return;
  const rect=canvas.getBoundingClientRect();
  // Canvas uses object-fit: contain; remove letterboxing before mapping clicks.
  const scale=Math.min(rect.width/image.width,rect.height/image.height), dw=image.width*scale,dh=image.height*scale;
  const x=(e.clientX-rect.left-(rect.width-dw)/2)/dw,y=(e.clientY-rect.top-(rect.height-dh)/2)/dh;
  if(x<0||x>1||y<0||y>1)return;
  if(mode==='center'){$('cx').value=x.toFixed(4);$('cy').value=y.toFixed(4);}
  else {$('radius-value').value=(Math.hypot((x-Number($('cx').value))*image.width,(y-Number($('cy').value))*image.height)/Math.min(image.width,image.height)).toFixed(4);}
  mode=null;$('click-hint').textContent='Calibration updated';draw();clearResult();
});
document.querySelectorAll('.fields input').forEach(input=>input.addEventListener('change',()=>{draw();clearResult();}));
document.querySelectorAll('[data-sample]').forEach(button=>button.onclick=()=>sample(button.dataset.sample));
$('inspect').onclick=async()=>{
  $('inspect').disabled=true;$('inspect').textContent='Inspecting…';
  clearResult();$('message').textContent='Checking quality and verifying the needle…';
  try {
    const raw=document.createElement('canvas');raw.width=image.width;raw.height=image.height;raw.getContext('2d').drawImage(image,0,0);
    const payload={image:raw.toDataURL('image/jpeg',.92).split(',')[1],calibration:calibration()};
    const response=await fetch('/api/inspect',{method:'POST',headers:{'Content-Type':'application/json','X-DialGuard-Token':$('token').value},body:JSON.stringify(payload)});
    const result=await response.json();if(!response.ok)throw new Error(result.error||'Inspection failed');
    lastResult=result;$('status').textContent=result.status==='READ'?'READING AVAILABLE':result.status==='REVIEW'?'HUMAN REVIEW':'TAKE ANOTHER PHOTO';$('status').className='status '+result.status.toLowerCase();
    $('reading').textContent=result.reading===null?'—':String(result.reading);
    if(result.reading!==null){const unit=document.createElement('small');unit.textContent=result.unit;$('reading').append(unit);}
    $('message').textContent=result.reasons.join(' ')||'Needle evidence passed the configured checks. Confirm important readings independently.';
    $('annotated').src='data:image/jpeg;base64,'+result.annotated_image;$('annotated').hidden=false;
    $('support').textContent=result.evidence_score.toFixed(3)+' / 1';$('latency').textContent=result.latency_ms+' ms';$('metrics').hidden=false;
    $('trace').textContent=JSON.stringify(result.trace,null,2);$('trace-details').hidden=false;$('download').hidden=false;
  }catch(e){showError(e.message);}finally{$('inspect').disabled=false;$('inspect').textContent='Inspect this dial →';}
};
$('download').onclick=()=>{
  if(!lastResult)return;const {annotated_image,...evidence}=lastResult;
  const url=URL.createObjectURL(new Blob([JSON.stringify(evidence,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download='dialguard-'+evidence.inspection_id+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
fetch('/health').then(r=>r.json()).then(data=>{$('runtime').textContent='OpenCV '+data.opencv_version+' · '+data.mode;}).catch(()=>{$('runtime').textContent='Engine unavailable';});
sample('clean');
