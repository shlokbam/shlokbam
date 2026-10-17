from lib import *

P = 'tl'
W = 900
ROW = 80
Y0 = 112


def build():
    items = profile()['timeline']
    H = Y0 + len(items) * ROW + 6
    css = font_css(P) + reduced_css(P) + f"""
@keyframes {P}-in{{from{{opacity:0;transform:translateX(18px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes {P}-draw{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes {P}-pop{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:scale(1)}}}}
.{P}-line{{transform-box:fill-box;transform-origin:top;animation:{P}-draw 2.2s cubic-bezier(.4,.1,.2,1) .2s both}}
.{P}-row{{animation:{P}-in .7s cubic-bezier(.2,.8,.2,1) both}}
.{P}-node{{transform-box:fill-box;transform-origin:center;animation:{P}-pop .5s cubic-bezier(.3,1.6,.5,1) both}}
"""
    defs = common_defs(P, W, H) + (
        f'<linearGradient id="{P}-vl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CRIMSON}"/>'
        f'<stop offset=".5" stop-color="#8d6bff"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>')
    body = card_bg(P, W, H, [('b', 140, H - 40, 300), ('c', 790, 60, 280)])
    assert syne_w('Experience', 32) < 400
    body += f'<text class="{P}-d" x="48" y="66" font-size="32" letter-spacing="-.8">Experience</text>'
    LX = 214
    n = len(items)
    top, bot = Y0 + 12, Y0 + (n - 1) * ROW + 12
    body += (f'<rect x="{LX - 1.5}" y="{top}" width="3" height="{bot - top}" rx="1.5" fill="{CARD}"/>'
             f'<rect class="{P}-line" x="{LX - 1.5}" y="{top}" width="3" height="{bot - top}" rx="1.5" fill="url(#{P}-vl)"/>')
    pulse = ''
    for i, it in enumerate(items):
        y = Y0 + i * ROW
        d = 0.5 + i * 0.42
        cur = it.get('current')
        title_w = syne_w(it['title'], 17)
        assert body_w(it['when'], 13, 600) <= 150, it['when']
        for ln in it['text']:
            assert body_w(ln, 14) <= 852 - 246, ln
        assert 246 + title_w + 14 + body_w(it['org'], 15, 600) <= 852, it['title']
        node_col = CRIMSON if cur else BLUE
        body += (f'<g class="{P}-row" style="animation-delay:{d:.2f}s">'
                 f'<text class="{P}-bb {P}-dim" x="{LX - 28}" y="{y + 17}" font-size="13" text-anchor="end">{it["when"]}</text>'
                 f'<g class="{P}-node" style="animation-delay:{d:.2f}s"><circle cx="{LX}" cy="{y + 12}" r="8" fill="{NAVY}" stroke="{node_col}" stroke-width="2.500"/>'
                 f'<circle cx="{LX}" cy="{y + 12}" r="3.500" fill="{node_col}"/></g>'
                 f'<text class="{P}-d" x="246" y="{y + 17}" font-size="17" letter-spacing="-.2">{it["title"]}</text>'
                 f'<text class="{P}-bb" x="{f(246 + title_w + 14)}" y="{y + 17}" font-size="15" style="fill:{"#ff8a9a" if cur else "#6aa8ff"}">{it["org"]}</text>')
        for k, ln in enumerate(it['text']):
            body += f'<text class="{P}-b {P}-dim" x="246" y="{y + 40 + k * 20}" font-size="14">{ln}</text>'
        body += '</g>'
        if cur:   # SMIL: a ring that keeps pulsing on the "now" marker
            pulse += (f'<circle cx="{LX}" cy="{y + 12}" r="8" fill="none" stroke="{CRIMSON}" stroke-width="2" opacity="0">'
                      f'<animate attributeName="r" values="8;8;22;22" keyTimes="0;.42;.9;1" dur="2.6s" begin="0s" repeatCount="indefinite"/>'
                      f'<animate attributeName="opacity" values="0;0;.7;0" keyTimes="0;.42;.5;1" dur="2.6s" begin="0s" repeatCount="indefinite"/></circle>')
    body += f'<g class="{P}-ani">{pulse}</g>'
    return shell(P, W, H, css, defs, body, 'Experience timeline of Shlok Bam',
                 'Timeline, newest first: ' + '; '.join(f"{i['when']}: {i['title']}, {i['org']}" for i in items) + '.')


if __name__ == '__main__':
    open(f'{B}/out/assets/timeline.svg', 'w').write(build()); print('ok')
