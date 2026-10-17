import json, datetime
from lib import *
import idcard as I

P = 'idc'
W, H = 900, 624
SC, TX = 0.82, -38
X0, RW = 340, 512
NUM = [('17+', 'projects completed'), ('3', 'patents, co-inventor'), ('9.01', 'CGPA, 6th semester'),
       ('90+', 'Google Arcade badges'), ('3', 'certifications'), ('Winner', 'INDOvateAI, 2025')]
LANG_COL = ['#247bff', '#ff354f', '#8d6bff', '#6aa8ff', '#ff8a9a', '#5b6a94']
HEAT = ['#141d33', '#1c4a99', '#247bff', '#7db3ff', '#ff354f']


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%b %Y")}'


def numbers():
    out = f'<text class="{P}-d" x="{X0}" y="58" font-size="22" letter-spacing="-.3">By the numbers</text>'
    cw = RW / 3
    for i, (v, lab) in enumerate(NUM):
        c, r = i % 3, i // 3
        x, y = X0 + c * cw, 76 + r * 90
        size = min(32, 150 / syne_w(v, 1))
        assert body_w(lab, 13) <= cw - 14, lab
        out += (f'<g class="{P}-row" style="animation-delay:{1.0 + i * .1:.2f}s">'
                f'<rect x="{f(x)}" y="{y}" width="{f(cw - 16)}" height="1" fill="url(#{P}-edge)" fill-opacity=".6"/>'
                f'<text class="{P}-d" x="{f(x)}" y="{y + 40}" font-size="{f(size)}" letter-spacing="-.5">{v}</text>'
                f'<text class="{P}-b" x="{f(x)}" y="{y + 62}" font-size="13">{lab}</text></g>')
    out += (f'<text class="{P}-b {P}-dim" x="{X0}" y="270" font-size="12">Portfolio figures as of 17 Oct 2026. Patents: 1 granted, 1 filed,</text>'
            f'<text class="{P}-b {P}-dim" x="{X0}" y="286" font-size="12">1 published. Winner among 200+ teams, per resume.</text>')
    return out


def heatmap(cal, x0, y0):
    if not cal:
        return '', 0
    days = [(datetime.date.fromisoformat(d), l) for d, l in cal]
    first = days[0][0]
    first -= datetime.timedelta(days=(first.weekday() + 1) % 7)       # back to the Sunday
    cell, pitch = 7.2, 9.6
    out = ''
    for d, l in days:
        col = (d - first).days // 7
        row = (d.weekday() + 1) % 7
        out += f'<rect x="{f(x0 + col * pitch)}" y="{f(y0 + row * pitch)}" width="{cell}" height="{cell}" rx="1.800" fill="{HEAT[min(l, 4)]}"/>'
    return out, 7 * pitch


def github(st):
    out = (f'<rect x="{X0}" y="304" width="{RW}" height="1" fill="url(#{P}-edge)" fill-opacity=".6"/>'
           f'<text class="{P}-d" x="{X0}" y="340" font-size="22" letter-spacing="-.3">GitHub</text>'
           f'<text class="{P}-b {P}-dim" x="{X0 + RW}" y="340" font-size="12" text-anchor="end">as of {fmt_date(st["updated"])}</text>')
    cm = st.get('commits_month')
    commits = (st['commits_year'], 'commits, 1 yr') if st.get('commits_year') is not None else \
              ((cm['value'], f'commits, {cm["label"].split()[0]}') if cm else (None, ''))
    tiles = [(st.get('repos'), 'public repos'), (st.get('followers'), 'followers'),
             (st.get('contributions'), 'contributions'), commits]
    tiles = [(v, l) for v, l in tiles if v is not None]            # unknown counts are omitted
    gap = 10
    tw = (RW - gap * (len(tiles) - 1)) / len(tiles)
    for i, (v, l) in enumerate(tiles):
        x = X0 + i * (tw + gap)
        assert body_w(l, 12) <= tw - 16, l
        out += (f'<g class="{P}-row" style="animation-delay:{1.6 + i * .1:.2f}s">'
                f'<rect x="{f(x)}" y="354" width="{f(tw)}" height="62" rx="14" fill="{CARD}" stroke="url(#{P}-edge)" stroke-opacity=".7" stroke-width="1.1"/>'
                f'<text class="{P}-d" x="{f(x + 14)}" y="388" font-size="24" letter-spacing="-.4">{v:,}</text>'
                f'<text class="{P}-b {P}-dim" x="{f(x + 14)}" y="406" font-size="12">{l}</text></g>')
    hm, hh = heatmap(st.get('calendar'), X0, 434)
    if hm:
        out += f'<g class="{P}-row" style="animation-delay:2.1s">{hm}</g>'
        y = 434 + hh + 20
        if st.get('streak_current') is not None:
            out += (f'<text class="{P}-b" x="{X0}" y="{y}" font-size="13">Current streak: {st["streak_current"]} days. '
                    f'Longest: {st["streak_longest"]} days.</text>'
                    f'<text class="{P}-b {P}-dim" x="{X0 + RW}" y="{y}" font-size="12" text-anchor="end">daily contributions, last year</text>')
    langs = st.get('languages') or []
    if langs:
        total = sum(c for _, c in langs)
        top = langs[:5]; other = total - sum(c for _, c in top)
        segs = top + ([('Other', other)] if other > 0 else [])
        by = 548
        out += f'<text class="{P}-b {P}-dim" x="{X0}" y="{by}" font-size="12">Top languages, by repository count</text>'
        out += f'<clipPath id="{P}-lc"><rect x="{X0}" y="{by + 8}" width="{RW}" height="10" rx="5"/></clipPath><g clip-path="url(#{P}-lc)">'
        x = X0
        for k, (n, c) in enumerate(segs):
            w = RW * c / total
            out += f'<rect x="{f(x)}" y="{by + 8}" width="{f(w + .5)}" height="10" fill="{LANG_COL[k]}"/>'
            x += w
        out += '</g>'
        lx, ly = X0, by + 40
        for k, (n, c) in enumerate(segs):
            txt = f'{n} {round(100 * c / total)}%'
            wl = body_w(txt, 12) + 22
            if lx + wl > X0 + RW:
                lx, ly = X0, ly + 18
            out += (f'<circle cx="{f(lx + 5)}" cy="{ly - 4}" r="4" fill="{LANG_COL[k]}"/>'
                    f'<text class="{P}-b" x="{f(lx + 16)}" y="{ly}" font-size="12">{txt}</text>')
            lx += wl + 8
    return out


def build(stats_path=None):
    st = json.load(open(stats_path or f'{B}/data/stats.json'))
    css = font_css(P) + reduced_css(P) + f"@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}.{P}-row{{animation:{P}-in .7s ease both}}"
    base = I.build()
    defs = re.search(r'<defs>(.*)</defs>', base, re.S).group(1)
    badge = f'<g transform="translate({TX} 0) scale({SC})"><g class="{P}-ani">{I.badge(True)}</g><g class="{P}-still">{I.badge(False)}</g></g>'
    body = card_bg(P, W, H, [('b', 160, 520, 300), ('c', 800, 80, 280)]) + badge + numbers() + github(st)
    desc = ('A lanyard ID badge with portrait, barcode and metal clasp that drops in and swings gently, beside six figures: 17 plus projects, 3 patents as co-inventor, CGPA 9.01 at the 6th semester, 90 plus Google Arcade badges, 3 certifications and an INDOvateAI 2025 win, plus GitHub activity: public repos, followers, contributions, commits, a year heatmap, streaks and top languages, as of ' + fmt_date(st['updated']) + '.')
    return shell(P, W, H, css, defs, body, 'Shlok Bam: ID badge, numbers and GitHub activity', desc)


if __name__ == '__main__':
    open(f'{B}/out/assets/id-dashboard.svg', 'w').write(build()); print('ok', os.path.getsize(f'{B}/out/assets/id-dashboard.svg'))
