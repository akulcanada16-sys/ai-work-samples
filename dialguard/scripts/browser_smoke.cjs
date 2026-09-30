/* Run with the pinned Playwright package; no credentials written to disk. */
const fs=require('node:fs');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async()=>{
  const base=process.env.DIALGUARD_URL || 'http://127.0.0.1:8080';
  const options={headless:true,args:['--no-sandbox']};
  if(process.env.CHROME_EXECUTABLE)options.executablePath=process.env.CHROME_EXECUTABLE;
  const browser=await chromium.launch(options);
  const page=await browser.newPage({viewport:{width:1280,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.waitForFunction(()=>document.getElementById('image').width===512);
  if(process.env.DIALGUARD_TOKEN)await page.locator('#token').fill(process.env.DIALGUARD_TOKEN);
  await page.getByRole('button',{name:'Inspect this dial'}).click();
  await page.waitForFunction(()=>document.getElementById('status').textContent==='READING AVAILABLE');
  let reading=parseFloat(await page.locator('#reading').textContent());
  if(Math.abs(reading-62)>1.2)throw new Error('Wrong visible reading');
  fs.mkdirSync('evidence',{recursive:true});
  await page.screenshot({path:'evidence/browser-desktop.png',fullPage:true});
  await page.getByRole('button',{name:'High · 90',exact:true}).click();
  await page.waitForFunction(()=>document.getElementById('image-label').textContent.endsWith('high'));
  await page.getByRole('button',{name:'Inspect this dial'}).click();
  await page.waitForFunction(()=>document.getElementById('status').textContent==='HUMAN REVIEW');
  await page.getByRole('button',{name:'Blurred',exact:true}).click();
  await page.waitForFunction(()=>document.getElementById('image-label').textContent.endsWith('blur'));
  await page.getByRole('button',{name:'Inspect this dial'}).click();
  await page.waitForFunction(()=>document.getElementById('status').textContent==='TAKE ANOTHER PHOTO');
  // Actual file-upload flow, including JPEG re-encoding in the UI.
  const response=await page.request.get(base+'/sample/clean');
  await page.locator('#upload').setInputFiles({name:'gauge-fixture.png',mimeType:'image/png',buffer:await response.body()});
  await page.waitForFunction(()=>document.getElementById('image-label').textContent==='gauge-fixture.png');
  await page.getByRole('button',{name:'Inspect this dial'}).click();
  await page.waitForFunction(()=>document.getElementById('status').textContent==='READING AVAILABLE');
  const downloadPromise=page.waitForEvent('download');await page.locator('#download').click();
  const download=await downloadPromise;
  if(!download.suggestedFilename().endsWith('.json'))throw new Error('Evidence download failed');
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:'evidence/browser-mobile.png',fullPage:true});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw new Error('Mobile horizontal overflow');
  if(errors.length)throw new Error(errors.join('\n'));
  console.log(JSON.stringify({browser:'Chromium',read:true,review:true,retake:true,upload:true,
    evidence_download:true,mobile_overflow:false,page_errors:errors}));
  await browser.close();
})().catch(error=>{console.error(error.message);process.exit(1);});
