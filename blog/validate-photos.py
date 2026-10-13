from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib,json,collections
root=Path(__file__).resolve().parent
articles=json.loads((root/'articles.json').read_text())
photos=json.loads((root/'photo-assets.json').read_text())
assert len(photos)==60 and len({(p['slug'],p['kind']) for p in photos})==60
hashes=[];refs=[]
class Images(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='img' and a.get('class')=='hero-photo':self.images.append(a)
  if tag=='img' and '-detail.webp' in a.get('src',''):self.images.append(a)
for article in articles:
 p=root/article['path']/'index.html';parser=Images();parser.feed(p.read_text())
 assert len(parser.images)==2,(article['slug'],parser.images)
 for image in parser.images:
  f=(p.parent/image['src']).resolve()
  assert f.exists(),f
  assert article['slug'] in f.name,(article['slug'],f.name)
  assert image.get('alt'),f
  refs.append(str(f));hashes.append(hashlib.sha256(f.read_bytes()).hexdigest())
assert len(set(refs))==60
assert len(set(hashes))==60
out={'articles':len(articles),'unique_photo_files':len(set(refs)),'unique_photo_hashes':len(set(hashes)),'two_subject_specific_images_per_article':True}
(root/'research/photo-validation.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
