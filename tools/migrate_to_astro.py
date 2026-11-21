"""One-time migration: reads the current premium index.html and writes website/src/data/content.json.
After this, website/src/data/content.json is the single source of the website text."""
import json
import re
import sys
from bs4 import BeautifulSoup

src, dst = sys.argv[1], sys.argv[2]
raw = open(src).read()
soup = BeautifulSoup(raw, 'html.parser')

def inner(el):
    return ''.join(str(c) for c in el.contents).strip() if el else ''
def text(el):
    return el.get_text(' ', strip=True) if el else ''
def head(sec):
    h2 = sec.find('h2'); intro = sec.select_one('.head > p') or sec.select_one('.intro p:not(.eyebrow)')
    return {'eyebrow': text(sec.select_one('.eyebrow')), 'title': inner(h2), 'intro': inner(intro)}

meta = {
    'title': soup.title.string,
    'description': soup.find('meta', attrs={'name': 'description'})['content'],
    'url': soup.find('link', rel='canonical')['href'],
    'ogTitle': soup.find('meta', property='og:title')['content'],
    'ogImage': soup.find('meta', property='og:image')['content'],
    'jsonld': json.loads(soup.find('script', type='application/ld+json').string),
}

hero = soup.select_one('section.hero')
c = {'meta': meta}
c['hero'] = {
    'eyebrow': text(hero.select_one('.eyebrow')),
    'lead': inner(hero.select_one('.hero-lead')),
    'assure': [text(li) for li in hero.select('.assure li')],
}
c['statement'] = inner(soup.select_one('section.statement p'))

sec = soup.select_one('#challenges')
c['challenges'] = head(sec) | {'items': [
    {'href': a['href'], 'tag': text(a.select_one('.tag')), 'title': inner(a.h3), 'text': inner(a.p), 'more': text(a.select_one('.more'))}
    for a in sec.select('a.challenge')]}

sec = soup.select_one('#first-engagement')
c['offer'] = {'eyebrow': text(sec.select_one('.eyebrow')), 'title': inner(sec.h2), 'lede': inner(sec.select_one('.offer-lede')),
              'facts': [{'term': text(d.dt), 'detail': inner(d.dd)} for d in sec.select('.facts > div')]}

sec = soup.select_one('#services')
labels = {a['href'][1:]: inner(a) for a in sec.select('#svc-index a')}
items = []
for art in sec.select('article.svc'):
    img = art.img
    items.append({'id': art['id'], 'label': labels[art['id']], 'num': text(art.select_one('.num')),
                  'image': img['src'], 'alt': img['alt'], 'width': int(img['width']), 'height': int(img['height']),
                  'title': inner(art.h3), 'text': inner(art.select_one('h3 + p')),
                  'capsLabel': text(art.select_one('.cats')), 'caps': [inner(li) for li in art.select('ul li')]})
c['services'] = head(sec) | {'items': items}

sec = soup.select_one('#sectors')
c['sectors'] = head(sec) | {'items': [{'icon': str(a.svg), 'title': inner(a.h3), 'text': inner(a.p)} for a in sec.select('article.sector')]}

sec = soup.select_one('#technology')
c['platforms'] = head(sec) | {
    'core': [{'name': inner(d.b), 'detail': inner(d.span)} for d in sec.select('.eco-item')],
    'toolkitLabel': text(sec.select_one('.toolkit .lbl')),
    'toolkit': [{'name': text(p).replace(text(p.select_one('.dev')), '').strip() if p.select_one('.dev') else text(p),
                 'growing': bool(p.select_one('.dev'))} for p in sec.select('.toolkit .p')]}

sec = soup.select_one('#how-we-work')
c['method'] = head(sec) | {
    'steps': [{'step': text(a.select_one('.n')), 'question': text(a.select_one('.ask')), 'title': inner(a.h3),
               'text': inner(a.select_one('h3 + p')), 'points': [inner(li) for li in a.select('ul li')],
               'result': inner(a.select_one('.out'))} for a in sec.select('article.step')],
    'outcomesTitle': text(sec.select_one('.outcomes-head')),
    'outcomes': [{'label': text(d.select_one('.index')), 'title': inner(d.h3), 'text': inner(d.p)} for d in sec.select('.outcomes > div')]}

sec = soup.select_one('#faq')
c['faq'] = head(sec) | {'items': [{'question': text(d.summary), 'answer': inner(d.select_one('.a'))} for d in sec.select('details')]}

sec = soup.select_one('#contact')
c['contact'] = {'eyebrow': text(sec.select_one('.eyebrow')), 'title': inner(sec.h2), 'text': inner(sec.select_one('.contact-copy > p')),
                'email': 'info@dataitech.eu', 'linkedin': sec.select_one('a.btn[href*=linkedin]')['href'],
                'person': {'name': text(sec.select_one('.person b')), 'role': text(sec.select_one('.person div span')),
                           'photo': sec.select_one('.person img')['src']}}
c['footer'] = {'legal': [inner(x) for x in soup.select('.site-footer .legal > span')], 'slogan': text(soup.select_one('.site-footer .mono'))}
c['nav'] = [{'href': a['href'], 'label': text(a)} for a in soup.select('.nav-links a:not(.btn)')]

def strip_pd(v):
    return v
json.dump(c, open(dst, 'w'), indent=2, ensure_ascii=False)
print('written', dst, {k: (len(v['items']) if isinstance(v, dict) and 'items' in v else '') for k, v in c.items()})
