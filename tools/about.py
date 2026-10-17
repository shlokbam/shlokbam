from lib import *

P = 'life'
W, H = 900, 452
_P = profile()
CAPS = [(c['name'], c['sub']) for c in _P['capabilities']]
SLIDES = [(s['title'], s['icon'], s['lines']) for s in _P['slides']]
CX, CY, CW, CH = 470, 40, 382, 384
PAD = 30
SEG_GAP = 8
SEG_W = (CW - 2 * PAD - 2 * SEG_GAP) / 3
DUR = 12


def people(cx, cy, col):
    return (f'<g fill="none" stroke="{col}" stroke-width="2.4" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy - 9}" r="6"/><path d="M{cx - 11} {cy + 14}c0-7 5-11 11-11s11 4 11 11"/>'
            f'<circle cx="{cx - 20}" cy="{cy - 4}" r="4.500" opacity=".7"/><circle cx="{cx + 20}" cy="{cy - 4}" r="4.500" opacity=".7"/></g>')


def slide(i, animate):
    title, ic, lines = SLIDES[i]
    x0, y0 = CX + PAD, CY
    disc = (f'<circle cx="{x0 + 42}" cy="{y0 + 120}" r="42" fill="{NAVY}" stroke="url(#{P}-edge)" stroke-width="1.5"/>')
    disc += icon_use(ic, x0 + 42, y0 + 120, 40) if ic else people(x0 + 42, y0 + 120, INK)
    txt = f'<text class="{P}-d" x="{x0}" y="{y0 + 222}" font-size="22" letter-spacing="-.2">{title}</text>'
    for k, ln in enumerate(lines):
        txt += f'<text class="{P}-b {P}-dim" x="{x0}" y="{y0 + 266 + k * 28}" font-size="15.500">{ln}</text>'
    if not animate:
        return f'<g>{disc}{txt}</g>'
    a, b = i / 3, (i + 1) / 3
    e = 0.4 / DUR
    if i == 0:
        vals, kts = '1;1;0;0;1', f'0;{f(b - e)};{f(b)};{f(1 - e)};1'
    else:
        vals, kts = '0;0;1;1;0;0', f'0;{f(a - e)};{f(a)};{f(b - e)};{f(b)};1'
    return (f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="{vals}" keyTimes="{kts}" '
            f'dur="{DUR}s" begin="0s" repeatCount="indefinite"/>{disc}{txt}</g>')


def segs(animate):
    out = ''
    for i in range(3):
        x = CX + PAD + i * (SEG_W + SEG_GAP)
        out += f'<rect x="{f(x)}" y="{CY + 34}" width="{f(SEG_W)}" height="5" rx="2.5" fill="#26324f"/>'
        full = i == 0
        out += f'<rect x="{f(x)}" y="{CY + 34}" width="{f(SEG_W) if full else 0}" height="5" rx="2.5" fill="url(#{P}-ink)">'
        if animate:
            a, b = i / 3, (i + 1) / 3
            if i == 0:
                vals, kts = f'0;{f(SEG_W)};{f(SEG_W)}', f'0;{f(b)};1'
            else:
                vals, kts = f'0;0;{f(SEG_W)};{f(SEG_W)}', f'0;{f(a)};{f(b)};1'
            out += (f'<animate attributeName="width" values="{vals}" keyTimes="{kts}" dur="{DUR}s" '
                    f'begin="0s" repeatCount="indefinite"/>')
        out += '</rect>'
    return out


def build():
    css = font_css(P) + reduced_css(P) + f"""
@keyframes {P}-draw{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes {P}-pop{{from{{opacity:0;transform:scale(.96)}}to{{opacity:1;transform:scale(1)}}}}
.{P}-bar{{transform-box:fill-box;transform-origin:top;animation:{P}-draw .7s cubic-bezier(.2,.8,.2,1) both}}
.{P}-tx{{animation:{P}-in .7s ease both}}
.{P}-cardin{{transform-box:fill-box;transform-origin:center;animation:{P}-pop .9s cubic-bezier(.16,.84,.24,1) .3s both}}
"""
    defs = common_defs(P, W, H) + (
        f'<clipPath id="{P}-cc"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="26"/></clipPath>')
    body = card_bg(P, W, H, [('b', 90, 470, 300), ('c', 760, 40, 280)])
    body += f'<text class="{P}-d" x="48" y="74" font-size="34" letter-spacing="-1">What I build</text>'
    for i, (t, s) in enumerate(CAPS):
        y = 106 + i * 66
        d = 0.35 + i * 0.14
        body += (
            f'<rect class="{P}-bar" x="48" y="{y}" width="4" height="46" rx="2" fill="url(#{P}-edge)" style="animation-delay:{d}s"/>'
            f'<text class="{P}-d {P}-tx" x="68" y="{y + 22}" font-size="20" style="animation-delay:{d + .1}s">{t}</text>'
            f'<text class="{P}-b {P}-dim {P}-tx" x="68" y="{y + 46}" font-size="15" style="animation-delay:{d + .2}s">{s}</text>')
    body += (f'<g class="{P}-cardin"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="26" fill="{CARD}"/>'
             f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="26" fill="url(#{P}-dots)"/>'
             f'<rect x="{CX + .75}" y="{CY + .75}" width="{CW - 1.5}" height="{CH - 1.5}" rx="25.250" fill="none" stroke="url(#{P}-edge)" stroke-width="1.5"/>'
             f'<g clip-path="url(#{P}-cc)">'
             f'<g class="{P}-ani">{segs(True)}{"".join(slide(i, True) for i in range(3))}</g>'
             f'<g class="{P}-still">{segs(False)}{slide(0, False)}</g></g></g>')
    return shell(P, W, H, css, defs, body, 'What Shlok builds, and what he does away from the keyboard',
                 'Five capability areas: agentic AI, LLM evaluation, RAG and MCP, full-stack delivery, cloud and DevOps. Beside them a carousel of three interests that changes every four seconds: writing, problem solving and community.')


if __name__ == '__main__':
    open(f'{B}/out/assets/life_tmp.svg', 'w').write('')
    os.remove(f'{B}/out/assets/life_tmp.svg')
    open(f'{B}/out/assets/about-life.svg', 'w').write(build())
    print('ok', os.path.getsize(f'{B}/out/assets/about-life.svg'))
