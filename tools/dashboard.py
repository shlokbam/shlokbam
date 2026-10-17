import json, datetime
from lib import *
import idcard as I

P = 'idc'
W, H = 900, 560
SC, TX = 0.74, -21.4
X0, RW = 340, 512
NUM = [('17+', 'projects completed'), ('3', 'patents, co-inventor'), ('9.01', 'CGPA, 6th semester'),
       ('90+', 'Google Arcade badges'), ('3', 'certifications'), ('Winner', 'INDOvateAI, 2025')]
LANG_COL = ['#247bff', '#ff354f', '#8d6bff', '#6aa8ff', '#ff8a9a', '#5b6a94']


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%b %Y")}'


def numbers():
    out = f'<text class="{P}-d" x="{X0}" y="62" font-size="24" letter-spacing="-.4">By the numbers</text>'
    cw = RW / 3
    for i, (v, lab) in enumerate(NUM):
        c, r = i % 3, i // 3
        x, y = X0 + c * cw, 84 + r * 96
        size = min(36, 150 / (syne_w(v, 1)))
        assert mono_w(lab, 13) <= cw - 12, lab
        out += (f'<g class="{P}-row" style="animation-delay:{1.0 + i * .1:.2f}s">'
                f'<rect x="{f(x)}" y="{y}" width="{f(cw - 16)}" height="1" fill="url(#{P}-edge)" fill-opacity=".6"/>'
                f'<text class="{P}-d" x="{f(x)}" y="{y + 42}" font-size="{f(size)}" letter-spacing="-.6">{v}</text>'
                f'<text class="{P}-m" x="{f(x)}" y="{y + 66}" font-size="13">{lab}</text></g>')
    out += (f'<text class="{P}-m {P}-dim" x="{X0}" y="290" font-size="12">Portfolio figures as of 17 Oct 2026. Patents: 1 granted,</text>'
            f'<text class="{P}-m {P}-dim" x="{X0}" y="306" font-size="12">1 filed, 1 published. Winner among 200+ teams, per resume.</text>')
    return out


def github(st):
    out = (f'<rect x="{X0}" y="326" width="{RW}" height="1" fill="url(#{P}-edge)" fill-opacity=".6"/>'
           f'<text class="{P}-d" x="{X0}" y="366" font-size="22" letter-spacing="-.3">GitHub</text>'
           f'<text class="{P}-m {P}-dim" x="{X0 + RW}" y="366" font-size="12" text-anchor="end">as of {fmt_date(st["updated"])}</text>')
    tiles = [(st.get('repos'), 'public repos'), (st.get('followers'), 'followers'),
             (st.get('stars'), 'stars earned'), (st.get('contributions'), 'contributions, 1 yr')]
    tiles = [(v, l) for v, l in tiles if v is not None]       # unknown counts are omitted
    tw, gap = 118, 10
    for i, (v, l) in enumerate(tiles):
        x = X0 + i * (tw + gap)
        out += (f'<g class="{P}-row" style="animation-delay:{1.7 + i * .1:.2f}s">'
                f'<rect x="{x}" y="382" width="{tw}" height="66" rx="14" fill="{CARD}" stroke="url(#{P}-edge)" stroke-opacity=".7" stroke-width="1.1"/>'
                f'<text class="{P}-d" x="{x + 14}" y="418" font-size="26" letter-spacing="-.5">{v:,}</text>'
                f'<text class="{P}-m {P}-dim" x="{x + 14}" y="438" font-size="12">{l}</text></g>')
    langs = st.get('languages') or []
    if langs:
        total = sum(c for _, c in langs)
        top = langs[:5]; other = total - sum(c for _, c in top)
        segs = top + ([('Other', other)] if other > 0 else [])
        out += f'<text class="{P}-m {P}-dim" x="{X0}" y="474" font-size="12">Top languages, by repository count</text>'
        out += f'<clipPath id="{P}-lc"><rect x="{X0}" y="482" width="{RW}" height="12" rx="6"/></clipPath><g clip-path="url(#{P}-lc)">'
        x = X0; lx, ly = X0, 516
        for k, (n, c) in enumerate(segs):
            w = RW * c / total
            out += f'<rect x="{f(x)}" y="482" width="{f(w + .5)}" height="12" fill="{LANG_COL[k]}"/>'
            x += w
        out += '</g>'
        for k, (n, c) in enumerate(segs):
            txt = f'{n} {round(100 * c / total)}%'
            wlab = mono_w(txt, 12) + 22
            if lx + wlab > X0 + RW:
                lx, ly = X0, ly + 20
            out += (f'<circle cx="{f(lx + 5)}" cy="{ly - 4}" r="4" fill="{LANG_COL[k]}"/>'
                    f'<text class="{P}-m" x="{f(lx + 16)}" y="{ly}" font-size="12">{txt}</text>')
            lx += wlab + 8
    return out


def build(stats_path=None):
    st = json.load(open(stats_path or f'{B}/data/stats.json'))
    css = font_css(P) + reduced_css(P) + f"@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}.{P}-row{{animation:{P}-in .7s ease both}}"
    base = I.build()
    # reuse badge defs/markup from idcard, scaled
    defs = re.search(r'<defs>(.*)</defs>', base, re.S).group(1)
    badge = f'<g transform="translate({TX} 0) scale({SC})"><g class="{P}-ani">{I.badge(True)}</g><g class="{P}-still">{I.badge(False)}</g></g>'
    body = card_bg(P, W, H, [('b', 160, 480, 300), ('c', 800, 80, 280)]) + badge + numbers() + github(st)
    desc = ('A lanyard ID badge with portrait, barcode and metal clasp that drops in and swings gently, beside six figures: 17 plus projects, 3 patents as co-inventor, CGPA 9.01 at the 6th semester, 90 plus Google Arcade badges, 3 certifications and an INDOvateAI 2025 win, plus GitHub activity as of ' + fmt_date(st['updated']) + '.')
    return shell(P, W, H, css, defs, body, 'Shlok Bam: ID badge, numbers and GitHub activity', desc)


if __name__ == '__main__':
    open(f'{B}/out/assets/id-dashboard.svg', 'w').write(build()); print('ok', os.path.getsize(f'{B}/out/assets/id-dashboard.svg'))
