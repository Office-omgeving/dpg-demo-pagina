(()=>{
const path=location.pathname;
if(path.startsWith('/demo/'))return;
const sectors={dakwerken:{label:'Dakwerken',sales:'/dakwerken/',info:'/dakwerken-info/'},zonnepanelen:{label:'Zonnepanelen',sales:'/zonnepanelen/',info:'/zonnepanelen-info/'},thuisbatterij:{label:'Thuisbatterijen',sales:'/thuisbatterij/',info:'/thuisbatterij-info/'}};
const key=path.includes('zonnepanelen')?'zonnepanelen':path.includes('thuisbatterij')?'thuisbatterij':path==='/blog/'?null:'dakwerken';
const topic=sectors[key];
const css=document.createElement('style');css.textContent=`.dpg-demo-nav{background:#f5faf7;border-bottom:1px solid #dce5ea;color:#022b52;font:14px/1.5 Figtree,Helvetica,sans-serif}.dpg-demo-nav>div{width:min(1280px,calc(100% - 32px));margin:auto;display:flex;align-items:center;gap:24px;padding:10px 0}.dpg-demo-nav a{color:#067b45;text-decoration:none;font-weight:600}.dpg-demo-nav a:hover{text-decoration:underline}.dpg-demo-nav a:focus-visible{outline:3px solid #067b45;outline-offset:3px}.dpg-demo-nav details{margin-left:auto}.dpg-demo-nav summary{display:none}.dpg-demo-nav .dpg-links{display:flex;gap:24px;align-items:center}.dpg-demo-nav .dpg-links a[aria-current=page]{color:#022b52;text-decoration:underline}.dpg-demo-nav .dpg-label{font-size:13px}@media(max-width:650px){.dpg-demo-nav>div{gap:12px;padding:7px 0;font-size:12px}.dpg-demo-nav summary{display:block!important;cursor:pointer;padding:0!important;font:600 12px/1.5 Figtree,Helvetica,sans-serif;list-style:revert!important}.dpg-demo-nav summary:after{display:none!important}.dpg-demo-nav details{border:0}.dpg-demo-nav details:not([open]) .dpg-links{display:none}.dpg-demo-nav details[open] .dpg-links{display:flex;position:absolute;right:16px;z-index:20;background:white;border:1px solid #dce5ea;padding:16px;flex-direction:column;align-items:flex-start;gap:16px;margin-top:8px}.dpg-demo-nav .dpg-label{font-size:12px}}`;
document.head.append(css);
const bar=document.createElement('div');bar.className='dpg-demo-nav';bar.setAttribute('role','navigation');bar.setAttribute('aria-label','Navigatie door de DPG-demo');
const links=topic?[[topic.info,'Informatiepagina'],[topic.sales,'Salespagina'],[`/blog/${key}/`,'Blogs']]:[['/dakwerken-info/','Dakwerken'],['/zonnepanelen-info/','Zonnepanelen'],['/thuisbatterij-info/','Thuisbatterijen']];
bar.innerHTML=`<div><a href="/demo/">← Demo-overzicht</a>${topic?`<span class="dpg-label">${topic.label}</span>`:''}<details><summary>Pagina’s</summary><div class="dpg-links">${links.map(([url,label])=>`<a href="${url}" ${path===url?'aria-current="page"':''}>${label}</a>`).join('')}</div></details></div>`;
document.body.prepend(bar);
const menu=bar.querySelector("details");const mobile=matchMedia("(max-width:650px)");menu.open=!mobile.matches;mobile.addEventListener("change",()=>menu.open=!mobile.matches);
// Keep the demo's brand links inside the demo; calculators and source links stay intact.
document.querySelectorAll('a[href="https://www.mijnenergie.be/"]').forEach(a=>a.href='/demo/');
})();
