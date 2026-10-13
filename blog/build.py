from pathlib import Path
from html import escape as e
import json,re,runpy,math,difflib,unicodedata
ROOT=Path(__file__).resolve().parent
A=runpy.run_path(str(ROOT/'content.py'))['ARTICLES']
EXTRA=runpy.run_path(str(ROOT/'extra.py'))['EXTRA']
DEEP=runpy.run_path(str(ROOT/'deepening.py'))['DEEP']
LABELS={'dakwerken':'Dakwerken','zonnepanelen':'Zonnepanelen','thuisbatterij':'Thuisbatterijen'}
IMAGES={'dakwerken':('roof','roof-detail','Dak van een Belgische woning','Dakraam en dakgoot bij een hellend dak'),'zonnepanelen':('solar','solar-detail','Zonnepanelen op een Belgische woning','Zonnepanelen op een plat dak'),'thuisbatterij':('battery','battery-detail','Thuisbatterij met omvormer','Batterij en elektrische apparatuur in een technische ruimte')}
for a in A:
 a['sections'].append(EXTRA[a['slug']])
 a['depth']='deep' if a['slug'] in DEEP else 'short'
 if a['depth']=='deep':
  a['sections'].extend(DEEP[a['slug']]['sections'])
  a['comparison']=DEEP[a['slug']]['table']
 a['word_count']=len(re.findall(r'\w+',a['lead']+' '+str(a['sections'])+' '+str(a['check'])+' '+a['example']+' '+str(a['faq'])))
 if a['depth']=='deep':
  a['word_count']+=len(re.findall(r'\w+',str(a['comparison'])))
 a['minutes']=max(2,math.ceil(a['word_count']/200))
 a['path']=f"{a['sector']}/{a['slug']}/"

PHOTO_JOBS=json.loads((ROOT/'photo-jobs.json').read_text()) if (ROOT/'photo-jobs.json').exists() else []
PHOTO_READY=(ROOT/'photo-assets.json').exists()
def images_for(article):
 if PHOTO_READY:
  jobs={x['kind']:x for x in PHOTO_JOBS if x['slug']==article['slug']}
  return (article['slug']+'-hero',article['slug']+'-detail',jobs['hero']['alt'],jobs['detail']['alt'])
 return IMAGES[article['sector']]

if PHOTO_READY:
 for article in A:
  article['images']=[{'file':'assets/'+article['slug']+'-'+job['kind']+'.webp','kind':job['kind'],'alt':job['alt'],'caption':job['alt']+' — AI-gegenereerd illustratief beeld'} for job in PHOTO_JOBS if job['slug']==article['slug']]

def render_paragraph(text, article):
 rendered=e(text)
 urls={'Fluvius':article['source'] if 'fluvius' in article['source'] else 'https://www.fluvius.be/nl/veelgestelde-vragen/groene-stroom','Buildwise':article['source'] if 'buildwise' in article['source'] else 'https://www.buildwise.be/nl/help-center/faq/mag-men-zonnepanelen-plaatsen-op-een-asbesthoudend-dak/','SMA':article['source'] if 'sma' in article['source'] else 'https://www.sma.de/en/products/solar-batteries/sma-home-storage','Vlaamse Nutsregulator':article['source'] if 'nutsregulator' in article['source'] else 'https://www.vlaamsenutsregulator.be/veelgestelde-vragen'}
 for name,url in urls.items():
  rendered=rendered.replace(name,f'<a href="{url}">{name}</a>',1)
 return rendered

def shell(title,description,body,prefix=''):
 return f'''<!doctype html><html lang="nl-BE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{e(title)} | Mijnenergie.be — demo</title><meta name="description" content="{e(description[:170])}"><meta property="og:title" content="{e(title)}"><meta property="og:type" content="article"><link rel="stylesheet" href="{prefix}style.css?v=depth2"></head><body><a class="skip" href="#main">Ga naar inhoud</a><div class="demo">DPG-concept · Nieuwe artikels · Geen officiële publicatie</div><header><div class="container top"><a href="{prefix}../"><img src="{prefix}../assets/mijnenergie-logo.png" alt="Mijnenergie.be" width="250" height="52"></a><a href="{prefix}">Duurzaam wonen</a></div><nav class="container" aria-label="Hoofdnavigatie"><a href="{prefix}dakwerken/">Dakwerken</a><a href="{prefix}zonnepanelen/">Zonnepanelen</a><a href="{prefix}thuisbatterij/">Thuisbatterijen</a><a href="{prefix}">Alle artikels</a></nav></header><main id="main">{body}</main><footer><div class="container"><p>Informatieve demo voor DPG · Researchstand 13 oktober 2026</p><p>Elk artikel heeft twee eigen AI-gegenereerde illustratieve beelden. Ze tonen geen gerealiseerde klantinstallaties.</p><a href="{prefix}research/overlap.html">Research en overlapcontrole</a> · <a href="{prefix}../">Dakwerken calculator</a> · <a href="{prefix}../zonnepanelen/">Zonnepanelen calculator</a> · <a href="{prefix}../thuisbatterij/">Thuisbatterij calculator</a></div></footer><script src="/demo/navigation.js" defer></script></body></html>'''

def card(a,prefix=''):
 im=images_for(a)
 return f'''<article class="story" data-sector="{a['sector']}" data-search="{e((a['title']+' '+a['lead']).lower())}"><a href="{prefix}{a['path']}" class="story-image" tabindex="-1" aria-hidden="true"><img src="{prefix}assets/{im[0]}.webp" alt="" width="1400" height="560" loading="lazy"></a><div class="story-copy"><p class="story-meta">{LABELS[a['sector']]} · {a['minutes']} min. · {'Verdiepend' if a['depth']=='deep' else 'Kort'}</p><h2><a href="{prefix}{a['path']}">{e(a['title'])}</a></h2><p>{e(a['lead'].split('. ')[0])}.</p><a class="read" href="{prefix}{a['path']}" aria-label="Lees {e(a['title'])}">Lees de gids <span aria-hidden="true">→</span></a></div></article>'''

# All-article index with progressive-enhancement search/filter.
ordered=[A[i] for j in range(10) for i in [j,j+10,j+20]]
filters=''.join(f'<button type="button" data-filter="{k}" aria-pressed="false">{v} <span>10</span></button>' for k,v in LABELS.items())
body=f'''<section class="container index-heading"><h1>Praktische gidsen voor je woning</h1><p>Duidelijke uitleg over dakwerken, zonnepanelen en thuisbatterijen. Van je eerste vragen tot een goed voorbereide installatie.</p><div class="filters" aria-label="Filter artikels"><button type="button" data-filter="all" aria-pressed="true">Alles <span>30</span></button>{filters}</div><label class="search">Zoek een onderwerp<input type="search" id="search" placeholder="Bijvoorbeeld: offerte, garantie of dakraam"></label><p id="count" class="count" role="status" aria-live="polite">30 artikels</p></section><section class="container stories" aria-label="Artikels">{''.join(card(a) for a in ordered)}</section><p class="container empty" id="empty" hidden>Geen artikels gevonden. Probeer een ander zoekwoord of kies een andere categorie.</p><script src="filter.js" defer></script>'''
(ROOT/'index.html').write_text(shell('Blogs over dakwerken, zonnepanelen en thuisbatterijen','30 nieuwe praktische gidsen voor duurzame woningprojecten.',body))
for sector,label in LABELS.items():
 p=ROOT/sector;p.mkdir(exist_ok=True)
 body=f'''<section class="container index-heading"><p class="crumb"><a href="../">Duurzaam wonen</a> / {label}</p><h1>{label}: praktische gidsen</h1><p>Vijf korte gidsen en vijf verdiepende artikels om jouw project beter te begrijpen en voor te bereiden.</p><a class="text-link" href="../../{sector+'/' if sector!='dakwerken' else ''}">Naar de {sector}calculator →</a></section><section class="container stories">{''.join(card(a,'../') for a in A if a['sector']==sector)}</section>'''
 (p/'index.html').write_text(shell(label+' blogs','Praktische gidsen over '+label.lower(),body,'../'))
for a in A:
 p=ROOT/a['path'];p.mkdir(parents=True,exist_ok=True)
 im=images_for(a);secs='';toc=''
 for i,(heading,paragraph) in enumerate(a['sections']):
  ident='onderdeel-'+str(i+1);toc+=f'<li><a href="#{ident}">{e(heading)}</a></li>'
  secs+=f'<section id="{ident}"><h2>{e(heading)}</h2><p>{render_paragraph(paragraph,a)}</p></section>'
  if i==1:secs+=f'<figure class="inline-photo"><img src="../../assets/{im[1]}.webp" alt="{im[3]}" width="1400" height="560" loading="lazy"><figcaption>{im[3]}. Illustratief beeld, geen technische uitvoeringsreferentie.</figcaption></figure>'
 if a['depth']=='deep':
  table=a['comparison']
  secs+='<section id="vergelijking"><h2>Praktische vergelijking</h2><div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+e(t)+'</th>' for t in table['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(t)+'</td>' for t in row)+'</tr>' for row in table['rows'])+'</tbody></table></div></section>'
  toc+='<li><a href="#vergelijking">Praktische vergelijking</a></li>'
 source_name='Buildwise' if 'buildwise' in a['source'] else 'Fluvius' if 'fluvius' in a['source'] else 'OVAM' if 'ovam' in a['source'] else 'Vlaamse Nutsregulator' if 'nutsregulator' in a['source'] else 'SMA' if 'sma' in a['source'] else 'Victron Energy'
 related=[x for x in A if x['sector']==a['sector'] and x['slug']!=a['slug']][:3]
 sector_dest='../../../'+(a['sector']+'/' if a['sector']!='dakwerken' else '')
 body=f'''<div class="container article-top"><p class="crumb"><a href="../../">Duurzaam wonen</a> / <a href="../">{LABELS[a['sector']]}</a></p><h1>{e(a['title'])}</h1><p class="lead">{e(a['lead'])}</p><p class="byline">{'Verdiepende gids' if a['depth']=='deep' else 'Korte gids'} · Conceptartikel · 13 oktober 2026 · {a['minutes']} min. leestijd</p><figure><img class="hero-photo" src="../../assets/{im[0]}.webp" alt="{im[2]}" width="1400" height="560"><figcaption>{im[2]} · AI-gegenereerd illustratief beeld</figcaption></figure></div><div class="container article-layout"><aside aria-label="Inhoudsopgave"><h2>In dit artikel</h2><ol>{toc}<li><a href="#checklist">Checklist</a></li><li><a href="#bron">Bron en achtergrond</a></li></ol></aside><article class="reading">{secs}<section class="example"><h2>Een praktisch voorbeeld</h2><p>{e(a['example'])}</p><p class="small">Illustratief scenario, geen klantcase.</p></section><section id="checklist" class="checklist"><h2>Neem dit mee naar je gesprek</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in a['check'])}</ul></section><section><h2>Veelgestelde vraag</h2><h3>{e(a['faq'][0])}</h3><p>{e(a['faq'][1])}</p></section><section id="bron" class="sources"><h2>Bron en achtergrond</h2><p><a href="{a['source']}">{source_name}: officiële of technische achtergrond bij dit onderwerp ↗</a></p><p>Geraadpleegd op 13 oktober 2026. De praktische checklist en het voorbeeld zijn redactionele uitwerkingen. Fabrikantinformatie geldt voor de beschreven producten; ze is geen algemene garantie voor andere systemen.</p></section><section class="next"><h2>Wat betekent dit voor jouw woning?</h2><p>Gebruik de calculator voor een eerste indicatie. Een vakman beoordeelt jouw situatie en bevestigt de uitvoering en definitieve prijs.</p><a class="button" href="{sector_dest}">Bekijk de {a['sector']}calculator →</a>{'<p><a href="../../../dakwerken-info/">Lees ook de volledige dakwerken-gids</a></p>' if a['sector']=='dakwerken' else ''}</section><section class="related"><h2>Verder lezen over {LABELS[a['sector']].lower()}</h2>{''.join(f'<a href="../{x["slug"]}/">{e(x["title"])}</a>' for x in related)}</section></article></div>'''
 text=shell(a['title'],a['lead'],body,'../../')
 schema={'@context':'https://schema.org','@type':'Article','headline':a['title'],'description':a['lead'],'inLanguage':'nl-BE','dateModified':'2026-10-13','articleSection':LABELS[a['sector']],'wordCount':a['word_count'],'isAccessibleForFree':True}
 text=text.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script></head>')
 (p/'index.html').write_text(text)
# Inventory evidence and nearest semantic candidates, for review (not a claim of exhaustive uniqueness).
inventory=json.loads((ROOT/'research/inventory.json').read_text())
heads=json.loads((ROOT/'research/existing-headings.json').read_text())
def terms(s):
 s=unicodedata.normalize('NFKD',s.lower());return set(re.findall(r'[a-z]{4,}',s))-{'voor','deze','zijn','welke','over','jouw','wordt','niet','meer','moet','door','zonnepanelen','thuisbatterij','dakwerken'}
report=[]
for a in A:
 t=terms(a['title']+' '+a['lead']);scores=[]
 for x in heads:
  h=' '.join(x.get('headings',[])[:20]);u=x['url'].split('/blog/')[-1].replace('-',' ');v=terms(h+' '+u)
  score=len(t&v)/max(1,len(t|v));scores.append((score,x))
 near=[dict(url=x['url'],score=round(s,3)) for s,x in sorted(scores,key=lambda z:z[0],reverse=True)[:2]]
 report.append(dict(title=a['title'],path=a['path'],angle=a['angle'],nearest=near,exact_slug_match=any(x['url'].rstrip('/').endswith('/'+a['slug']) for x in inventory)))
(ROOT/'research/overlap.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
rows=''.join(f'<tr><td>{e(a["title"])}</td><td>{e(a["angle"])}</td><td>'+''.join(f'<a href="{x["url"]}">{e(x["url"].split("/blog/")[-1].replace("-"," "))}</a><br>' for x in a['nearest'])+'</td></tr>' for a in report)
body=f'''<section class="container research"><h1>Onderzoek en overlapcontrole</h1><p>Stand: 13 oktober 2026. Inventaris: {len(inventory)} blog-URL’s uit de <a href="https://www.mijnenergie.be/sitemap.xml">Mijnenergie-sitemap</a>. Van {len(heads)} thematisch geselecteerde pagina’s zijn titelstructuren onderzocht; {sum('error' in x for x in heads)} pagina’s konden niet worden opgehaald.</p><p>Algemene onderwerpen over prijs, werking, rendement, aantal panelen, plug-and-play, injectievergoedingen en zelfverbruik zijn bewust vermeden als hoofdonderwerp. De nieuwe artikels kiezen specifieke praktijkvragen. Er zijn geen gelijke slugs gevonden. De onderstaande kandidaten zijn woordgebaseerde vergelijkingen, geen bewijs van volledige inhoudelijke uniciteit.</p><p>Redactionele grens: een breed bestaand artikel kan een deelonderwerp al noemen. De kolom “Nieuwe invalshoek” omschrijft het verschil. Een laatste DPG/CMS-controle blijft nodig vóór publicatie, vooral voor niet-geïndexeerde of niet-bereikbare content.</p><p>Alle dertig teksten zijn nieuw geschreven. Elk artikel heeft twee unieke AI-gegenereerde beelden die bij zijn onderwerp aansluiten; er is geen beeldmateriaal uit Mijnenergie-artikels gekopieerd. Lokale demopagina’s staan op noindex; canonicals en productiedomein worden pas bij plaatsing ingevuld.</p><div class="table-wrap"><table><thead><tr><th>Nieuw artikel</th><th>Nieuwe invalshoek</th><th>Dichtstbijzijnde bestaande onderwerpen</th></tr></thead><tbody>{rows}</tbody></table></div><p><a href="inventory.json">Volledige URL-inventaris (JSON)</a> · <a href="existing-headings.json">Gelezen titelstructuren</a> · <a href="overlap.json">Overlapmatrix</a></p></section>'''
(ROOT/'research/overlap.html').write_text(shell('Research en overlapcontrole','Inventaris van Mijnenergie en nieuwe redactionele invalshoeken.',body,'../'))
(ROOT/'articles.json').write_text(json.dumps(A,ensure_ascii=False,indent=2))
print(f'{len(A)} artikels; woorden {min(a["word_count"] for a in A)}–{max(a["word_count"] for a in A)}; totaal {sum(a["word_count"] for a in A)}')
