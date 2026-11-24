#!/usr/bin/env python3
"""TradeX-Blog bauen: tools/blog/beitraege/*.md -> blog/<slug>/index.html,
blog/index.html, Vorschaubilder (blog/<slug>/og.png) und Blog-Block in sitemap.xml.

Aufruf im Repo-Wurzelverzeichnis:  python3 tools/blog/bauen.py
Vorschaubilder brauchen Node mit Playwright (tools/blog/og.cjs); fehlt es,
bleibt ein vorhandenes og.png stehen, sonst wird og-image.png verwendet.
Nur Standardbibliothek. Anleitung: tools/blog/ANLEITUNG.md
"""
import html, json, os, re, subprocess, sys, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'tools', 'blog', 'beitraege')
SITE = 'https://tradexag.ch'
STYLE_FROM = os.path.join(ROOT, 'wissen', 'sicherheit', '02-hosting', 'index.html')
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August',
          'September', 'Oktober', 'November', 'Dezember']
PFLICHT = ['slug', 'title', 'description', 'excerpt', 'keyword', 'category', 'publishedAt', 'author']


def fehler(msg):
    sys.exit('FEHLER: ' + msg)


def esc(s):
    return html.escape(s, quote=True)


def datum(d):
    y, m, t = d.split('-')
    return f'{int(t)}. {MONATE[int(m) - 1]} {y}'


def lies(pfad):
    t = open(pfad, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
    if not m:
        fehler(f'{pfad}: Kopf (--- ... ---) fehlt')
    kopf = {}
    for z in m.group(1).splitlines():
        if z.strip():
            k, _, v = z.partition(':')
            kopf[k.strip()] = v.strip()
    for k in PFLICHT:
        if not kopf.get(k):
            fehler(f'{pfad}: Feld "{k}" fehlt')
    kopf.setdefault('h1', kopf['title'])
    kopf.setdefault('updatedAt', kopf['publishedAt'])
    if kopf.get('entwurf', '').lower() in ('ja', 'true', '1'):
        return None
    if len(kopf['title']) > 60:
        fehler(f'{pfad}: title {len(kopf["title"])} Zeichen, höchstens 60')
    if not 120 <= len(kopf['description']) <= 160:
        fehler(f'{pfad}: description {len(kopf["description"])} Zeichen, Ziel 120 bis 160')
    if not re.fullmatch(r'[a-z0-9-]+', kopf['slug']):
        fehler(f'{pfad}: slug nur a-z, 0-9 und -')
    kopf['body_md'] = m.group(2).strip()
    return kopf


# ---------- kleines Markdown ----------
def inline(s):
    s = esc(s).replace('&quot;', '"')
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)

    def link(m):
        text, url = m.group(1), m.group(2).replace('&amp;', '&')
        if url.startswith('http'):
            return f'<a href="{esc(url)}" target="_blank" rel="noopener">{text}</a>'
        return f'<a href="{esc(url)}">{text}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, s)


def slugify(s):
    s = s.lower()
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def md(text):
    out, blocks = [], re.split(r'\n\s*\n', text)
    k = 0
    for b in blocks:
        lines = b.strip('\n').splitlines()
        first = lines[0]
        if first.startswith('### '):
            out.append(f'<h3>{inline(first[4:])}</h3>')
            rest = '\n'.join(lines[1:]).strip()
            if rest:
                out.append(f'<p>{inline(rest)}</p>')
        elif first.startswith('## '):
            t = first[3:]
            out.append(f'<h2 id="{slugify(t)}">{inline(t)}</h2>')
        elif first.startswith('|'):
            rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if not re.match(r'^\|[\s:|-]+\|$', l.strip())]
            h = ''.join(f'<th>{inline(c)}</th>' for c in rows[0])
            bd = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
            out.append(f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{bd}</tbody></table></div>')
        elif first.startswith('- [ ] '):
            items = ''
            for l in lines:
                k += 1
                items += f'<li class="chk"><label><input type="checkbox" data-k="{k}"><span>{inline(l[6:])}</span></label></li>'
            out.append(f'<ul class="checklist">{items}</ul>')
        elif first.startswith('- '):
            out.append('<ul>' + ''.join(f'<li>{inline(l[2:])}</li>' for l in lines) + '</ul>')
        elif re.match(r'\d+\. ', first):
            out.append('<ol>' + ''.join('<li>' + inline(re.sub(r'^\d+\. ', '', l)) + '</li>' for l in lines) + '</ol>')
        elif first.startswith('> '):
            out.append(f'<blockquote><p>{inline(" ".join(l[2:] for l in lines))}</p></blockquote>')
        else:
            out.append(f'<p>{inline(" ".join(lines))}</p>')
    return '\n'.join(out)


def faqs(body_md):
    teil = body_md.split('## Häufige Fragen', 1)
    if len(teil) < 2:
        return []
    teil = re.split(r'\n## ', teil[1])[0]
    return [(q.strip(), re.sub(r'\s+', ' ', a).strip()) for q, a in re.findall(r'### (.+?)\n\n(.+?)(?=\n### |\Z)', teil, re.S)]


def plain(s):
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s).replace('**', '')


# ---------- Seitenrahmen ----------
def style():
    src = open(STYLE_FROM, encoding='utf-8').read()
    css = src[src.index('<style>') + 7:src.index('</style>')]
    return css + '''
main.single{max-width:820px}
.lead{font-size:19px}
.crumbs{font-size:13px;color:var(--muted);margin-bottom:28px}.crumbs a{text-decoration:none;border:0;color:var(--muted)}.crumbs a:hover{color:var(--ink)}
.meta{color:var(--muted);margin:-24px 0 32px}
.posts{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}
.posts li{border-bottom:1px solid var(--line)}
.posts a{display:block;padding:24px 0;text-decoration:none;border:0}
.posts h2{margin:6px 0 8px;font-size:24px;letter-spacing:-.02em}
.posts p{color:#303030;margin:0}
.posts a:hover h2{text-decoration:underline;text-decoration-color:var(--accent)}
.source{color:var(--muted);font-size:15px}
.navlink{text-decoration:none;color:var(--muted)}.navlink:hover{color:var(--ink)}
'''


def kontakt():
    src = open(STYLE_FROM, encoding='utf-8').read()
    return src[src.index('<aside class="support">'):src.index('</aside>') + 8]


def fuss():
    src = open(STYLE_FROM, encoding='utf-8').read()
    return src[src.index('<footer class="mono">'):]


LOGO = '<a class="logo" href="/" aria-label="TradeX International AG, Startseite"><svg viewBox="0 0 22 22" aria-hidden="true"><rect width="22" height="22" fill="#111111"/><path d="M6.5 6.5 L15.5 15.5 M15.5 6.5 L6.5 15.5" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="square"/></svg><span>TRADEX</span></a>'


def kopf(title, desc, url, image, typ, extra_meta, ld):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="TradeX Blog" href="{SITE}/blog/feed.xml">
<meta property="og:type" content="{typ}">
<meta property="og:site_name" content="TradeX International AG">
<meta property="og:locale" content="de_CH">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{extra_meta}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{style()}</style>
</head>
<body>
<header>{LOGO}<a class="navlink mono" href="/blog/">Blog</a></header>
'''


PUBLISHER = {'@type': 'Organization', 'name': 'TradeX International AG', 'url': SITE + '/',
             'logo': {'@type': 'ImageObject', 'url': SITE + '/apple-touch-icon.png'}}


def lesezeit(body_md):
    return max(1, round(len(plain(body_md).split()) / 200))


def og_bild(p, ziel_dir):
    png = os.path.join(ziel_dir, 'og.png')
    vorlage = os.path.join(ROOT, 'tools', 'blog', 'og-vorlage.html')
    t = open(vorlage, encoding='utf-8').read()
    t = t.replace('{{TITEL}}', esc(p['h1'])).replace('{{KATEGORIE}}', esc(p['category']))
    tmp = os.path.join(ziel_dir, '_og.html')
    open(tmp, 'w', encoding='utf-8').write(t)
    try:
        subprocess.run(['node', os.path.join(ROOT, 'tools', 'blog', 'og.cjs'), tmp, png],
                       check=True, capture_output=True, timeout=120)
    except Exception as e:
        print(f'  Hinweis: Vorschaubild nicht gerendert ({e.__class__.__name__}).')
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    if os.path.exists(png):
        return f'{SITE}/blog/{p["slug"]}/og.png'
    return f'{SITE}/og-image.png'


def beitrag(p, alle):
    url = f'{SITE}/blog/{p["slug"]}/'
    d = os.path.join(ROOT, 'blog', p['slug'])
    os.makedirs(d, exist_ok=True)
    image = og_bild(p, d)
    fq = faqs(p['body_md'])
    graph = [
        {'@type': 'BlogPosting', 'headline': p['h1'], 'name': p['title'], 'description': p['description'],
         'image': image, 'datePublished': p['publishedAt'], 'dateModified': p['updatedAt'],
         'inLanguage': 'de-CH', 'keywords': p['keyword'], 'articleSection': p['category'],
         'wordCount': len(plain(p['body_md']).split()),
         'author': {'@type': 'Person', 'name': p['author'], 'url': SITE + '/'},
         'publisher': PUBLISHER, 'mainEntityOfPage': url,
         'isPartOf': {'@type': 'Blog', 'name': 'TradeX Blog', 'url': SITE + '/blog/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Start', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + '/blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': p['h1'], 'item': url}]},
    ]
    if fq:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in fq]})
    extra = (f'<meta property="article:published_time" content="{p["publishedAt"]}">\n'
             f'<meta property="article:modified_time" content="{p["updatedAt"]}">\n'
             f'<meta property="article:author" content="{esc(p["author"])}">\n'
             f'<meta property="article:section" content="{esc(p["category"])}">\n')
    titel_tag = p['title'] if len(p['title']) > 50 else p['title'] + ' | TradeX'
    body = md(p['body_md'])
    body = body.replace('<p><strong>Kurz gesagt:', '<p class="lead"><strong>Kurz gesagt:', 1)
    quelle = ''
    if p.get('quelle'):
        name, _, qurl = p['quelle'].partition('|')
        quelle = (f'<p class="source">Anregung: <a href="{esc(qurl.strip())}" target="_blank" rel="noopener">{esc(name.strip())}</a>. '
                  'Eigener Text, keine Übernahme.</p>' if qurl.strip() else f'<p class="source">Anregung: {esc(name.strip())}. Eigener Text.</p>')
    weitere = [x for x in alle if x['slug'] != p['slug']][:3]
    mehr = ''
    if weitere:
        mehr = '<h2>Weitere Beiträge</h2><ul>' + ''.join(
            f'<li><a href="/blog/{x["slug"]}/">{esc(x["h1"])}</a></li>' for x in weitere) + '</ul>'
    stand = f'Veröffentlicht am {datum(p["publishedAt"])}'
    if p['updatedAt'] != p['publishedAt']:
        stand += f' · aktualisiert am {datum(p["updatedAt"])}'
    html_ = (kopf(titel_tag, p['description'], url, image, 'article', extra, {'@context': 'https://schema.org', '@graph': graph})
             + f'''<main class="single"><article>
<nav class="crumbs mono" aria-label="Brotkrumen"><a href="/">Start</a> / <a href="/blog/">Blog</a> / {esc(p["category"])}</nav>
<h1>{esc(p["h1"])}</h1>
<p class="meta mono"><time datetime="{p["publishedAt"]}">{datum(p["publishedAt"])}</time> · {esc(p["author"])} · {lesezeit(p["body_md"])} Min. Lesezeit</p>
{body}
{quelle}
{mehr}
{kontakt()}
<hr>
<p>{stand} · {esc(p["author"])}, TradeX International AG</p><p class="kb-foot"><a href="/blog/">Alle Beiträge im TradeX Blog</a></p></article></main>
''' + fuss())
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html_)
    return url


def uebersicht(alle):
    url = SITE + '/blog/'
    titel = 'Blog: KI, Automatisierung und E-Commerce | TradeX'
    desc = ('Wie wir bei TradeX mit KI Software bauen und E-Commerce automatisieren: Arbeitsweise, '
            'Werkzeuge und Erfahrungen aus der Praxis, offen beschrieben.')
    ld = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'TradeX Blog', 'url': url,
          'description': desc, 'inLanguage': 'de-CH', 'publisher': PUBLISHER,
          'blogPost': [{'@type': 'BlogPosting', 'headline': p['h1'], 'url': f'{SITE}/blog/{p["slug"]}/',
                        'datePublished': p['publishedAt']} for p in alle]}
    items = ''.join(f'''<li><a href="/blog/{p["slug"]}/"><span class="mono">{esc(p["category"])} · {datum(p["publishedAt"])}</span>
<h2>{esc(p["h1"])}</h2><p>{esc(p["excerpt"])}</p></a></li>''' for p in alle)
    html_ = (kopf(titel, desc, url, SITE + '/og-image.png', 'website', '', ld)
             + f'''<main class="single"><article>
<nav class="crumbs mono" aria-label="Brotkrumen"><a href="/">Start</a> / Blog</nav>
<h1>Blog</h1>
<p class="lead">Wie wir bei TradeX mit KI Software bauen und E-Commerce automatisieren. Unsere Arbeitsweise, unsere Werkzeuge und was wir dabei lernen.</p>
<ul class="posts">{items}</ul>
{kontakt()}
</article></main>
''' + fuss())
    os.makedirs(os.path.join(ROOT, 'blog'), exist_ok=True)
    open(os.path.join(ROOT, 'blog', 'index.html'), 'w', encoding='utf-8').write(html_)


def feed(alle):
    items = ''.join(f'''<item><title>{esc(p["h1"])}</title><link>{SITE}/blog/{p["slug"]}/</link><guid>{SITE}/blog/{p["slug"]}/</guid>
<pubDate>{datetime.datetime.strptime(p["publishedAt"], "%Y-%m-%d").strftime("%a, %d %b %Y 07:00:00 +0000")}</pubDate><description>{esc(p["excerpt"])}</description></item>''' for p in alle)
    open(os.path.join(ROOT, 'blog', 'feed.xml'), 'w', encoding='utf-8').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>TradeX Blog</title><link>{SITE}/blog/</link>'
        f'<description>KI, Automatisierung und E-Commerce bei TradeX</description><language>de-ch</language>{items}</channel></rss>\n')


def sitemap(alle):
    pfad = os.path.join(ROOT, 'sitemap.xml')
    t = open(pfad, encoding='utf-8').read()
    neu = '  <!-- blog:start (von tools/blog/bauen.py erzeugt) -->\n'
    letzte = max(p['updatedAt'] for p in alle)
    neu += f'  <url><loc>{SITE}/blog/</loc><lastmod>{letzte}</lastmod></url>\n'
    for p in alle:
        neu += f'  <url><loc>{SITE}/blog/{p["slug"]}/</loc><lastmod>{p["updatedAt"]}</lastmod></url>\n'
    neu += '  <!-- blog:end -->\n'
    if '<!-- blog:start' in t:
        t = re.sub(r'  <!-- blog:start.*?<!-- blog:end -->\n', neu, t, flags=re.S)
    else:
        t = t.replace('</urlset>', neu + '</urlset>')
    open(pfad, 'w', encoding='utf-8').write(t)


def main():
    alle = [p for p in (lies(os.path.join(SRC, f)) for f in sorted(os.listdir(SRC)) if f.endswith('.md')) if p]
    slugs = [p['slug'] for p in alle]
    if len(set(slugs)) != len(slugs):
        fehler('slug doppelt')
    alle.sort(key=lambda p: p['publishedAt'], reverse=True)
    for p in alle:
        print('Beitrag:', beitrag(p, alle))
    uebersicht(alle)
    feed(alle)
    sitemap(alle)
    print(f'{len(alle)} Beiträge, Übersicht, Feed und Sitemap aktualisiert.')


if __name__ == '__main__':
    main()
