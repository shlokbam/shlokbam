from lib import *

P = 'hero'
W, H = 900, 478
_H = profile()['hero']
ROLES = _H['roles']
GREET = "Hi, I'm"
PITCH = _H['pitch']
NAME_SIZE = 112


def typed(animate):
    size = 24
    adv = 0.6 * size
    n = len(GREET)
    txt = f'<text class="{P}-m" x="48" y="82" font-size="{size}">{GREET}</text>'
    if not animate:
        return txt
    t0, dur = 0.25, 1.6
    kt = [0] + [(t0 + (dur - t0) * i / n) / dur for i in range(n)]
    vals_w = [0] + [adv * (i + 1) for i in range(n)]
    vals_x = [48] + [48 + adv * (i + 1) for i in range(n)]
    kts = ';'.join(f(k) for k in kt)
    return (
        f'<clipPath id="{P}-tclip"><rect x="48" y="54" width="{f(adv * n)}" height="38">'
        f'<animate attributeName="width" values="{";".join(f(v) for v in vals_w)}" keyTimes="{kts}" '
        f'calcMode="discrete" dur="{dur}s" begin="0s" fill="freeze"/></rect></clipPath>'
        f'<g clip-path="url(#{P}-tclip)">{txt}</g>'
        f'<rect x="{f(48 + adv * n + 4)}" y="60" width="3" height="28" rx="1.5" fill="{CRIMSON}" opacity="0">'
        f'<animate attributeName="x" values="{";".join(f(v + 4) for v in vals_x)}" keyTimes="{kts}" '
        f'calcMode="discrete" dur="{dur}s" begin="0s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.5;.5001;.99;1" dur="1.1s" '
        f'begin="0s" repeatCount="indefinite"/></rect>'
    )


def roles(animate):
    Y, SZ = 338, 30
    if not animate:
        return f'<text class="{P}-d" x="48" y="{Y}" font-size="{SZ}" style="fill:url(#{P}-ink)">{ROLES[0]}</text>'
    out, n, dur = '', len(ROLES), 16
    for k, r in enumerate(ROLES):
        a, b, e = k / n, (k + 1) / n, 0.02
        if k == 0:
            vals, kts = '1;1;0;0;1', f'0;{f(b - e)};{f(b)};{f(1 - e)};1'
        else:
            vals, kts = '0;0;1;1;0;0', f'0;{f(a - e)};{f(a)};{f(b - e)};{f(b)};1'
        out += (f'<g opacity="{1 if k == 0 else 0}"><animate attributeName="opacity" values="{vals}" keyTimes="{kts}" '
                f'dur="{dur}s" begin="0s" repeatCount="indefinite"/>'
                f'<text class="{P}-d" x="48" y="{Y}" font-size="{SZ}" style="fill:url(#{P}-ink)">{r}</text></g>')
    return out


def chip(x, y, label, icon):
    w = 50 + body_w(label, 17, 600) + 22
    return (f'<g transform="translate({f(x)} {y})"><rect width="{f(w)}" height="44" rx="22" fill="{CARD}" '
            f'stroke="url(#{P}-edge)" stroke-opacity=".7" stroke-width="1.2"/>{icon}'
            f'<text class="{P}-bb" x="50" y="28.500" font-size="17">{label}</text></g>'), w


PIN = (f'<path d="M26 10c-4.400 0-8 3.400-8 7.700 0 5.600 8 14.300 8 14.300s8-8.700 8-14.300c0-4.300-3.600-7.700-8-7.700z" '
       f'fill="none" stroke="{CRIMSON}" stroke-width="2" stroke-linejoin="round"/><circle cx="26" cy="17.800" r="2.800" fill="{CRIMSON}"/>')
CASE = (f'<rect x="17" y="14" width="18" height="14" rx="3" fill="none" stroke="{BLUE}" stroke-width="2"/>'
        f'<path d="M22 14v-2.500a1.500 1.500 0 0 1 1.500-1.500h5a1.500 1.500 0 0 1 1.500 1.500V14M17 21h18" fill="none" stroke="{BLUE}" stroke-width="2"/>')


SPARK = (f'<path d="M26 9l2.600 7.400L36 19l-7.400 2.600L26 29l-2.600-7.400L16 19l7.400-2.600z" fill="none" stroke="{CRIMSON}" stroke-width="2" stroke-linejoin="round"/>')


def build():
    css = font_css(P) + reduced_css(P) + f"""
@keyframes {P}-rise{{from{{transform:translateY(130px)}}to{{transform:translateY(0)}}}}
@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes {P}-slide{{from{{opacity:0;transform:translateX(46px)}}to{{opacity:1;transform:translateX(0)}}}}
.{P}-n1{{animation:{P}-rise 1s cubic-bezier(.16,.84,.24,1) .9s both}}
.{P}-n2{{animation:{P}-rise 1s cubic-bezier(.16,.84,.24,1) 1.12s both}}
.{P}-pan{{animation:{P}-slide .9s cubic-bezier(.16,.84,.24,1) 1.5s both}}
.{P}-late{{animation:{P}-in .8s ease 2.3s both}}
.{P}-late2{{animation:{P}-in .8s ease 2.7s both}}
"""
    PX, PY, PW, PH = 560, 32, 300, 316
    defs = common_defs(P, W, H) + (
        f'<clipPath id="{P}-n1c"><rect x="40" y="92" width="500" height="98"/></clipPath>'
        f'<clipPath id="{P}-n2c"><rect x="40" y="192" width="500" height="98"/></clipPath>'
        f'<clipPath id="{P}-pc"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="26"/></clipPath>'
        f'<linearGradient id="{P}-pbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141f3d"/><stop offset="1" stop-color="#0a1020"/></linearGradient>'
        f'<linearGradient id="{P}-rule" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity=".9"/><stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></linearGradient>'
        f'<image id="{P}-img" width="{PW}" height="{PH}" preserveAspectRatio="xMidYMin slice" xlink:href="data:image/png;base64,{PNG_ID}"/>')
    body = card_bg(P, W, H, [('b', 120, 440, 330), ('c', 800, 50, 300)])
    body += (f'<g class="{P}-pan"><g clip-path="url(#{P}-pc)"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="url(#{P}-pbg)"/>'
             f'<circle cx="{PX + 30}" cy="{PY + 270}" r="200" fill="url(#{P}-gb)"/><circle cx="{PX + 270}" cy="{PY + 50}" r="190" fill="url(#{P}-gc)"/>'
             f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="url(#{P}-dots)"/>'
             f'<use href="#{P}-img" xlink:href="#{P}-img" x="{PX}" y="{PY}"/></g>'
             f'<rect x="{PX + .5}" y="{PY + .5}" width="{PW - 1}" height="{PH - 1}" rx="26" fill="none" stroke="url(#{P}-edge)" stroke-width="1.5"/></g>')
    body += f'<g class="{P}-ani">{typed(True)}</g><g class="{P}-still">{typed(False)}</g>'
    body += (f'<g clip-path="url(#{P}-n1c)"><text class="{P}-d {P}-n1" x="42" y="184" font-size="{NAME_SIZE}" letter-spacing="-3">Shlok</text></g>'
             f'<g clip-path="url(#{P}-n2c)"><text class="{P}-d {P}-n2" x="42" y="280" font-size="{NAME_SIZE}" letter-spacing="-3">Bam</text></g>')
    body += f'<g class="{P}-late"><g class="{P}-ani">{roles(True)}</g><g class="{P}-still">{roles(False)}</g></g>'
    c1, w1 = chip(48, 412, _H['location'], PIN)
    c2, w2 = chip(48 + w1 + 14, 412, _H['company'], CASE)
    c3, w3 = chip(48 + w1 + w2 + 28, 412, _H['open_to'], SPARK)
    assert 48 + w1 + w2 + w3 + 28 <= 852, 'hero chips too wide'
    body += (f'<g class="{P}-late2"><rect x="48" y="362" width="804" height="1.5" fill="url(#{P}-rule)"/>'
             f'<text class="{P}-b" x="48" y="402" font-size="20">{PITCH}</text>'.replace('y="402"', 'y="396"') + c1 + c2 + c3 + '</g>')
    return shell(P, W, H, css, defs, body, 'Shlok Bam: AI, Gen AI and Agentic AI engineer',
                 'Hero banner with a portrait of Shlok Bam, cycling role titles, a one-line pitch, location Pune, India, role Intern at PharmaACE Innovations, and open to collaborate.')


if __name__ == '__main__':
    open(f'{B}/out/assets/hero.svg', 'w').write(build()); print('ok', os.path.getsize(f'{B}/out/assets/hero.svg'))
