import json
from lib import *
P = 'wr'
W = 900
def build(path=None):
    posts = json.load(open(path or f'{B}/data/writing.json'))[:3]
    H = 96 + len(posts) * 78 + 18
    css = font_css(P) + reduced_css(P) + f"@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}@keyframes {P}-draw{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}.{P}-r{{animation:{P}-in .7s ease both}}.{P}-b{{transform-box:fill-box;transform-origin:top;animation:{P}-draw .6s cubic-bezier(.2,.8,.2,1) both}}"
    defs = common_defs(P, W, H)
    body = card_bg(P, W, H, [('b', 130, H - 30, 280), ('c', 800, 40, 260)])
    assert syne_w('Latest writing', 30) < 460
    body += (f'<text class="{P}-d" x="48" y="66" font-size="30" letter-spacing="-.6">Latest writing</text>'
             f'<text class="{P}-b {P}-dim" x="852" y="64" font-size="13" text-anchor="end">journal-murex-three.vercel.app</text>')
    for i, p in enumerate(posts):
        y = 92 + i * 78
        sub = p.get('subtitle', '')
        if len(sub) > 70: sub = sub[:67].rstrip() + '...'
        size = 17
        while syne_w(p['title'], size) > 640: size -= 1
        d = .3 + i * .15
        tag = p['source']; tw = body_w(tag, 13, 600) + 28
        body += (f'<g class="{P}-r" style="animation-delay:{d:.2f}s">'
                 f'<rect class="{P}-b" x="48" y="{y}" width="4" height="56" rx="2" fill="url(#{P}-edge)" style="animation-delay:{d:.2f}s"/>'
                 f'<text class="{P}-d" x="70" y="{y + 24}" font-size="{size}" letter-spacing="-.2">{p["title"]}</text>'
                 f'<text class="{P}-b {P}-dim" x="70" y="{y + 48}" font-size="14">{sub}</text>'
                 f'<rect x="{852 - tw}" y="{y + 12}" width="{f(tw)}" height="30" rx="15" fill="{CARD}" stroke="url(#{P}-edge)" stroke-opacity=".7" stroke-width="1.1"/>'
                 f'<text class="{P}-bb" x="{852 - tw / 2}" y="{y + 32}" font-size="13" text-anchor="middle">{tag}</text></g>')
    return shell(P, W, H, css, defs, body, 'Latest writing by Shlok Bam',
                 'Latest posts from the journal: ' + '; '.join(p['title'] for p in posts) + '. Links are listed below this image in the README.')
if __name__ == '__main__':
    open(f'{B}/out/assets/writing.svg','w').write(build()); print('ok')
