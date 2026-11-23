// node smoke.js file.html  -> clicks every tab at phone + desktop width, reports JS errors
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();let bad=0;
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:860}});const errs=[];
p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(process.argv[2]));await p.waitForTimeout(2500);
const tabs=await p.$$('nav button, [role=tab], .tabs button');
for(const t of tabs){try{await t.click({timeout:2000});await p.waitForTimeout(400)}catch(e){}}
const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);
console.log(w,'tabs',tabs.length,'errors',errs.length,'overflow',ov,errs.slice(0,3));bad+=errs.length;await p.close()}
await b.close();process.exit(bad?1:0)})();
