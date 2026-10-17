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
    if TOKEN:
        try:
            q = json.dumps({'query': 'query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions}}}}',
                            'variables': {'l': USER}}).encode()
            res = json.loads(get('https://api.github.com/graphql', data=q, headers={'Content-Type': 'application/json'}))
            st['contributions'] = res['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
        except Exception as e:
            print('WARNING: contributions not refreshed:', e)
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
