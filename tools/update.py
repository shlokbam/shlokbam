"""Regenerates the three data-driven images (id-dashboard, writing, footer) and cache-busts them in README.md.
Run by .github/workflows/update-profile.yml; safe to run locally:  python tools/update.py [--offline]
Any fetch that fails keeps the previous value, so a flaky API never blanks the profile."""
import json, os, re, sys, datetime, collections, urllib.request, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
USER = 'shlokbam'
TOKEN = os.environ.get('GITHUB_TOKEN', '')
OFFLINE = '--offline' in sys.argv


def get(url, data=None, headers=None):
    h = {'User-Agent': 'profile-readme-updater', 'Accept': 'application/vnd.github+json'}
    if TOKEN:
        h['Authorization'] = f'Bearer {TOKEN}'
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def parse_calendar(html):
    """Reads github.com/users/<user>/contributions (public HTML, no token needed)."""
    cells = re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?data-level="(\d)"', html)
    if not cells:
        cells = [(d, l) for l, d in re.findall(r'data-level="(\d)"[^>]*?data-date="(\d{4}-\d\d-\d\d)"', html)]
    cells = sorted(set((d, int(l)) for d, l in cells))
    m = re.search(r'([\d,]+)\s+contributions\s+in\s+the\s+last\s+year', re.sub(r'\s+', ' ', html))
    total = int(m.group(1).replace(',', '')) if m else None
    cur = best = run = 0
    for _, lvl in cells:
        run = run + 1 if lvl > 0 else 0
        best = max(best, run)
    for _, lvl in reversed(cells):            # current streak: a still-empty "today" does not break it
        if lvl > 0:
            cur += 1
        elif cur == 0 and _ == cells[-1][0]:
            continue
        else:
            break
    return {'calendar': [[d, l] for d, l in cells], 'contributions': total, 'streak_current': cur, 'streak_longest': best}


def refresh_stats(st):
    ok = False
    try:
        u = json.loads(get(f'https://api.github.com/users/{USER}'))
        st['repos'], st['followers'], st['following'] = u['public_repos'], u['followers'], u['following']
        repos, page = [], 1
        while True:
            chunk = json.loads(get(f'https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}'))
            repos += chunk
            if len(chunk) < 100:
                break
            page += 1
        own = [r for r in repos if not r.get('fork')]
        st['stars'] = sum(r.get('stargazers_count', 0) for r in own)
        langs = collections.Counter(r['language'] for r in own if r.get('language'))
        if langs:
            st['languages'] = [[k, v] for k, v in langs.most_common()]
        ok = True
        print('stats refreshed from the REST API')
    except Exception as e:
        print('WARNING: REST stats not refreshed, keeping previous values:', e)
    try:
        cal = parse_calendar(get(f'https://github.com/users/{USER}/contributions', headers={'Accept': 'text/html'}))
        if cal['calendar']:
            st.update({k: v for k, v in cal.items() if v is not None})
            ok = True
            print('contribution calendar refreshed')
    except Exception as e:
        print('WARNING: calendar not refreshed:', e)
    if TOKEN:
        try:
            first = datetime.date.today().replace(day=1).isoformat() + 'T00:00:00Z'
            q = json.dumps({'query': 'query($l:String!,$f:DateTime!){user(login:$l){a:contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions} m:contributionsCollection(from:$f){totalCommitContributions}}}',
                            'variables': {'l': USER, 'f': first}}).encode()
            u = json.loads(get('https://api.github.com/graphql', data=q, headers={'Content-Type': 'application/json'}))['data']['user']
            st['commits_year'] = u['a']['totalCommitContributions']
            st['pull_requests_year'] = u['a']['totalPullRequestContributions']
            st['commits_month'] = {'label': datetime.date.today().strftime('%b %Y'), 'value': u['m']['totalCommitContributions']}
            print('commit totals refreshed')
        except Exception as e:
            print('WARNING: commit totals not refreshed:', e)
    if ok:   # only re-date the numbers when they were really refreshed
        st['updated'] = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    return st


def refresh_writing(posts):
    """Prepend any Medium post not already listed. The journal has no feed, so journal posts are edited by hand in data/writing.json."""
    try:
        xml = get(f'https://medium.com/feed/@{USER.capitalize()}', headers={'Accept': 'application/rss+xml'})
        items = ET.fromstring(xml).findall('./channel/item')
        known = {p['url'].split('?')[0] for p in posts}
        fresh = []
        for it in items[:5]:
            url = (it.findtext('link') or '').split('?')[0]
            title = (it.findtext('title') or '').strip()
            if url and title and url not in known:
                fresh.append({'title': title, 'subtitle': '', 'url': url, 'source': 'Medium'})
        posts = fresh + posts
        print(f'medium: {len(fresh)} new post(s)')
    except Exception as e:
        print('WARNING: Medium feed not read, keeping the current list:', e)
    return posts


def main():
    sp, wp = f'{HERE}/data/stats.json', f'{HERE}/data/writing.json'
    st, posts = json.load(open(sp)), json.load(open(wp))
    if OFFLINE:
        print('offline mode: using stored data')
    else:
        st, posts = refresh_stats(st), refresh_writing(posts)
        json.dump(st, open(sp, 'w'), indent=1)
        json.dump(posts, open(wp, 'w'), indent=1)
    sys.path.insert(0, HERE)
    import dashboard, writing, footer
    os.makedirs(f'{ROOT}/assets', exist_ok=True)
    for name, mod in (('id-dashboard', dashboard), ('writing', writing), ('footer', footer)):
        open(f'{ROOT}/assets/{name}.svg', 'w').write(mod.build())
        print('wrote assets/%s.svg' % name)
    rd = f'{ROOT}/README.md'
    if os.path.exists(rd):
        stamp = st['updated'].replace('-', '')
        txt = open(rd).read()
        for name in ('id-dashboard', 'writing', 'footer'):
            txt = re.sub(rf'(assets/{name}\.svg\?v=)[\w]+', rf'\g<1>{stamp}', txt)
        open(rd, 'w').write(txt)


if __name__ == '__main__':
    main()
