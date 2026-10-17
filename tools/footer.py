import json
from lib import *
from dashboard import fmt_date
P='ft'; W,H=900,92
def build(path=None):
    st=json.load(open(path or f'{B}/data/stats.json'))
    msg="Thanks for visiting. Let's build something awesome."
    size=17
    while syne_w(msg,size)>780: size-=1
    css=font_css(P)+reduced_css(P)+f"@keyframes {P}-in{{from{{opacity:0}}to{{opacity:1}}}}.{P}-t{{animation:{P}-in .9s ease .2s both}}"
    body=card_bg(P,W,H,[('b',150,90,220),('c',760,0,220)])+(f'<g class="{P}-t"><text class="{P}-d" x="450" y="44" font-size="{size}" text-anchor="middle" letter-spacing="-.3">{msg}</text>'
          f'<text class="{P}-b {P}-dim" x="450" y="70" font-size="13" text-anchor="middle">Last updated {fmt_date(st["updated"])}</text></g>')
    return shell(P,W,H,css,common_defs(P,W,H),body,'Footer','Thanks for visiting. Last updated '+fmt_date(st['updated'])+'.')
if __name__=='__main__':
    open(f'{B}/out/assets/footer.svg','w').write(build()); print('ok')
