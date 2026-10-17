from lib import *

P = 'idc'
W, H = 900, 724
PX, PY = 260, 10                  # pendulum pivot (top of the strap)
CARD_X, CARD_Y, CARD_W, CARD_H = 110, 238, 300, 462
MOD = 1.55

METRICS = [
    ('17+', 'projects completed', 'per portfolio, as of 17 Oct 2026'),
    ('3', 'patents as co-inventor', '1 granted, 1 filed, 1 published, 2025-26'),
    ('9.01', 'CGPA out of 10, 6th semester', 'VIT Pune, per portfolio, 17 Oct 2026'),
    ('90+', 'Google Arcade badges', 'Diamond League, 2025'),
    ('3', 'certifications completed', 'McKinsey, Google Cloud, AWS, 2025'),
    ('48', 'public GitHub repositories', 'github.com/shlokbam, as of 17 Oct 2026'),
]


def barcode_rects(x0, y0, h):
    bits = '100010111011101010111010111000101110101000111010101110101000111011101011101000101110101010001110101110100010111011101010001011101110111010100010100010111011101'  # Code 39 modules for SHLOKBAM
    out, i = '', 0
    while i < len(bits):
        if bits[i] == '1':
            j = i
            while j < len(bits) and bits[j] == '1':
                j += 1
            out += f'<rect x="{f(x0 + i * MOD)}" y="{y0}" width="{f((j - i) * MOD)}" height="{h}"/>'
            i = j
        else:
            i += 1
    return out, len(bits) * MOD


def pend_values(T=12.0, step=0.1, E=4.0, tau=2.3, Ts=3.4, t_land=0.66):
    n = int(T / step)
    vals = []
    for i in range(n + 1):
        t = i * step
        if t < t_land:
            a = 0
        else:
            ramp = min(1, (t - t_land) / 0.3)
            a = E * ramp * math.exp(-(t - t_land) / tau) * math.sin(2 * math.pi * (t - t_land) / Ts)
        vals.append(a if i < n else 0)
    return ';'.join(f'{f(v)} {PX} {PY}' for v in vals), ';'.join(f(i / n) for i in range(n + 1)), T


def hanger(animate):
    strap = (
        f'<rect x="{PX - 15}" y="-80" width="30" height="236" fill="url(#{P}-strap)"/>'
        f'<rect x="{PX - 12}" y="-80" width="1.4" height="236" fill="#ffffff" fill-opacity=".35"/>'
        f'<rect x="{PX + 10.6}" y="-80" width="1.4" height="236" fill="#ffffff" fill-opacity=".35"/>'
        f'<text class="{P}-d" font-size="11" fill="#fff" fill-opacity=".72" letter-spacing="2" transform="translate({PX + 4} 138) rotate(-90)">SHLOK BAM</text>'
        f'<text class="{P}-d" font-size="11" fill="#fff" fill-opacity=".72" letter-spacing="2" transform="translate({PX + 4} 52) rotate(-90)">SHLOK BAM</text>'
    )
    crimp = (f'<rect x="{PX - 17}" y="150" width="34" height="24" rx="5" fill="url(#{P}-metal)" stroke="#4a5470" stroke-width="1"/>'
             f'<rect x="{PX - 17}" y="158" width="34" height="2" fill="#4a5470" fill-opacity=".5"/>'
             f'<rect x="{PX - 17}" y="165" width="34" height="2" fill="#4a5470" fill-opacity=".5"/>')
    swivel = (f'<circle cx="{PX}" cy="181" r="7" fill="url(#{P}-metal)" stroke="#4a5470" stroke-width="1"/>')
    # lobster clasp
    claw = (f'<path d="M{PX - 13} 192 h26 a6 6 0 0 1 6 6 v18 a19 19 0 0 1 -19 19 a19 19 0 0 1 -19 -19 v-18 a6 6 0 0 1 6 -6 z" '
            f'fill="none" stroke="url(#{P}-metal)" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M{PX - 13} 192 h26 a6 6 0 0 1 6 6 v18 a19 19 0 0 1 -19 19 a19 19 0 0 1 -19 -19 v-18 a6 6 0 0 1 6 -6 z" '
            f'fill="none" stroke="#4a5470" stroke-opacity=".55" stroke-width=".9"/>'
            f'<rect x="{PX + 15}" y="203" width="9" height="14" rx="3" fill="url(#{P}-metal)" stroke="#4a5470" stroke-width="1"/>')
    ring = (f'<circle cx="{PX}" cy="{CARD_Y + 22}" r="11" fill="none" stroke="url(#{P}-metal)" stroke-width="4.200"/>'
            f'<circle cx="{PX}" cy="{CARD_Y + 22}" r="13" fill="none" stroke="#4a5470" stroke-opacity=".45" stroke-width=".8"/>')
    return strap + crimp + swivel + claw + ring


def card(animate):
    cx, cy = CARD_X, CARD_Y
    bars, bw = barcode_rects(0, 0, 40)
    bx = (CARD_W - 48 - bw) / 2 + 24
    sweep = ''
    if animate:
        sweep = (f'<g clip-path="url(#{P}-cc)"><g transform="translate(-460 0)">'
                 f'<animateTransform attributeName="transform" type="translate" '
                 f'values="-460 0;-460 0;520 0;520 0" keyTimes="0;.35;.62;1" dur="7s" begin="0s" repeatCount="indefinite" '
                 f'calcMode="linear"/>'
                 f'<rect x="0" y="-60" width="110" height="{CARD_H + 140}" fill="url(#{P}-sweep)" transform="rotate(18 55 {CARD_H / 2})"/></g></g>')
    return (
        f'<g transform="translate({cx} {cy})">'
        f'<g clip-path="url(#{P}-cc)">'
        f'<rect width="{CARD_W}" height="{CARD_H}" fill="url(#{P}-cbg)"/>'
        f'<rect width="{CARD_W}" height="{CARD_H}" fill="url(#{P}-dots)"/>'
        f'<rect width="{CARD_W}" height="46" fill="url(#{P}-foil)"/>'
        f'</g>'
        f'<rect x="{CARD_W / 2 - 28}" y="16" width="56" height="12" rx="6" fill="{NAVY}" stroke="#2b3656" stroke-width="1.2"/>'
        f'<g clip-path="url(#{P}-pw)"><rect x="24" y="58" width="252" height="206" fill="url(#{P}-pbg)"/>'
        f'<circle cx="40" cy="230" r="150" fill="url(#{P}-gb)"/><circle cx="270" cy="90" r="140" fill="url(#{P}-gc)"/>'
        f'<use xlink:href="#{P}-img" href="#{P}-img" x="24" y="58"/></g>'
        f'<rect x="24.600" y="58.600" width="250.800" height="204.800" rx="18" fill="none" stroke="url(#{P}-edge)" stroke-width="1.4"/>'
        f'<text class="{P}-d" x="24" y="306" font-size="29" letter-spacing="-.6">Shlok Bam</text>'
        f'<text class="{P}-m" x="24" y="331" font-size="15">AI / Generative AI Engineer</text>'
        f'<text class="{P}-m {P}-dim" x="24" y="353" font-size="14">Intern, PharmaACE Innovations</text>'
        f'<rect x="24" y="368" width="252" height="62" rx="9" fill="{INK}"/>'
        f'<g transform="translate({f(bx)} 379)" fill="{NAVY}">{bars}</g>'
        f'<text class="{P}-mb" x="{CARD_W / 2}" y="448" text-anchor="middle" font-size="12" letter-spacing="3" style="fill:{MUTED}">SHLOKBAM</text>'
        f'{sweep}'
        f'<rect x=".75" y=".75" width="{CARD_W - 1.5}" height="{CARD_H - 1.5}" rx="23" fill="none" stroke="url(#{P}-edge)" stroke-width="1.5"/>'
        f'</g>'
    )


def pendulum_anim():
    vals, kts, T = pend_values()
    A = 1.7
    steady = f'0 {PX} {PY};{A} {PX} {PY};0 {PX} {PY};{-A} {PX} {PY};0 {PX} {PY}'
    return (
        f'<animateTransform attributeName="transform" type="rotate" values="{vals}" keyTimes="{kts}" dur="{T}s" '
        f'begin="0s" fill="freeze" additive="replace" calcMode="linear"/>'
        f'<animateTransform attributeName="transform" type="rotate" values="{steady}" keyTimes="0;.25;.5;.75;1" '
        f'keySplines=".37 0 .63 1;.37 0 .63 1;.37 0 .63 1;.37 0 .63 1" calcMode="spline" dur="3.4s" begin="0s" '
        f'repeatCount="indefinite" additive="sum"/>'
    )


def drop_anim():
    return (f'<animateTransform attributeName="transform" type="translate" values="0 -780;0 0;0 -20;0 0" '
            f'keyTimes="0;.55;.76;1" calcMode="spline" keySplines=".55 0 1 .45;.2 .6 .4 1;.5 0 .5 1" dur="1.2s" '
            f'begin="0s" fill="freeze"/>')


def badge(animate):
    inner = hanger(animate) + card(animate)
    if not animate:
        return f'<g>{inner}</g>'
    return f'<g>{drop_anim()}<g>{pendulum_anim()}{inner}</g></g>'


def metrics():
    X = 540
    out = f'<text class="{P}-d" x="{X}" y="86" font-size="25" letter-spacing="-.4">By the numbers</text>'
    assert syne_w('By the numbers', 25) <= 316, syne_w('By the numbers', 25)
    for i, (v, lab, src) in enumerate(METRICS):
        y = 142 + i * 92
        d = 1.2 + i * 0.12
        out += (f'<g class="{P}-row" style="animation-delay:{d:.2f}s">'
                f'<rect x="{X}" y="{y - 22}" width="316" height="1" fill="url(#{P}-edge)" fill-opacity=".6"/>'
                f'<text class="{P}-d" x="{X}" y="{y + 28}" font-size="34" letter-spacing="-.6">{v}</text>'
                f'<text class="{P}-m" x="{X}" y="{y + 50}" font-size="15">{lab}</text>'
                f'<text class="{P}-m {P}-dim" x="{X}" y="{y + 68}" font-size="13">{src}</text></g>')
        assert mono_w(lab, 15) <= 316 and mono_w(src, 13) <= 316, (lab, src)
    return out


def build():
    css = font_css(P) + reduced_css(P) + f"""
@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}
.{P}-row{{animation:{P}-in .7s ease both}}
"""
    defs = common_defs(P, W, H) + (
        f'<linearGradient id="{P}-strap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b3182f"/>'
        f'<stop offset=".5" stop-color="{CRIMSON}"/><stop offset="1" stop-color="#a01428"/></linearGradient>'
        f'<linearGradient id="{P}-metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f7ff"/>'
        f'<stop offset=".42" stop-color="#9aa4bd"/><stop offset=".58" stop-color="#5f6985"/><stop offset="1" stop-color="#d5dbea"/></linearGradient>'
        f'<linearGradient id="{P}-cbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#131d38"/>'
        f'<stop offset="1" stop-color="#0a1020"/></linearGradient>'
        f'<linearGradient id="{P}-foil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/>'
        f'<stop offset=".5" stop-color="#8d6bff"/><stop offset="1" stop-color="{CRIMSON}"/></linearGradient>'
        f'<linearGradient id="{P}-pbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16224a"/>'
        f'<stop offset="1" stop-color="#0a1020"/></linearGradient>'
        f'<linearGradient id="{P}-sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity=".30"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="{P}-cc"><rect width="{CARD_W}" height="{CARD_H}" rx="24"/></clipPath>'
        f'<clipPath id="{P}-pw"><rect x="24" y="58" width="252" height="206" rx="18"/></clipPath>'
        f'<image id="{P}-img" width="252" height="301.4" preserveAspectRatio="xMidYMin slice" '
        f'xlink:href="data:image/png;base64,{PNG_ID}"/>'
    )
    body = card_bg(P, W, H, [('b', 160, 600, 320), ('c', 780, 120, 300)])
    body += (f'<g class="{P}-ani">{badge(True)}</g><g class="{P}-still">{badge(False)}</g>')
    body += metrics()
    return shell(P, W, H, css, defs, body, 'Shlok Bam ID badge with verified numbers',
                 'A lanyard ID badge with a portrait, barcode and metal clasp that drops in and swings gently, beside six dated figures: 17 plus projects completed, 3 patents as co-inventor, CGPA 9.01 at the 6th semester, 90 plus Google Arcade badges, 3 certifications, and 48 public GitHub repositories as of 17 October 2026.')


if __name__ == '__main__':
    open(f'{B}/out/assets/id-dashboard.svg', 'w').write(build())
    print('ok', os.path.getsize(f'{B}/out/assets/id-dashboard.svg'))
