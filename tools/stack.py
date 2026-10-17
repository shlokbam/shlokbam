from lib import *

P = 'stack'
W = 900
OY = 224                      # orbit centre y
OCX = 450
ORB_H = 446

# (rx, ry, tilt, duration, sweep, dash, [(icon key, label, start angle deg)])
ORBITS = [
    (368, 166, -12, 60, 1, '', [('python', 'Python', 0), ('fastapi', 'FastAPI', 90), ('react', 'React', 180),
                                ('postgresql', 'PostgreSQL', 270)]),
    (268, 108, -12, 60, 1, '', [('langchain', 'LangChain', 30), ('langgraph', 'LangGraph', 120),
                                ('mcp', 'MCP', 210), ('huggingface', 'Hugging Face', 300)]),
    (168, 52, -12, 60, 1, '5 7', [('docker', 'Docker', 60), ('terraform', 'Terraform', 150),
                                  ('aws', 'AWS', 240), ('jenkins', 'Jenkins', 330)]),
]

GROUPS = [(g['label'], g['items']) for g in profile()['stack_groups']]


def pos(rx, ry, deg):
    a = math.radians(deg)
    return rx * math.cos(a), ry * math.sin(a)


def pill_w(label):
    return body_w(label, 14, 600) + 52


def icon_node(key, label, extra=''):
    col = glyph_color(key)
    w = pill_w(label)
    ev = ' fill-rule="evenodd"' if ICONS[key].get("lobe") else ''
    return (f'<rect x="{f(-w / 2)}" y="-19" width="{f(w)}" height="38" rx="19" fill="{CARD}" stroke="url(#{P}-edge)" stroke-width="1.4"/>'
            f'<circle cx="{f(-w / 2 + 19)}" cy="0" r="14" fill="{NAVY}"/>'
            f'<path d="{icon_path(key)}" fill="{col}" transform="translate({f(-w / 2 + 19 - 8.5)} -8.5) scale(.7083)"{ev}/>'
            f'<text class="{P}-bb" x="{f(-w / 2 + 40)}" y="5" font-size="14">{label}</text>')


PH = json.load(open(f'{B}/orbit_best.json'))['phis_deg']
PERIOD = 54
NS = 72


def orbit_layer(animate):
    out = ''
    k = 0
    for oi, (rx, ry, tilt, _d, sweep, dash, items) in enumerate(ORBITS):
        out += f'<g transform="translate({OCX} {OY}) rotate({tilt})">'
        out += (f'<ellipse rx="{rx}" ry="{ry}" fill="none" stroke="url(#{P}-edge)" stroke-opacity=".75" '
                f'stroke-width="1.4"{f" stroke-dasharray=\"{dash}\"" if dash else ""}/>')
        for key, label, _deg in items:
            phi = math.radians(PH[k]); k += 1
            x0, y0 = rx * math.cos(phi), ry * math.sin(phi)
            node = f'<g transform="rotate({-tilt})">{icon_node(key, label)}</g>'
            if animate:
                pts = [(rx * math.cos(phi + 2 * math.pi * j / NS), ry * math.sin(phi + 2 * math.pi * j / NS)) for j in range(NS + 1)]
                vals = ';'.join(f'{f(px)} {f(py)}' for px, py in pts)
                out += (f'<g transform="translate({f(x0)} {f(y0)})"><animateTransform attributeName="transform" type="translate" '
                        f'values="{vals}" dur="{PERIOD}s" begin="0s" repeatCount="indefinite" calcMode="linear"/>{node}</g>')
            else:
                out += f'<g transform="translate({f(x0)} {f(y0)})">{node}</g>'
        out += '</g>'
    return out


def chips():
    """three-column masonry of grouped chips; returns svg, height"""
    X0, COLW, CGAP = 48, 252, 24
    cs, pad, gap, ch = 13.500, 10, 6, 28
    cols = [[], [], []]
    heights = [0, 0, 0]
    laid = []
    for gi, (label, items) in enumerate(GROUPS):
        assert syne_w(label, 14) <= COLW, label
        x, row, rows = 0, 0, []
        for it in items:
            w = body_w(it, cs, 600) + 2 * pad
            assert w <= COLW, it
            if x + w > COLW:
                x, row = 0, row + 1
            rows.append((x, row, w, it))
            x += w + gap
        h = 24 + (row + 1) * (ch + gap) + 12
        c = heights.index(min(heights))
        laid.append((c, heights[c], label, rows, gi))
        heights[c] += h
    out = ''
    for c, y, label, rows, gi in laid:
        cx = X0 + c * (COLW + CGAP)
        parts = ''
        for x, r, w, it in rows:
            parts += (f'<g transform="translate({f(x)} {24 + r * (ch + gap)})"><rect width="{f(w)}" height="{ch}" rx="{ch / 2}" fill="{CARD}" '
                      f'stroke="url(#{P}-edge)" stroke-opacity=".6" stroke-width="1.1"/>'
                      f'<text class="{P}-bb" x="{pad}" y="19" font-size="{cs}">{it}</text></g>')
        out += (f'<g class="{P}-row" style="animation-delay:{0.9 + gi * 0.09:.2f}s" transform="translate({cx} {y})">'
                f'<text class="{P}-d" x="0" y="14" font-size="14">{label}</text>{parts}</g>')
    return out, max(heights)


def build():
    rows, rows_h = chips()
    top = ORB_H + 14
    H = int(top + rows_h + 24)
    css = font_css(P) + reduced_css(P) + f"""
@keyframes {P}-grow{{from{{opacity:0;transform:scale(.82)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}
.{P}-orb{{transform-origin:{OCX}px {OY}px;animation:{P}-grow 1.3s cubic-bezier(.16,.84,.24,1) .2s both}}
.{P}-row{{animation:{P}-in .6s ease both}}
"""
    defs = common_defs(P, W, H) + (
        f'<radialGradient id="{P}-hub" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#16244a"/>'
        f'<stop offset="1" stop-color="#0a1020"/></radialGradient>')
    body = card_bg(P, W, H, [('b', 150, 120, 360), ('c', 780, 330, 340)])
    hub = (f'<circle cx="{OCX}" cy="{OY}" r="30" fill="url(#{P}-hub)" stroke="url(#{P}-edge)" stroke-width="1.6"/>'
           f'<text class="{P}-d" x="{OCX}" y="{OY + 6}" text-anchor="middle" font-size="17" letter-spacing="-.5">SB</text>')
    body += (f'<g class="{P}-orb">{hub}<g class="{P}-ani">{orbit_layer(True)}</g>'
             f'<g class="{P}-still">{orbit_layer(False)}</g></g>')
    body += f'<g transform="translate(0 {top})">{rows}</g>'
    return shell(P, W, H, css, defs, body, 'Tech stack of Shlok Bam',
                 'Nineteen technology icons, each labelled, travelling on three tilted elliptical orbits, followed by the full stack grouped into languages, GenAI frameworks and techniques, LLM evaluation, machine learning, web, databases, cloud and DevOps, and core computer science.')


if __name__ == '__main__':
    open(f'{B}/out/assets/stack.svg', 'w').write(build())
    print('ok', os.path.getsize(f'{B}/out/assets/stack.svg'))
