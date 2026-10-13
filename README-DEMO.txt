DPG contentdemo — 13 oktober 2026

Open lokaal: http://127.0.0.1:4178/blog/
Start vanuit deze map: python3 -m http.server 4178 --bind 127.0.0.1

Inhoud:
- drie salespagina’s met live calculators
- informatieve dakwerken-pillar op /dakwerken-info/
- 30 complete conceptblogs, 10 per sector, op /blog/
- categoriepagina’s, zoek/filter en calculatorlinks
- blog/articles.json: alle teksten, onderwerpen en bronnen
- blog/research/overlap.html: afbakening en overlapmatrix
- blog/research/inventory.json: 1.020 blog-URL’s uit de Mijnenergie-sitemap
- blog/content.py, extra.py en build.py: reproduceerbare inhoud en HTML-generatie

Beelden: zestig unieke AI-gegenereerde illustratieve beelden in blog/assets, geoptimaliseerd als WebP. Iedere blog heeft een eigen hoofdbeeld en een eigen detailbeeld met onderwerpgerichte alt-tekst. Geen foto’s van klantprojecten. Afzonderlijke salespagina’s gebruiken eigen bestaande/gegenereerde assets.

Research: 185 thematisch geselecteerde artikelstructuren onderzocht, waarvan 3 niet konden worden opgehaald. Geen identieke slugs gevonden. Gekozen invalshoeken zijn specifiek en aanvullend. Dit is geen bewijs dat geen enkele passage overlapt met een breed bestaand artikel; laatste DPG/CMS-check voor publicatie vereist.

Demo is noindex. Productie-URL’s, canonicals, auteurschap en eventuele CMS-taxonomie worden bij definitieve plaatsing ingevuld. Geen publicatie verricht. Live calculators zijn bestaande externe diensten; dien geen fictieve persoonsgegevens in.

QA: alle 30 artikelroutes HTTP 200; lokale links en anchors geldig; 10 artikelen per sector; filters, zoekfunctie en lege resultaten werken; desktop en mobiele weergave gecontroleerd.
Wrike: actieve DPG-subtaak 4582917443 met opgeslagen werkupdate.

Verdieping: per sector vijf korte blogs behouden (325–386 woorden) en vijf verdiepende blogs (836–910 woorden), met extra uitleg en praktische vergelijkingstabellen. Bron: blog/deepening.py. Controle: blog/research/depth-validation.json. Alle 60 unieke blogbeelden behouden.

Startpunt voor DPG: http://127.0.0.1:4178/demo/ . Drie sectoren met elk informatiepagina, salespagina en tien blogs. Gedeelde demobalk op de onderliggende pagina’s. Aanvullende informatiepagina’s gegenereerd met build-demo.py. Na blog/build.py ook build-demo.py uitvoeren. Nog niet gepubliceerd.
