import base64, json, math, os, re

B = os.path.dirname(os.path.abspath(__file__))
NAVY, BLUE, CRIMSON, INK = '#070b16', '#247bff', '#ff354f', '#f2f4fa'
CARD = '#0d1424'
MUTED = '#9aa5c0'
ICONS = json.load(open(f'{B}/icons.json'))


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


FONT_DISP = b64(f'{B}/fonts/manrope-latin-800-normal.woff2')
FONT_B5 = b64(f'{B}/fonts/inter-latin-500-normal.woff2')
FONT_B6 = b64(f'{B}/fonts/inter-latin-600-normal.woff2')
FONT_M500 = b64(f'{B}/fonts/jetbrains-mono-latin-500-normal.woff2')
FONT_M700 = b64(f'{B}/fonts/jetbrains-mono-latin-700-normal.woff2')
PNG_ID = b64(f'{B}/id.png')
PNG_POINT = b64(f'{B}/right_pointing.png') if os.path.exists(f'{B}/right_pointing.png') else ''

LICENSE_COMMENT = (
    '<!-- Fonts embedded as base64 WOFF2 under the SIL Open Font License 1.1: '
    'Manrope (c) The Manrope Project Authors; Inter (c) The Inter Project Authors; JetBrains Mono (c) 2020 The JetBrains Mono Project Authors. '
    'Full texts: LICENSES/OFL-*.txt. '
    'Brand marks: see LICENSES/ICON-SOURCES.md. Portraits: author-supplied PNGs, pixel-identical. -->'
)


def mono_w(text, size):
    return len(text) * 0.6 * size


def lum(hexc):
    h = hexc.lstrip('#')
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def glyph_color(key):
    hx = '#' + ICONS[key]['hex']
    return hx if lum(hx) > 0.06 else INK


def font_css(p):
    ff = lambda fam, w, data: f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{data}) format('woff2');}}"
    return (
        ff('SB Display', 800, FONT_DISP) + ff('SB Body', 500, FONT_B5) + ff('SB Body', 600, FONT_B6)
        + ff('SB Mono', 500, FONT_M500) + ff('SB Mono', 700, FONT_M700)
        + f".{p}-d{{font-family:'SB Display','Segoe UI',Arial,sans-serif;font-weight:800;fill:{INK}}}"
        f".{p}-b{{font-family:'SB Body','Segoe UI',Arial,sans-serif;font-weight:500;fill:{INK}}}"
        f".{p}-bb{{font-family:'SB Body','Segoe UI',Arial,sans-serif;font-weight:600;fill:{INK}}}"
        f".{p}-m{{font-family:'SB Mono','JetBrains Mono',Menlo,Consolas,monospace;font-weight:500;fill:{INK}}}"
        f".{p}-mb{{font-family:'SB Mono','JetBrains Mono',Menlo,Consolas,monospace;font-weight:700;fill:{INK}}}"
        f".{p}-dim{{fill:{MUTED}}}"
    )


REDUCED = '@media (prefers-reduced-motion:reduce){*{animation:none!important}.%s-m_{display:none}.%s-s_{display:inline}}'


def reduced_css(p):
    # .p-ani = SMIL layer, .p-still = static twin shown only for reduced motion
    return (f'.{p}-still{{display:none}}'
            f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}'
            f'.{p}-ani{{display:none}}.{p}-still{{display:inline}}}}')


def shell(p, W, H, css, defs, body, title, desc):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="{p}-t {p}-ds">\n'
        f'{LICENSE_COMMENT}\n'
        f'<title id="{p}-t">{title}</title><desc id="{p}-ds">{desc}</desc>\n'
        f'<style>{css}</style>\n<defs>{defs}</defs>\n{body}\n</svg>\n'
    )


def common_defs(p, W, H):
    """gradients, dot texture, card clip - all ids namespaced"""
    return (
        f'<linearGradient id="{p}-edge" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{BLUE}" stop-opacity=".25"/>'
        f'<stop offset="1" stop-color="{CRIMSON}"/></linearGradient>'
        f'<linearGradient id="{p}-ink" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="#6aa8ff"/><stop offset="1" stop-color="#ff6b80"/></linearGradient>'
        f'<pattern id="{p}-dots" width="18" height="18" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.1" fill="#9db4ff" fill-opacity=".16"/></pattern>'
        f'<radialGradient id="{p}-gb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BLUE}" stop-opacity=".34"/>'
        f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="{p}-gc" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CRIMSON}" stop-opacity=".30"/>'
        f'<stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="{p}-card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28"/></clipPath>'
    )


def card_bg(p, W, H, glows=()):
    """navy card with dot texture, glows and gradient hairline. glows: (kind,cx,cy,r)"""
    g = ''.join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{p}-g{k})"/>' for k, x, y, r in glows)
    return (
        f'<g clip-path="url(#{p}-card)"><rect width="{W}" height="{H}" fill="{NAVY}"/>{g}'
        f'<rect width="{W}" height="{H}" fill="url(#{p}-dots)"/></g>'
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="none" stroke="url(#{p}-edge)" stroke-width="1.5"/>'
    )


def icon_path(key):
    return ICONS[key]['path']


def profile():
    return json.load(open(f'{B}/data/profile.json'))


def custom_glyph(key, cx, cy, size, color):
    k = size / 24
    t = f'translate({cx - size / 2:.2f} {cy - size / 2:.2f}) scale({k:.4f})'
    st = f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    if key == 'globe':
        return (f'<g transform="{t}" {st}><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.200 3 14.800 0 18M12 3c-3 3.200-3 14.800 0 18"/></g>')
    if key == 'journal':
        return (f'<g transform="{t}" {st}><path d="M6 3h11a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6z"/><path d="M6 3v18M10 8h5M10 12h5"/></g>')
    raise KeyError(key)


def icon_use(key, cx, cy, size, color=None):
    if key not in ICONS:
        return custom_glyph(key, cx, cy, size, color or INK)
    """brand glyph centred at cx,cy, drawn from a 24x24 path"""
    s = size / 24
    color = color or glyph_color(key)
    return (f'<path d="{icon_path(key)}" fill="{color}" '
            f'transform="translate({cx - size / 2:.2f} {cy - size / 2:.2f}) scale({s:.4f})"/>')


def f(n):
    return f'{n:.3f}'.rstrip('0').rstrip('.')


from fontTools.ttLib import TTFont as _TT


def _metrics(path):
    t = _TT(path)
    return t['cmap'].getBestCmap(), t['hmtx'], t['head'].unitsPerEm


_FM = {'disp': _metrics(f'{B}/fonts/manrope-latin-800-normal.woff2'),
       500: _metrics(f'{B}/fonts/inter-latin-500-normal.woff2'),
       600: _metrics(f'{B}/fonts/inter-latin-600-normal.woff2')}


def _w(key, text, size):
    c, h, u = _FM[key]
    return sum(h[c[ord(ch)]][0] for ch in text) * size / u


def disp_w(text, size):
    return _w('disp', text, size)


syne_w = disp_w                      # legacy name used across the generators


def body_w(text, size, weight=500):
    return _w(weight, text, size)
