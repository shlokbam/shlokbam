from lib import *
P = 'conn'
W, H = 900, 244
CARDS = profile()['connect']
RES = profile()['resume']
CH, GX, GY, X0, Y0 = 58, 15, 12, 48, 16
CW3 = 258
CW2 = (804 - GX) / 2


def chev(x, y, op=1):
    return f'<path d="M{x} {y-8} l8 8 l-8 8" fill="none" stroke="url(#{P}-ink)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="{op}"/>'


def nudge(i, anim, inner):
    if not anim: return f'<g>{inner}</g>'
    s = i / max(len(CARDS), 1) * .8; kt = [0, s, s + .04, s + .08, s + .12, s + .16, 1]; v = ['0 0', '0 0', '8 0', '0 0', '8 0', '0 0', '0 0']
    return f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(v)}" keyTimes="{";".join(f(k) for k in kt)}" dur="6s" begin="0s" repeatCount="indefinite"/>{inner}</g>'


def drop(anim, inner):
    if not anim: return f'<g>{inner}</g>'
    return f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 5;0 0;0 5;0 0;0 0" keyTimes="0;.1;.2;.3;.4;1" dur="4s" begin="0s" repeatCount="indefinite"/>{inner}</g>'


def layout():
    """first row of three, then the rest split evenly across a second row"""
    out = []
    for i, c in enumerate(CARDS):
        if i < 3:
            out.append((X0 + i * (CW3 + GX), Y0, CW3))
        else:
            rest = len(CARDS) - 3
            w = (804 - GX * (rest - 1)) / rest
            out.append((X0 + (i - 3) * (w + GX), Y0 + CH + GY, w))
    return out


def cards(anim):
    out = ''
    for i, (c, (x, y, w)) in enumerate(zip(CARDS, layout())):
        k = c['icon']
        assert body_w(c['sub'], 13) <= w - 62 - 36, c['sub']
        out += (f'<g class="{P}-card" style="animation-delay:{.3 + i * .1:.2f}s">'
                f'<rect x="{f(x)}" y="{y}" width="{f(w)}" height="{CH}" rx="18" fill="{CARD}"/><rect x="{f(x)}" y="{y}" width="{f(w)}" height="{CH}" rx="18" fill="url(#{P}-dots)"/>'
                f'<rect x="{f(x + .75)}" y="{y + .75}" width="{f(w - 1.5)}" height="{CH - 1.5}" rx="17.25" fill="none" stroke="url(#{P}-edge)" stroke-width="1.4"/>'
                f'<circle cx="{f(x + 32)}" cy="{y + CH / 2}" r="19" fill="{NAVY}" stroke="url(#{P}-edge)" stroke-width="1.2"/>'
                f'{icon_use(k, x + 32, y + CH / 2, 20, INK if k in ("codechef", "globe", "journal") else None)}'
                f'<text class="{P}-d" x="{f(x + 62)}" y="{y + 26}" font-size="16">{c["name"]}</text>'
                f'<text class="{P}-b {P}-dim" x="{f(x + 62)}" y="{y + 44}" font-size="13">{c["sub"]}</text>'
                f'{nudge(i, anim, chev(f(x + w - 28), y + CH / 2))}</g>')
    return out


def resume(anim):
    y = Y0 + 2 * (CH + GY) + 4
    doc = (f'<g transform="translate({X0 + 28} {y + 14})" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">'
           f'<path d="M3 0 h13 l7 7 v21 a3 3 0 0 1 -3 3 h-17 a3 3 0 0 1 -3 -3 v-25 a3 3 0 0 1 3 -3 z"/><path d="M16 0 v7 h7"/><path d="M7 15 h10 M7 21 h10"/></g>')
    arrow = drop(anim, f'<path d="M0 -8 v14 M-7 0 l7 7 l7 -7" transform="translate({X0 + 804 - 38} {y + 30})" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<g class="{P}-card" style="animation-delay:.9s"><rect x="{X0}" y="{y}" width="804" height="60" rx="20" fill="url(#{P}-btn)"/>'
            f'<rect x="{X0 + .75}" y="{y + .75}" width="802.5" height="58.5" rx="19.25" fill="none" stroke="url(#{P}-edge)" stroke-width="1.5"/>{doc}'
            f'<text class="{P}-d" x="{X0 + 78}" y="{y + 37}" font-size="20" letter-spacing="-.3">{RES["label"]}</text>'
            f'<text class="{P}-m" x="{X0 + 804 - 76}" y="{y + 35}" font-size="14" text-anchor="end" style="fill:{INK};fill-opacity:.85">{RES["file"]}</text>{arrow}</g>')


def build():
    css = font_css(P) + reduced_css(P) + f"@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}.{P}-card{{animation:{P}-in .6s ease both}}"
    defs = common_defs(P, W, H) + f'<linearGradient id="{P}-btn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset="1" stop-color="{CRIMSON}" stop-opacity=".55"/></linearGradient>'
    body = card_bg(P, W, H, [('b', 120, 230, 240), ('c', 800, 20, 240)]) + f'<g class="{P}-ani">{cards(True)}{resume(True)}</g><g class="{P}-still">{cards(False)}{resume(False)}</g>'
    names = ', '.join(c['name'] for c in CARDS)
    return shell(P, W, H, css, defs, body, 'Connect with Shlok Bam and download his resume',
                 f'Social and site cards: {names}, and a resume download button. Clickable links are listed below this image in the README.')


if __name__ == '__main__':
    open(f'{B}/out/assets/connect.svg', 'w').write(build()); print('ok')
