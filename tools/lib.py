import base64, json, math, os, re

B = os.path.dirname(os.path.abspath(__file__))
NAVY, BLUE, CRIMSON, INK = '#070b16', '#247bff', '#ff354f', '#f2f4fa'
CARD = '#0d1424'
MUTED = '#9aa5c0'
ICONS = json.load(open(f'{B}/icons.json'))


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


FONT_SYNE = b64(f'{B}/fonts/syne-latin-800-normal.woff2')
FONT_M500 = b64(f'{B}/fonts/jetbrains-mono-latin-500-normal.woff2')
FONT_M700 = b64(f'{B}/fonts/jetbrains-mono-latin-700-normal.woff2')
PNG_ID = b64(f'{B}/id.png')
PNG_POINT = b64(f'{B}/right_pointing.png') if os.path.exists(f'{B}/right_pointing.png') else ''

LICENSE_COMMENT = (
    '<!-- Fonts embedded as base64 WOFF2 under the SIL Open Font License 1.1: '
    'Syne (c) 2019 The Syne Project Authors; JetBrains Mono (c) 2020 The JetBrains Mono Project Authors. '
    'Full texts: LICENSES/OFL-Syne.txt, LICENSES/OFL-JetBrainsMono.txt. '
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
    return (
        f"@font-face{{font-family:'SB Syne';font-weight:800;src:url(data:font/woff2;base64,{FONT_SYNE}) format('woff2');}}"
        f"@font-face{{font-family:'SB Mono';font-weight:500;src:url(data:font/woff2;base64,{FONT_M500}) format('woff2');}}"
        f"@font-face{{font-family:'SB Mono';font-weight:700;src:url(data:font/woff2;base64,{FONT_M700}) format('woff2');}}"
        f".{p}-d{{font-family:'SB Syne','Arial Black','Segoe UI',sans-serif;font-weight:800;fill:{INK}}}"
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


def icon_use(key, cx, cy, size, color=None):
    """brand glyph centred at cx,cy, drawn from a 24x24 path"""
    s = size / 24
    color = color or glyph_color(key)
    return (f'<path d="{icon_path(key)}" fill="{color}" '
            f'transform="translate({cx - size / 2:.2f} {cy - size / 2:.2f}) scale({s:.4f})"/>')


def f(n):
    return f'{n:.3f}'.rstrip('0').rstrip('.')


from fontTools.ttLib import TTFont as _TT
_sy = _TT(f'{B}/fonts/syne-latin-800-normal.woff2')
_sy_c, _sy_h, _sy_u = _sy['cmap'].getBestCmap(), _sy['hmtx'], _sy['head'].unitsPerEm


def syne_w(text, size):
    return sum(_sy_h[_sy_c[ord(ch)]][0] for ch in text) * size / _sy_u
